## CldAws230 Final Project
### DSpace Pull Request Deployment Service

Terry Brady
https://github.com/terrywbrady/info

+++

## Goal
- [DSpace](https://dspace.org) is an open-source repository platform used by academic libraries and other institutions.
- Many institutions have very limited developer support.  End users within these institutions have expertise to offer to the project.
- Ths project will build an automated system to build an deploy a test instance of DSpace using code from a specific [pull request](https://github.com/DSpace/DSpace/pulls).
- The system will carefully manage deployed instances in order to control costs.

---

## Services Used
- AWS Cloud Formation
- S3
- EC2
- Lambda
- API Gateway
- Cloud Watch Rule

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

- DSpace requires an m2.large or larger EC2 instance.
- The system will cap the number of instances that can be started at once.
- The system will set an expiration time on each instance.
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

+++?image=presentation/dspace.gif
## DSpace

+++?image=presentation/dashboard.gif
## DSpace Instance Manager Dashboard


+++?image=presentation/baseline.png
## DSpace Demo

+++?image=presentation/pr.png
## Create a DSpace PR

+++?image=presentation/withPR.png
## DSpace: Demonstrate PR Changes

+++?image=presentation/dashboard2.gif

---
## Further Enhancements

- Functionality
- AWS Operations

+++

## Additional Functionality

- Support all branches of DSpace - customize webapps per branch
- Make EC2/Docker startup logs accessible
- Post incremental status updates during startup process
- Explore ECS or EKS instead of EC2 for deployment
- Explore code pipeline to build and publish PR images

+++

## AWS Operations - Functinality

- Make logs accessible
- Security enhancments (see earlier slide)
- Regional deployment
- Find AMI by tag rather than hard-coding

+++

## AWS Operations - Portability to another account
- Generate AMI with CloudFormation
- Create Lambda security group with Cloud Formation
- Deploy Lambda and API Gateway with Cloud Formation
- Deploy S3 website with Cloud Formation

---
## References

- Cloud Formation
- Bootstrap Script
- Lambda Permissions
- Lambda Instances
- Lambda GitHub API
- Webapp JavaSciprt

+++?code=bootstrap/ec2-cloudformation.json
## Cloud Formation

+++?code=bootstrap/startup.sh
## Bootstrap Script

+++?code=lambda/lambdaPerms.json
## Lambda Permissions

+++?code=lambda/getInstances.py
## Lambda Instances

+++?code=lambda/getBranches.py
## Lambda GitHub API

+++?code=web/dspaceLauncher.js
## Webapp JavaSciprt
