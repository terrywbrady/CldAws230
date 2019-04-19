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

To run the image (Linux/MacOS)
```
docker run --rm -it terrywbrady/cldaws230week3
```

To run the image (Windows Git-Bash)
```
winpty docker run --rm -it terrywbrady/cldaws230week3
```

To run the image with a custom message (Linux/MacOS)
```
docker run --rm -it terrywbrady/cldaws230week3 Your Custom Message
```
To run the image with a custom message (Windows Git-Bash)

```
winpty docker run --rm -it terrywbrady/cldaws230week3 Your Custom Message
```
