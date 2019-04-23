Startup Data

```
#! /bin/bash
# 
# bootstrap userdata for ec2 to access codecommit
# to be used to git additional startup scripts
# and bootstrapping v1.0 by popmario@uw.edu
#
# first install git
yum install -y git

runuser -l ec2-user -c 'git clone https://github.com/terrywbrady/CldAws230.git -b week4'
cd /home/ec2-user/CldAws230
runuser -l ec2-user -c 'chmod 755 kinesis.sh'
runuser -l ec2-user -c './kinesis.sh'
```
