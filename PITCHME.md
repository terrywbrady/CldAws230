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
#### Simple Deployment Process

+++?code=cloud9build.sh
@[10-17](Prep Resources)
@[19-23](Deploy to S3)
@[26-31](Deploy to Lambda)

+++
#### Lambda Instances

+++?code=lambda/getInstances.py
@[16-28](Read SSM Stored Parameters)
@[36-42](Read SSM Stored Parameters)
@[50-55](Get Instances Lambda -> ec2.describe_instances)
@[123-145](Create EC2 Tags)
@[153-164](Construct EC2 UserData - docker compose)
@[166-172](UserData - Set Environment)
@[173-183](UserData - Clone DSpace Code for PR)
@[185-195](UserData - Clone Docker Compose Files)
@[220-222](Check that running instances does not exceed max allowed)
@[202-218](Start Instance Lambda -> ec2.run_instances)
@[280-285](Stop Instance Lambda -> ec2.terminate_instances)
@[298-303](Stop Overtime Instance Lambda -- Cloud Watch Rule)
@[314-326](Filter Running Instances)

+++
#### Lambda GitHub API

+++?code=lambda/getPRs.py
@[17-40](Call GitHub API)
@[42-49](Get PRs Lambda)
@[60-63](CLI Tester)

+++
#### Webapp JavaSciprt

+++?code=web/dspaceLauncher.js
@[7-15](Load Resources)
@[20-26](Call Get Instances Lambda)
@[35-44](Create stop button)
@[46-54](Show table)
@[67-81](Call Get PRs Lambda)
@[86-90](Call Stop Instance Lambda)
@[95-115](Call Start Instance Lambda)

---

### Thank You

- https://github.com/terrywbrady/Cldaws230
- https://github.com/terrywbrady/info
