import boto3
import base64
import json

def getAmi():
    return "ami-01861f340864168b2" #dspace-source

def getTags():
    return [
        {
            'Key':'DSpace',
            'Value':'DSpace'
        },
        {
            'Key':'Name',
            'Value':'MyDSpaceProject'
        }
    ]

def getUserData():
    return base64.b64encode("""
    #!/bin/bash
    sudo su -l ec2-user -c 'cd /home/ec2-user/DSpace-Docker-Images'
    sudo su -l ec2-user -c 'git pull origin'
    sudo su -l ec2-user -c 'cd docker-compose-files/dspace-compose'
    sudo su -l ec2-user -c 'docker-compose -p d6 -f docker-compose.yml -f d6.override.yml up -d'
    """)

def getEC2():
    region = 'us-west-2'
    return boto3.client('ec2', region_name=region)

def lambda_handler(event, context):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.create_instances
    # https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html
    ec2 = getEC2()
    instances = ec2.run_instances(
        MaxCount=1,
        MinCount=1,
        ImageId=getAmi(),
        InstanceType='t2.large',
        UserData=getUserData()
    )
    ids=[]
    for instance in instances['Instances']:
        ids.append(instance['InstanceId'])
    ec2.create_tags(Resources=ids,Tags=getTags())
    return {
        'statusCode': 200,
        'body': json.dumps(ids)
    }

lambda_handler([],[])