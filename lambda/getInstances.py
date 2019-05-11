# Source: https://github.com/terrywbrady/CldAws230/blob/project/lambda/getInstances.py
import boto3
import json
import sys

from datetime import timedelta

#from dateutil import tz
#HERE = tz.tzlocal()


def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps(getInstanceObjects())
    }
    
    
def getInstanceObjects():
    fres = []
    for instance in getInstances(): 
        fres.append(makeObj(instance))
    return fres

def makeObj(instance):
    tags = instance['Tags']
    return { 
        'found': 1,
        'name': getKey(tags, 'Name', ""),
        'id': instance['InstanceId'],
        'state': instance['State']['Name'],
        'dns': getKey(instance, 'PublicDnsName', ""),
        'launchTime': str(instance['LaunchTime']),
        'endTime': str((instance['LaunchTime'] + timedelta(hours=1))),
        'logs': 'tbd',
        'config': {
            'branch': 'tbd',
            'pr': 'tbd',
            'started_by': 'tbd',
            'requrested_timeout': 60,
            'environment': {},
            'services': {
                'name': 'tbd',
                'url': 'tbd'
            }
        }
    }

# Common Functions

def getEC2():
    region = 'us-west-2'
    return boto3.client('ec2', region_name=region)

def getReservations():
    return getEC2().describe_instances(
        Filters=[
            {
                'Name': 'tag:DSpace',
                'Values': ['DSpace']
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

# Testing command line

if len(sys.argv) > 0:
    for obj in getInstanceObjects():
        print obj['id']
        

