# Source: https://github.com/terrywbrady/CldAws230/blob/project/lambda/getInstances.py
#
# This code is used by the DSpace Launcher Dashboard Application.  This code is deployed as 4 separate Lambdas.
# - projListInstances  - list EC2 instances started by the DSpace Launcher Dashboard
# - projStopInstance   - manually stop an EC2 instance started by the DSpace Launcher Dashboard
# - projCreateInstance - start a new EC2 instance that will run DSpace using Docker Compose
# - projTimer          - kill a DSpace EC2 instance that has exceeded its allotted uptime (cost management)

import boto3
import json
import sys
import base64
import dateutil.tz
import datetime

# =====================================================
# AWS System Manager Parameter Store
#
# The parameter store is designed to throttle the costs associated with the
# resources launched from the dashboard without needing to redeploy code.
# =====================================================
ssm = boto3.client('ssm', region_name="us-west-2")
def getSSMParam(key, value):
    p = ssm.get_parameter(Name=key)
    return p['Parameter']['Value'] if p else value

def getSSMIntParam(key, value):
    return int(getSSMParam(key, value))

# =====================================================
# Constants
# =====================================================

DSPACE_TAG_NAME  = "DSpace"
DSPACE_TAG_VALUE = "DSpace"
MAX_INSTANCE     = getSSMIntParam("DSPACE_DASHBOARD.MAX_INSTANCES", 2)
REGION           = 'us-west-2'
TZONE            = dateutil.tz.gettz('US/Pacific')
UPTIME           = getSSMParam("DSPACE_DASHBOARD.UPTIME", "60")
INSTTYPE         = getSSMParam("DSPACE_DASHBOARD.INSTANCE_TYPE", "t2.xlarge")
AMI              = getSSMParam("DSPACE_DASHBOARD.AMI", "ami-01861f340864168b2")
KEYNAME          = getSSMParam("DSPACE_DASHBOARD.KEYNAME", "week8key")

# =====================================================
# Get Instances started from the DSpace Launcher dashboard
# =====================================================

# Lambda invoked from web form via API gateway
# --------------------------------------------
def lambda_getInstances(event, context):
    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(getInstanceJsonObjects())
    }

# Get a list of EC2 instances launched from the dashboard.
# Return the list of instances as dashboard objects
def getInstanceObjects():
    fres = []
    for instance in getInstances():
        fres.append(makeObj(instance))
    return fres

# Return the set of running DSpace instances as a json result
def getInstanceJsonObjects():
    json = []
    for instance in getInstances():
        obj = makeObj(instance)
        obj['launchTime'] = str(obj['launchTime'].astimezone(TZONE)) + " PT"
        obj['endTime'] = str(obj['endTime'].astimezone(TZONE)) + " PT"
        json.append(obj)
    return json

# Make a DSpace Dashboard Object from and EC2 instance.
# Read the EC2 tags to determine the start time, end time, branch, and PR for the instance.
# The services associated with an instance will vary based on the DSpace branch that was started.
def makeObj(instance):
    tags = instance['Tags']
    uptime = int(getTagVal(tags, "UPTIME", UPTIME))

    dstart = instance['LaunchTime']
    dend = dstart + datetime.timedelta(minutes=uptime)
    branch = getTagVal(tags, 'Branch', "")
    services = []
    if branch == "master" or branch == "preview":
        services.append({
            "name":"rest",
            "path":":8080/spring-rest"
        })
        services.append({
            "name":"angular",
            "path":":3000"
        })
    elif branch == "dspace-6_x" or branch == "dspace-5_x" or branch == "dspace-4_x":
        services.append({
            "name":"xmlui",
            "path":":8080/xmlui"
        })
        services.append({
            "name":"jspui",
            "path":":8080/jspui"
        })
    return {
        'found': 1,
        'name': getTagVal(tags, 'Name', ""),
        'branch': branch,
        'pr': getTagVal(tags, 'PRNUM', ""),
        'id': instance['InstanceId'],
        'state': instance['State']['Name'],
        'dns': getKey(instance, 'PublicDnsName', ""),
        'launchTime': dstart,
        'endTime': dend,
        'logs': 'tbd',
        'services': services
    }

# =====================================================
# Start Instances
# =====================================================

# Get a set of EC2 tags for a PR and branch
def getTags(pr, branch, title):
    return [
        {
            'Key': DSPACE_TAG_NAME,
            'Value': DSPACE_TAG_VALUE
        },
        {
            'Key':'Name',
            'Value': title
        },
        {
            'Key':'UPTIME',
            'Value': UPTIME
        },
        {
            'Key':'Branch',
            'Value': branch
        },
        {
            'Key':'PRNUM',
            'Value': pr
        }
    ]

