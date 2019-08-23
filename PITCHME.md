## CldAws230 Final Project
### DSpace Pull Request Deployment Service

Terry Brady

https://github.com/terrywbrady/info

+++

## Goal
[DSpace](https://dspace.org) is an open-source repository platform used by academic libraries and other institutions.
+++

## Goal
Many institutions have very limited developer support.  End users within these institutions have expertise to offer to the project.
+++

## Goal
This project will build an automated system to build and deploy a test instance of DSpace using code from a specific [pull request](https://github.com/DSpace/DSpace/pulls).
+++

## Goal
The system will carefully manage deployed instances in order to control costs.

+++
![Video](https://www.youtube.com/embed/lQp_G9A9uL0)
---

## Services Used
- AWS Cloud Formation
- S3
- EC2
- Lambda
- API Gateway
- Cloud Watch Rule
- System Manager (SSM) Parameter Store

+++
## Non AWS Services
- GitHub API
- Docker
- Docker Compose (launching DSpace)

---?image=presentation/CldAws230-Drawing.jpg

---
## Security and Cost Considerations

- Cost
- Security

+++

## Cost Management

- DSpace requires an m2.large or larger EC2 instance (SSM Param)
- The system will cap the number of instances that can be started at once (SSM Param)
- The system will set an expiration time on each instance (SSM Param)
- A Cloud Watch Rule + Lambda will terminate resources that have exceeded uptime

+++

## Security - Potential Enhancements

- Web resources
- Lambdas
- CORS Headers
- EC2 Ports

+++
## Security - Public Web Resources

- EC2 resources will be publicly accessible (for end users)
  - The dashboard will make test resources accessible
- Lambdas will be publicly accessible
  - The StartInstance lambda can trigger costs
  - Consider limiting access to this resource

+++

## Security - CORS
- CORS resources are wide open
+++

## Security - EC2 Ports
- Ports in use
  - DSpace 6: 8080, 3030
  - DSpace 7: 8080, 3030, 3000, 8983
- The ports on the running DSpace instances could be more carefully restricted

---

## Demonstration

- Dashboard (Web App): Start, List, Stop
- DSpace: View default
- Create a DSpace PR
- Deploy PR
- DSpace: View modified version

+++
## A Quick Preview of DSpace

- Navigate to an item
- Items can contain digital media

+++?image=presentation/dspace.gif

+++
## DSpace Instance Manager Dashboard

- Select a DSpace PR
  - Launch instance
- Select a DSpace branch
  - Launch instance

+++?image=presentation/dashboard.gif

+++
## DSpace - Standard Home Page

+++?image=presentation/baseline.png

+++
## Create a [DSpace PR](https://github.com/DSpace/DSpace/pull/2424/files)

+++?image=presentation/pr.png

+++
## DSpace: Demonstrate PR Changes
+++?image=presentation/withPR.png

+++
### Choose Instance from dashboard
- Choose instance without PR changes
- Choose instance with PR changes

+++?image=presentation/dashboard2.gif

---
## Further Enhancements

- Functionality
- AWS Operations

+++

## Additional Functionality

- Make EC2/Docker startup logs accessible
  - Flask on server OR use Kinesis
- Post incremental status updates during startup process
  - Use tag api
- Explore ECS or EKS instead of EC2 for deployment
- Explore code pipeline to build and publish PR images

+++

## AWS Operations - Functionality

- Make logs accessible
- Security enhancments (see earlier slide)
- Regional deployment

+++

## AWS Operations - Portability to another account
- Generate AMI with CloudFormation
- Create Lambda security group with Cloud Formation
- Deploy Lambda and API Gateway with Cloud Formation
- Deploy S3 website with Cloud Formation

---
## References

_Time will not likely permit this level of detail._

- Cloud Formation
- Bootstrap Script
- Lambda Permissions
- Deployment Process
- Lambda Instances
- Lambda GitHub API
- Webapp JavaSciprt

+++
#### Cloud Formation to Create AMI

+++?code=bootstrap/ec2-cloudformation.json&lang=JSON

@[3-7](URL Parameter for startup script)
@[8-21](Other Parameters)
@[29-32](Image Type and Key Name Parameter Ref)
@[34-52](Inject startup script URL into UserData)
@[54-59](Add Name Paremeter to Tags)

+++
#### Bootstrap Script for EC2 that will become an AMI

+++?code=bootstrap/startup.shlang=Bash

@[4-7](Install Java)
@[8-9](Install Git)
@[11-18](Install Docker)
@[20-24](Install Docker Compose)
@[26-27](Pre-load Docker Images)

+++
#### Lambda Permissions

+++?code=lambda/lambdaPerms.json&lang=JSON

@[17-24](EC2 Operations Performed by Lambda)

+++
#### Simple Deployment Process

+++?code=cloud9build.sh&lang=Bash

@[1-6](Prep Resources)
@[7-13](Deploy to S3)
@[15-20](Deploy to Lambda)

+++
#### Lambda Instances

+++?code=lambda/getInstances.py&lang=Python

@[9-18](Read SSM Stored Parameters)
@[20-32](Read SSM Stored Parameters)
@[40-45](Get Instances Lambda -> ec2.describe_instances)
@[106-119](Create Tags)
@[120-128](Create Tags)
@[131-142](Inject UserData)
@[143-152](Inject UserData)
@[153-162](Inject UserData)
@[163-175](Inject UserData)
@[196-197](Check that running instances does not exceed max allowed)
@[199-210](Start Instance Lambda -> ec2.run_instances)
@[242-250](Stop Instance Lambda -> ec2.terminate_instances)
@[261-267](Stop Overtime Instance Lambda -- Cloud Watch Rule)
@[284-296](Filter Running Instances)
@[345-355](CLI testing interface)
@[355-364](CLI testing interface)
@[365-374](CLI testing interface)

+++
#### Lambda GitHub API

+++?code=lambda/getPRs.py&lang=Python

@[25-39](Call GitHub API)
@[41-47](Get PRs Lambda)
@[49-51](CLI Tester)

+++
#### Webapp JavaScript

+++?code=web/dspaceLauncher.js&lang=JavaScript

@[3-11](Load Resources)
@[14-23](Call Get Instances Lambda)
@[44-33](Call Get Instances Lambda)
@[34-43](Call Get Instances Lambda)
@[44-49](Call Get Instances Lambda)
@[53-65](Call Get PRs Lambda)
@[69-71](Call Stop Instance Lambda)
@[75-94](Call Start Instance Lambda)

---

### Thank You

- https://github.com/terrywbrady/Cldaws230
- https://github.com/terrywbrady/info
