## CldAws230 Project Idea

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

### Note

Since the project requirements necessitate moving an application between regions, I imagine that target deployment server could be migrated between regions.  The deployment region could be a choice made in the initial user interface.
