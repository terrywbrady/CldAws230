#### C6 Lambda: Start Running Instance
- Verify that no more than N-1 instances are running
  - Where will N be set and managed?
  - Provide cost estimate for N
- Create EC2 from AMI, pass runtime config details (branch, PR, other config)
- What is the right mechanism to pass this in?
  - Tags
  - Dynamo DB
  - Something else in the instance object?
- What is the right mechanism to program auto-stop the Instance
  - Should this be set within the AWS instance?
  - Should a kill trigger be set in the OS (not preferred)
  - Should this be externally controlled by another AWS service?
    - Call Component C7 via a scheduled lambda execution


import boto3
import base64
# Enter the region your instances are in. Include only the region without specifying Availability Zone; e.g.; 'us-east-1'
region = 'us-west-2'
# Enter your instances here: ex. ['X-XXXXXXXX', 'X-XXXXXXXX']
ami = "ami-01861f340864168b2" #dspace-source
tags = [
    {
        'Key':'DSpace',
        'Value':'DSpace'
    },
    {
        'Key':'Name',
        'Value':'MyDSpaceProject'
    }
]

userdata="""
    #!/bin/bash
    sudo su -l ec2-user -c 'cd;cd DSpace-Docker-Images;git pull origin;cd docker-compose-files/dspace-compose;docker-compose -p d6 -f docker-compose.yml -f d6.override.yml up -d'
"""
userdata=base64.b64encode(userdata)

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name=region)
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.create_instances
    # https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html
    instances = ec2.run_instances(
        MaxCount=1,
        MinCount=1,
        ImageId=ami,
        InstanceType='t2.large',
        UserData=userdata
    )
    print 'started your instances: ' + str(instances)
    ids=[]
    for instance in instances:
        ids[0]=instance.id
    ec2.create_tags(Resources=ids,Tags=tags)

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "ec2:Describe*",
                "ec2:Start*",
                "ec2:RunInstances",
                "ec2:Stop*"
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor2",
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "arn:aws:logs:*:*:*"
        }
    ]
}