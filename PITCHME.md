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
Ths project will build an automated system to build an deploy a test instance of DSpace using code from a specific [pull request](https://github.com/DSpace/DSpace/pulls).
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

## Security - Public Web Resources

- EC2 resources will be publicly accessible (for end users)
  - The dashboard will make test resources accessible
- Lambdas will be publicly accessible
  - The StartInstance lambda could trigger a costly resources
  - Perhaps some additional verification could be added here

+++

## Security - CORS
- CORS resources are wide open
+++

## Security - EC2 Ports
- The ports on the running DSpace instances could be more carefully restricted

+++

## Security - Keyfile

- A specifically named keyfile is specified on startup.  
- While the file is not exposed, a more elegant approach is needed

---

## Demonstration

- Dashboard (Web App): Start, List, Stop
- DSpace: View default
- Create a DSpace PR
- Deploy PR
- DSpace: View modified version

+++
## A Quick Preview of DSpace

+++?image=presentation/dspace.gif

+++
## DSpace Instance Manager Dashboard

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
- Find AMI by tag rather than hard-coding

+++

## AWS Operations - Development

- Automate Lambda Deployment
- Automate S3 Web Resource Deployment

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
- Lambda Instances
- Lambda GitHub API
- Webapp JavaSciprt

+++
#### Cloud Formation to Create AMI

+++?code=bootstrap/ec2-cloudformation.json
@[3-7](URL Parameter for startup script)
@[8-21](Other Parameters)
@[29-32](Image Type and Key Name Parameter Ref)
@[34-52](Inject startup script URL into UserData)
@[54-59](Add Name Paremeter to Tags)

+++
#### Bootstrap Script for EC2 that will become an AMI

+++?code=bootstrap/startup.sh
@[4-7](Install Java)
@[8-9](Install Git)
@[11-18](Install Docker)
@[20-24](Install Docker Compose)
@[26-27](Pre-load Docker Images)

+++
#### Lambda Permissions

+++?code=lambda/lambdaPerms.json
@[17-24](EC2 Operations Performed by Lambda)

+++
#### Lambda Instances

+++?code=lambda/getInstances.py
@[9-18](Read SSM Stored Parameters)
@[20-30](Read SSM Stored Parameters)
@[39-44](Get Instances Lambda -> ec2.describe_instances)
@[109-119](Create Tags)
@[120-131](Create Tags)
@[133-142](Inject UserData)
@[143-152](Inject UserData)
@[153-162](Inject UserData)
@[163-171](Inject UserData)
@[192-193](Check that running instances does not exceed max allowed)
@[195-206](Start Instance Lambda -> ec2.run_instances)
@[238-246](Stop Instance Lambda -> ec2.terminate_instances)
@[257-263](Stop Overtime Instance Lambda -- Cloud Watch Rule)
@[280-292](Filter Running Instances)
@[341-350](CLI testing interface)
@[351-360](CLI testing interface)
@[361-370](CLI testing interface)

+++
#### Lambda GitHub API

+++?code=lambda/getPRs.py
@[25-39](Call GitHub API)
@[41-47](Get PRs Lambda)
@[49-51](CLI Tester)

+++
#### Webapp JavaSciprt

+++?code=web/dspaceLauncher.js
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
