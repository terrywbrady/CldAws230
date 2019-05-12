## get PRs

# https://developer.github.com/v3/pulls/#list-pull-requests

#- open pulls are grabbed by default
#- should the base url be pulled
#- should branch be inferred from pull?

#https://api.github.com/repos/DSpace/DSpace/pulls

import boto3
import urllib2
import json
req = urllib2.Request('https://api.github.com/repos/DSpace/DSpace/pulls')
req.add_header('accept', 'application/json')
response = urllib2.urlopen(req)
jsondata = json.load(response)
print str(jsondata)
