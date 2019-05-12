## get PRs

# https://developer.github.com/v3/pulls/#list-pull-requests

#- open pulls are grabbed by default
#- should the base url be pulled
#- should branch be inferred from pull?

#https://api.github.com/repos/DSpace/DSpace/pulls

import boto3
import urllib2
import json

def getPRs():
    req = urllib2.Request('https://api.github.com/repos/DSpace/DSpace/pulls?base=dspace-6_x')
    req.add_header('accept', 'application/json')
    response = urllib2.urlopen(req)
    jsondata = json.load(response)
    
    prs = []
    for pr in jsondata:
        prs.append({
            'url': pr['url'],
            'state': pr['state'],
            'title': pr['title'],
            'base': pr['base']['ref'],
        })
    return prs

def lambda_handler(event, context):
    prs = getPRs()
    return {
        'statusCode': 200,
        'body': json.dumps(prs)
    }

prs=getPRs()
for pr in getPRs():
    print pr['url']+" "+pr['base']