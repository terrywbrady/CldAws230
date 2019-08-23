## Lambda code for project

- getinstances.py
  - Manage a set of AWS EC2 Instances used for DSpace Testing (List, Start, Stop, Kill)
- getPRs.py
  - Call the GitHub API to retrieve the most recent list of DSpace Pull Requests 

## API Gateway Config Notes

Each Lambda created from this code will need to be configured through the AWS API Gateway.

The API Gateway configuration has not yet been automated.
