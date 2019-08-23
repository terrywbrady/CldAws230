## EC2 Bootstrap Files

The files in this directory are designed to create an AWS AMI that is bootstrapped with the following components
- Docker
- Docker Compose
- Base images used in DSpace Docker Image Builds

EC2 instances used in DSpace Testing will be built from this AMI.

The AMI created with this Cloud Formation script should be logged in an AWS SSM Parameter.

The AMI should be re-created periodically to minimize the number of updates that need to be installed as EC2 instances are created.
