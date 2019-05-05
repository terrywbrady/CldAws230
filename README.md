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

## Design Ideas

### System Components

#### C1 DSpace code
_git repos, docker images, docker compose files_
- All of these resources are open source and downloadable
- https://github.com/DSpace/DSpace
- https://github.com/DSpace-Labs/DSpace-Docker-Images

#### C2 Manually built AMIs containing git, docker, docker-compose
- Create AMI for project
  - [Instance Requirements](https://wiki.duraspace.org/display/~terrywbrady/Create+EC2+for+DSpace+Docker)
  - Create a [Cloud Formation Script](bootstrap/ec2-cloudformation.json) to create a baseline instance for this AMI
  - Create EC2 with [startup script](bootstrap/startup.sh)

#### C3 Managed pool of up to N EC2 instances that will run a specific branch/pr of DSpace within Docker.
- 6G of RAM is needed, so I have been using t2.large instances
- To manage costs for the scope of this project
  - only 2-3 instances will be permitted to be up at a given time
  - servers will only remain "up" for 30 min to 2 hours
- EC2 startup process
_The AMI already provides git, docker, docker-compose, and a cloned repo_
  - Startup script refreshes code, pulls PR, builds image
    - possible extension - publish built image to either Dockerhub or to Amazon image registry
  - Run docker-compose build up
    - with options appropriate to the branch and config
  - Stretch Goal: Direct docker-compose output to CloudWatch logs
    - provide some linkage to instnace name

#### C4 Web App
_This webapp would be available to a pool of power users of the open source system. This will be an experimental application for these users so any authentication process that is necessary will need to be minimal. This portion of the system should err on the side of accessibility over security.  The system will need to mitigate the risk of a malicious user.
- [html, css, js files](web)

##### C4A Web App: Display Running Instances
Using Component C5, list the running instances initiated from the webapp.  Display the following
- Config details used to start each instance
  - branch
  - PR
  - expandable field to show optional config details
- Runtime info
  - instance id
  - DNS
    - URL's to the running applications: DNS + contextual by branch
  - Pre-set shutdown time
  - Stretch Goal: Link to Cloud Watch Logs for instance
    - Display docker-compose output
- Provide a STOP button (maybe)
  - Minimal authentication required
- Provide an EXTEND button to delay shutdown (maybe)
  - Minimal authentication required

##### C4B Web App: Start Instance
Using Component C6, start a new instance
- To launch a new instance
  - Minimal authentication required
- Form Fields (detail below)
  - Cached list of regions with AMI
  - List of branches in DSpace/DSpace (static or dynamic from GitHub API)
  - List of pull requests in DSpace/DSpace (dynamic from DSpace)
    - Can be blank to run the branch unaltered    
  - Possible:
    - ENV variable declarations to pass to docker compose
    - Selectable JSON profiles for more complex docker compose init

#### Lambdas
_In the last class, I used the Java API.  It seems like it would be easier to learn Python and boto3 than to do formal Java builds_

#### C5 Lambda: Get Running Instance Info
- A lambda service will be needed to return information about the running instances
  - Participating instances will be identified by unique tags
  - Tags will contain summary display data about the init configuration
- Code: Implementation in Progress
  - [Lambda Code](lambda/getInstances.py)


#### C6 Lambda: Start Running Instance
- Verify that no more than N-1 instances are running
  - Where will N be set and managed?
  - Provide cost estimate for N
- Create EC2 from AMI, pass runtime config details (branch, PR, other config)
- What is the right mechanism to pass this in?
  - Tags
  - Something else in the instance object?
- What is the right mechanism to program auto-stop the Instance
  - Should this be set within the AWS instance?
  - Should a kill trigger be set in the OS (not preferred)
  - Should this be externally controlled by another AWS service?
    - Call Component C7 via a scheduled lambda execution
- Code: Implementation in Progress
  - [Lambda Code](lambda/startInstance.py)
  - [Lambda Permissions](lambda/lambdaPerms.json)

#### C7 Lambda: Stop Running Instance
Stop an instance freeing up a slot for a new launch

- Code: Not started
  - [Lambda Code](lambda/stopInstance.py)

#### C8 Lambda: Misc Utils
- Code: Not Started
  - [Get PRs](lambda/getPRs.py)
  - [Get Branches](lambda/getBranches.py)
  - [Get Config](lambda/getConfig.py)
