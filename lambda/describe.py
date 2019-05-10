import boto3
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

for res in reservations['Reservations']:
    for instance in res['Instances']:
        tags = instance['Tags']
        obj = { 
            'found': 1,
            'name': tags['Name'] if 'Name' in tags else "",
            'id': instance['InstanceId'],
            'state': instance['State']['Name'],
            'dns': instance['PublicDnsName'] if 'PublicDnsName' in instance else ""
        }
        fres.append(obj)

        for key in instance.keys():
            print "\t- " + key

for f in fres:
    print str(f)
    
print "--- describe done"