# Based on the Branch and PR to be started, construct the the bootstrap script that will
# launch Docker Compose.
# See https://github.com/DSpace-Labs/DSpace-Docker-images for an explanation of the
# DSpace Docker Compose Options.
# If DSpace were to pre-build docker images for every active pull request, the bootstrap logic
# could be simplified.
def getUserData(pr, branch):
    ver = " -f d7.override.yml"
    if branch == "master":
      ver = " -f d7.override.yml -f load.entities.yml"
    elif branch == "preview":
      ver = " -f d7.override.yml -f d7.preview.yml -f load.entities.yml"
    elif branch == "dspace-6_x":
      ver = " -f d6.override.yml"
    elif branch == "dspace-5_x":
      ver = " -f d5.override.yml"
    elif branch == "dspace-4_x":
      ver = " -f d4.override.yml"

    commands = [
        "cd /home/ec2-user/DSpace-Docker-Images",
        "DNS=`curl -s http://169.254.169.254/latest/meta-data/public-hostname`",
        "echo DNS=${DNS}",
        "export BASEROOT=http://${DNS}:8080",
        "sed -i -e s/localhost/${DNS}/ add-ons/angular-tools/environment.dev.js"
    ]
    if (pr != ""):
        commands = [
            "cd /home/ec2-user/",
            "git clone https://github.com/DSpace/DSpace.git",
            "cd DSpace",
            "git checkout " + branch,
            "git pull",
            "export DSPACE_SRC=$PWD",
            "curl -o /tmp/pr.patch -L https://github.com/DSpace/DSpace/pull/" + pr + ".diff",
            "git apply /tmp/pr.patch",
        ]

    commands.append("cd /home/ec2-user/DSpace-Docker-Images")
    commands.append("git pull origin")
    commands.append("cd docker-compose-files/dspace-compose")

    if (pr != ""):
        commands.append("docker-compose -p dspace -f docker-compose.yml " + ver + " -f src.override.yml build")
        commands.append("docker-compose -p dspace -f docker-compose.yml " + ver + " -f src.override.yml pull")
        commands.append("docker-compose -p dspace -f docker-compose.yml " + ver + " -f src.override.yml up -d")
    else:
        commands.append("docker-compose -p dspace -f docker-compose.yml " + ver + " pull")
        commands.append("docker-compose -p dspace -f docker-compose.yml " + ver + " up -d")

    return "#!/bin/bash\nsudo su -l ec2-user -c '" + ";".join(commands) + "'"

# Start and EC2 instance that will run a specific branch/pull request for DSpace.
# Set the EC2 tags to convey dashboard metadata for the instance.
# Set the userdata for the EC2 instance to bootstrap the call to docker-compose up
def startInstance(pr, branch, title):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.create_instances
    # https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html
    ec2 = getEC2()
    instances = ec2.run_instances(
        MaxCount=1,
        MinCount=1,
        ImageId=AMI,
        InstanceType=INSTTYPE,
        UserData=getUserData(pr, branch),
        KeyName=KEYNAME
    )
    ids=[]
    for instance in instances['Instances']:
        ids.append(instance['InstanceId'])
    ec2.create_tags(Resources=ids,Tags=getTags(pr, branch, title))
    return ids

# Verify that the number of DSpace instances does not exceed the maiximum allowed by the dashbaord
def checkRunningInstances():
    return len(getInstanceObjects()) < MAX_INSTANCE

# API Gateway interface for the lambda that starts an instance
def lambda_startInstances(event, context):
    body = json.loads(event['body'])
    pr = body['prnum']
    branch = body['base']
    title = body['title']
    if checkRunningInstances():
        ids = startInstance(pr, branch, title)
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps([pr, branch, title])
        }
    else:
        return {
            'statusCode': 429,
            'headers': { 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps("Too many running instances")
        }


# =====================================================
# Stop Instances
# =====================================================

# Lambda invoked from web form via API gateway to stop all running instances
# --------------------------------------------
def lambda_stopInstances(event, context):
    ids = stopInstances()
    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(ids)
    }

# Stop all DSpace instances started from the dashboard
def stopInstances():
    objarr = getInstanceObjects()
    ids = getObjIds(objarr)
    if (len(ids) > 0):
        ec2 = getEC2().terminate_instances(InstanceIds=ids)
    return ids

