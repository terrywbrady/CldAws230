import boto3
from datetime import timedelta
from dateutil import tz

HERE = tz.tzlocal()

region = 'us-west-2'
ec2 = boto3.client('ec2', region_name=region)
reservations = ec2.describe_instances(
    Filters=[
        {
            'Name': 'tag:DSpace',
            'Values': ['DSpace']
        },
    ]
)
fres = []

def getKey(dictname, name, value):
    return dictname[name] if name in dictname else value 

for res in reservations['Reservations']:
    for instance in res['Instances']:
        tags = instance['Tags']
        obj = { 
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
        fres.append(obj)

        for key in instance.keys():
            print "\t- " + key

for f in fres:
    print str(f)
    
print "--- describe done"
