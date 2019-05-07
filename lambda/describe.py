import boto3
region = 'us-west-2'
ec2 = boto3.client('ec2', region_name=region)
reservations = ec2.describe_instances()
for res in reservations['Reservations']:
    for instance in res['Instances']:
        id = instance['InstanceId']
        name = ""
        dns = instance['PublicDnsName'] if 'PublicDnsName' in instance else ""
        if 'Tags' in instance:
            tags = instance['Tags']
            for tag in tags:
                if tag['Key'] == 'Name':
                    name = tag['Value']
        print id + "\t" + name + "\t" + dns
        for key in instance.keys():
            print "\t- " + key
print "hi"