# Lambda invoked from web form via API gateway to stop a specific instance
# --------------------------------------------
def lambda_stopInstance(event, context):
    qp = event["queryStringParameters"] if 'queryStringParameters' in event else {}
    id = qp['id'] if 'id' in qp else ""
    ids = stopInstance(id)
    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(ids)
    }

# Stop a specific DSpace instance
def stopInstance(id):
    objarr = getInstanceObjects()
    ids = getObjIdsByVal(objarr, id)
    if (len(ids) > 0):
        ec2 = getEC2().terminate_instances(InstanceIds=ids)
    return ids

# Lambda invoked by cron/schedule - will run every 5 min to stop instnaces beyond their allotted time
# ------------------------------------------------------
def lambda_stopOvertimeInstances(event, context):
    ids = stopOvertimeInstances()
    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(ids)
    }

# Stop any DSpace instance over its allotted time
def stopOvertimeInstances():
    objarr = getInstanceObjects()
    ids = getObjIdsByDate(objarr)
    if (len(ids) > 0):
        ec2 = getEC2().terminate_instances(InstanceIds=ids)
    return ids

# =====================================================
# Common Functions
# =====================================================

# TODO: make this smarter  and more portable
def getEC2():
    return boto3.client('ec2', region_name=REGION)

# Filter EC2 Reservations instances by tags to find instances started from the dashboard
def getReservations():
    return getEC2().describe_instances(
        Filters=[
            {
                'Name': 'tag:' + DSPACE_TAG_NAME,
                'Values': [DSPACE_TAG_VALUE]
            },
            {
                'Name': 'instance-state-name',
                'Values': ['running', 'pending', 'stopping', 'shutting-down']
            },
        ]
    )

# get istances for AWS reservations that match a set of criteria
def getInstances():
    instances = []
    for res in getKey(getReservations(), 'Reservations', []):
        for instance in getKey(res, 'Instances', []):
            instances.append(instance)
    return instances

# Helper method for locating an EC2 tag from a python dictionary
def getKey(dictname, name, value):
    return dictname[name] if name in dictname else value

# Retrieve an EC2 tag value or a default if the value is not defined
def getTagVal(tags, name, value):
    for tag in tags:
        if (getKey(tag, 'Key', "") == name):
            return getKey(tag, 'Value', value)
    return value

# Create an array of AWS object ids from an array of AWS objects
def getObjIds(objarr):
    ids=[]
    for obj in objarr:
        ids.append(obj['id'])
    return ids

# Create an array of AWS objects ids searching a list of objects for a specific value
def getObjIdsByVal(objarr, val):
    ids=[]
    for obj in objarr:
        if obj['id'] == val:
            ids.append(val)
    return ids

# Create an array of AWS objects ids searching a list of objects for a specific date value
def getObjIdsByDate(objarr):
    ids=[]
    for obj in objarr:
        if obj['endTime'] < datetime.datetime.now(dateutil.tz.UTC):
            ids.append(obj['id'])
    return ids


# =====================================================
# Testing command line - these methods allow testing from AWS Cloud 9 
# =====================================================

def printObj(obj):
    d = obj['endTime'].astimezone(TZONE)
    stat = "OVERTIME" if (obj['endTime'] < datetime.datetime.now(dateutil.tz.UTC)) else "--"
    print "\t" + obj['id'] + "\t" + obj['name'] + "\t" + obj['state'] + "\t" + obj['dns'] + "\t" + str(d) + "\t" + stat


def doCommandLine():
    if len(sys.argv)== 0:
        return

    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    opt = sys.argv[2] if len(sys.argv) > 2 else ""
    opt2 = sys.argv[3] if len(sys.argv) > 3 else ""
    opt3 = sys.argv[4] if len(sys.argv) > 4 else ""
    if (cmd == "start"):
        if checkRunningInstances():
            ids = startInstance(opt, opt2, opt3)
            print "started " + str(ids)
        else:
            print "ERROR: Too Many Running Instances"
    elif (cmd == "stop"):
        ids = []
        if (opt == "all"):
            ids = stopInstances()
        else:
            ids = stopInstance(opt)
        print "Stopped " + str(ids)
    elif (cmd == "timer"):
        ids = stopOvertimeInstances()
        print "Stopped " + str(ids)
    elif (cmd == "userdata"):
        print getUserData(opt, opt2)
    else:
        print "list instances: " + str(datetime.datetime.now(TZONE))
        for obj in getInstanceObjects():
            printObj(obj)

# if testing from Cloud9, rather than Lambda, process command line
doCommandLine()
