# Source: https://github.com/terrywbrady/CldAws230/blob/project/lambda/getInstances.py
import boto3
import json
import sys
import base64
import dateutil.tz
import datetime

# =====================================================
# Constants
# =====================================================
DSPACE_TAG_NAME  = "DSpace"
DSPACE_TAG_VALUE = "DSpace"
MAX_INSTANCE     = 2
REGION           = 'us-west-2'
TZONE            = dateutil.tz.gettz('US/Pacific')
UPTIME           = "60"

# =====================================================
# Get Instances
# =====================================================

# Lambda invoked from web form via API gateway
# --------------------------------------------
def lambda_getInstances(event, context):
    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(getInstanceJsonObjects())
    }
    
def getInstanceObjects():
    fres = []
    for instance in getInstances(): 
        fres.append(makeObj(instance))
    return fres

def getInstanceJsonObjects():
    json = []
    for instance in getInstances(): 
        obj = makeObj(instance)
        obj['launchTime'] = str(obj['launchTime'].astimezone(TZONE))
        obj['endTime'] = str(obj['endTime'].astimezone(TZONE))
        json.append(obj)
    return json

def makeObj(instance):
    tags = instance['Tags']
    uptime = int(getTagVal(tags, "UPTIME", UPTIME))
    
    dstart = instance['LaunchTime']
    dend = dstart + datetime.timedelta(minutes=uptime)
    return { 
        'found': 1,
        'name': getTagVal(tags, 'Name', ""),
        'id': instance['InstanceId'],
        'state': instance['State']['Name'],
        'dns': getKey(instance, 'PublicDnsName', ""),
        'launchTime': dstart,
        'endTime': dend,
        'logs': 'tbd',
        'config': {
            'branch': 'tbd',
            'pr': 'tbd',
            'started_by': 'tbd',
            'environment': {},
            'services': {
                'name': 'tbd',
                'url': 'tbd'
            }
        }
    }
    
# =====================================================
# Start Instances
# =====================================================

# TODO: Make this smarter - find the source image by tag name
def getAmi():
    return "ami-01861f340864168b2" #dspace-source

def getTags():
    return [
        {
            'Key': DSPACE_TAG_NAME,
            'Value': DSPACE_TAG_VALUE
        },
        {
            'Key':'Name',
            'Value':'MyDSpaceProject'
        },
        {
            'Key':'UPTIME',
            'Value': UPTIME
        }
    ]

# TODO: read context from instance
def getUserData():
    commands = [
        "cd /home/ec2-user/DSpace-Docker-Images",
        "git pull origin",
        "cd docker-compose-files/dspace-compose",
        "docker-compose -p d6 -f docker-compose.yml -f d6.override.yml up -d"
    ]
    return "#!/bin/bash\nsudo su -l ec2-user -c '" + ";".join(commands) + "'"

# TODO: Take Parameters
def startInstance():
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.create_instances
    # https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html
    ec2 = getEC2()
    instances = ec2.run_instances(
        MaxCount=1,
        MinCount=1,
        ImageId=getAmi(),
        InstanceType='t2.large',
        UserData=getUserData(),
        KeyName='week8key'
    )
    ids=[]
    for instance in instances['Instances']:
        ids.append(instance['InstanceId'])
    ec2.create_tags(Resources=ids,Tags=getTags())
    return ids

def checkRunningInstances():
    return len(getInstanceObjects()) < MAX_INSTANCE

def lambda_startInstances(event, context):
    if checkRunningInstances():
        ids = startInstance()
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(ids)
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

# Lambda invoked from web form via API gateway
# --------------------------------------------
def lambda_stopInstances(event, context):
    ids = stopInstances()
    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(ids)
    }
    
def stopInstances():
    objarr = getInstanceObjects()
    ids = getObjIds(objarr)
    if (len(ids) > 0):
        ec2 = getEC2().stop_instances(InstanceIds=ids)
    return ids

# Lambda invoked from web form via API gateway
# --------------------------------------------
def lambda_stopInstance(event, context):
    # TODO: read from context
    ids = stopInstance("xx")
    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(ids)
    }

def stopInstance(id):
    objarr = getInstanceObjects()
    ids = getObjIdsByVal(objarr, id)
    if (len(ids) > 0):
        ec2 = getEC2().stop_instances(InstanceIds=ids)
    return ids

# Lambda invoked by cron/schedule - will run every 5 min
# ------------------------------------------------------
def lambda_stopOvertimeInstances(event, context):
    ids = stopOvertimeInstances()
    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(ids)
    }

def stopOvertimeInstances():
    objarr = getInstanceObjects()
    ids = getObjIdsByDate(objarr)
    if (len(ids) > 0):
        ec2 = getEC2().stop_instances(InstanceIds=ids)
    return ids

# =====================================================
# Common Functions
# =====================================================

# TODO: make this smarter  and more portable
def getEC2():
    return boto3.client('ec2', region_name=REGION)

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
    
def getInstances():
    instances = []
    for res in getKey(getReservations(), 'Reservations', []):
        for instance in getKey(res, 'Instances', []): 
            instances.append(instance)
    return instances
    
def getKey(dictname, name, value):
    return dictname[name] if name in dictname else value 

def getTagVal(tags, name, value):
    for tag in tags:
        if (getKey(tag, 'Key', "") == name):
            return getKey(tag, 'Value', value)
    return value

def getObjIds(objarr):
    ids=[]
    for obj in objarr:
        ids.append(obj['id'])
    return ids    
    
def getObjIdsByVal(objarr, val):
    ids=[]
    for obj in objarr:
        if obj['id'] == val:
            ids.append(val)
    return ids    

def getObjIdsByDate(objarr):
    ids=[]
    for obj in objarr:
        if obj['endTime'] < datetime.datetime.now(dateutil.tz.UTC):
            ids.append(obj['id'])
    return ids    


# =====================================================
# Testing command line
# =====================================================

def printObj(obj):
    d = obj['endTime'].astimezone(TZONE)
    stat = "OVERTIME" if (obj['endTime'] < datetime.datetime.now(dateutil.tz.UTC)) else "--"
    print "\t" + obj['id'] + "\t" + obj['state'] + "\t" + obj['dns'] + "\t" + str(d) + "\t" + stat


def doCommandLine():
    if len(sys.argv)== 0:
        return
    
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    opt = sys.argv[2] if len(sys.argv) > 2 else ""
    if (cmd == "start"):
        if checkRunningInstances():
            ids = startInstance()
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
        print getUserData()
    else:
        print "list instances: " + str(datetime.datetime.now(TZONE)) 
        for obj in getInstanceObjects():
            printObj(obj)
        
# if testing from Cloud9, rather than Lambda, process command line
doCommandLine()
