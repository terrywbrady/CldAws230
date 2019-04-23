#! /bin/bash
# stream to secure.log to kinesis firehose to S3
# v.0.1 popmario@uw.edu
# run as root
#
# install kinesis-agent
yum install -y aws-kinesis-agent
# declare variables
region="us-west-2"
# turn on log archiver to s3
sed -i 's/"kinesis.endpoint": "",/"kinesis.endpoint": "kinesis.'$region'.amazonaws.com",/g' /etc/aws-kinesis/agent.json
sed -i 's/"firehose.endpoint": ""/"firehose.endpoint": "firehose.'$region'.amazonaws.com"/g' /etc/aws-kinesis/agent.json
# link secure log to what's configured to log to s3 via firehose
ln -s /var/log/secure /tmp/app.log.secure
# ln -s /var/log/messages /tmp/app.log.messages
chmod 644 /var/log/secure
# chmod 644 /var/log/messages
service aws-kinesis-agent start
chkconfig aws-kinesis-agent on
wget -O /tmp/app.log.ip -r http://169.254.169.254/latest/meta-data/public-ipv4
