Simple Dockerfile example for CldAWS230 Homework.

Assets
- https://cloud.docker.com/u/terrywbrady/repository/docker/terrywbrady/cldaws230week3
- https://github.com/terrywbrady/CldAws230/blob/week3hw/week3/Dockerfile

## Build

From the directory containing the Dockerfile, use the following to build:
```
docker build -t terrywbrady/cldaws230week3 .
```

## Execution

To run the image
```
docker run --rm --name pip -p 5000:5000 terrywbrady/cldaws230week3
```

## View the results
Open the following link in your browser: http://localhost:5000

To run multiple copies
_I do not understand the suggestion in the assignment about running multiple copies of the application using `docker run`._
