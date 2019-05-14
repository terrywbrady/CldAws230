## DSpace Launcher Dashboard - Deploy a PR on AWS for Testing

[![Demonstration Video](https://i.ytimg.com/vi/lQp_G9A9uL0/hqdefault.jpg)](https://www.youtube.com/watch?v=lQp_G9A9uL0)

## Class Presentation

- https://gitpitch.com/terrywbrady/CldAws230

## Overview

![Overview](presentation/CldAws230-Drawing.jpg)

### Background

I had the following project in mind when I enrolled in the program, so I would be eager to implement some form of this project.

- I work on an open source system used by academic librarians
  - https://github.com/DSpace/DSpace
- I have Dockerized this application so that it can be run with Docker Compose
  - https://github.com/DSpace-Labs/DSpace-Docker-Images
- My goal is to create a service to make it easier for end users to test and preview the code associated with a pull request.
- If this project is successful, I would like to contribute this effort to the host organization for the DSpace project

### Ideal Goal (Container Service)

Ideally, I would like to launch a working instance of the application in a container managed service (ECS, EKS) on AWS.
I suspect that this 10+ year old application is not ready for such a deployment.  Many initialization tasks must be run through CLI commands within the main application container.

Based on my experience in the program so far, I have created the following instructions for running with Docker on an EC2 instance.
- https://wiki.duraspace.org/display/~terrywbrady/Create+EC2+for+DSpace+Docker

### Compromise Goal (EC2 Deployment with Docker Compose)

Assuming that my suspicion is true that the application is not yet ready for container managed deployment, I would like to create the following application.
- Create web interface that allows a user to select a DSpace pull request (PR) of interest.
- Create an automated build system to merge the code for a specific DSpace PR and publish a docker image for that PR.
- Deploy the newly built docker image in Docker Compose on an EC2 instance.
- Automatically shut down the instance after a prescribed amount of time.
- Some control will be needed to limit the number of active deployments at one time.

## Status
- Week 7
  - Complete Web App
  - Create Presentation
  - Create Summary video
- Week 6
  - [Presentation Template](https://gitpitch.com/terrywbrady/CldAws230)
  - [web page code](web)
    - app is deployable to S3
  - [getInstances.py](lambda/getInstances.py)
    - Initially, I planned to create several different python files, but there is so much shared code between the Lambdas, I decided to keep it all in one module.
    - CLI interface to list, stop, start instances
    - API Gateway resource to list instances
    - API Gateway resource to start an instance
    - API Gateway resource to stop an instance
    - Cloud Watch Rule to stop instances that are over time
- Week 5
  - Initial Code - Start instance from AMI and insert user data
- Week 4
  - Create a [Cloud Formation Script](bootstrap/ec2-cloudformation.json) to create a baseline instance for this AMI
  - Create EC2 with [startup script](bootstrap/startup.sh)
- Prior Weeks
  - Document Design Goals

## Questions
- I have the following system configuration hard-coded into a Lambda. https://github.com/terrywbrady/CldAws230/blob/master/lambda/getInstances.py#L12-L19  These settings are the primary dials that I can use to manage the cost of the application I have created. As I think about this, I wish these values were not in code. I wish that I could set them within a dashboard of some type.
  - Number of EC2 instances to manage
  - EC2 image type to start
