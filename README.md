# Learning Docker

- [Container Lifecycle](#container-lifecycle)
- [Running a container](#running-a-container)
- [Stopping a container](#stopping-a-container)
- [Profiling and debugging](#profiling-and-debugging)
- [Exec Command](#exec-command)
- [Image from running container](#image-from-running-container)
- [Networking](#networking)
- [Dockerfile](#dockerfile)
- [Docker Compose](#docker-compose)

## Container Lifecycle

A container can be in one of the following states:

1. Created: Container ready to run for the first time
2. Running
3. Exited: Container has completed the issued command

```sh
# List running containers
docker ps

# List all containers, even the ones that are not running
docker ps [--all/-a]
```

## Running a container

Differences between **create**, **start** and **run** commands

```sh
# Fetches prepares the file system snapshot with all the associated resources to run the container
docker create [image]

# Executes a command in the previously created/stopped container
# The -a option attaches the container output to the termninal
docker start -a [container]

# Executes a command in a new container, given the specified image. It is like create + start
docker run [image]
```

**Common arguments passed when running a container**

```sh
# -it: Creates a pseudo terminal that allows comminucation between the host and the container.
# --name name: Gives a name to the container about to get created
# --rm: This instructs Docker to remove the stopped container from the container registry
# -p <host_port>:<container_port>: This maps the host with the container ports. If the host port is not provided it will get 1 randomly
# -d: Runs the container in the background
# -e: Set environment variables
# --net network_name: connects the container to the specified network
# --restart: Sets the restart rule. "No" by default, you can limit the number of times it restarts too.
# -v [src-path]:[dest-path]: Mounts a volume that helps bypassing the Union file system allowing to share files between the host and the container. The paths must be absolute or you can use $PWD for the src-path. This is perfect for development mode.
docker container run -it --name <name> --rm -p <host port>:<container port> -d -e ENV=value <image name> --restart on-failure
```
**Note**: You cannot use the --rm and the --restart flag at the same time

## Stopping a container

Docker uses [signals](https://en.wikipedia.org/wiki/Signal_(IPC)) to stop running containers

```sh
# Sends a SIGTERM signal: if handled by the process, it can do a clean up and give it time to shut down
docker stop [container]

# Sends a SIGKILL signal: forces a process to terminate immediately
docker kill [container]

# Remove all stopped containers along with unused networks, dangling images and build cache
docker system prune
```

## Profiling and debugging

Logs:

```sh
# Get all the output logged by the specified container
# You can follow the logs as they come in by adding the follow argument
docker logs [container] [-f/--follow]

# Stats about network and memory usage
docker stats [container]
```

## Exec Command

Execute commands inside a running container

```sh
# Lets you run commands inside a running container
docker exec [options] [container] [command]

# Examples:
# Will use an interactive terminal to traverse the container file system
docker container exec -it web1 sh
# Runs Redis CLI
docker container exec -it local_redis redis-cli
```

If you have a mounted volume and you create a file in the container it might get copied to the docker host. If this happens and you're Running Linux check if the owner of the file in the Docker host is the root. If that's the case, then use the `--user $(id -u):$(id -g)` flag in the exec command to use the current logged in user instead of root

## Image from running container

Althought not widely used, it is possible to create an image based on a running container. As an example:

```sh
# To start an alpine container, attach the terminal and run the shell
docker run -it alpine:latest sh

# Inside the running container
apk add --update redis

# Using another terminal
docker commit -c 'CMD ["redis-server"]' [container] # MacOS/Linux
docker commit -c 'CMD "redis-server"' [container] # Windows

# Creates and starts a new container from the new image
docker run [image]
```

## Networking

Docker networks enable the connection between docker containers and services using a drivers subsystem. To list the available drivers use `docker network ls`. By default this list includes:
- Bridge: This is the default network driver where standalone containers get attached to so they can communicate with each other. You can check the container IP address by using the command `docker container exec <container_name> ifconfig`.
- Host: Use this to isolate the container and use the host's networking directly
- None: Diasbles the networking for the specified containers

To create a new network bridge driver: `docker network create --driver bridge <name>`

## Dockerfile

A Dockerfile is a configuration file which defines how a container should behave. Every Dockerfile should:
1. Specify a base image
2. Run commands to add dependencies
3. Specify the startup command

See [dockerfile reference](https://docs.docker.com/engine/reference/builder/)

```sh
# Command used to create an image out of a Dockerfile
# Tag an image to avoid using the auto generated id
docker build [build context / path] -t [dockerId/project:version]

# Example
docker build . -t [my_id/my_app:latest]

```

Behind the scenes, Docker downloads the base image. It then creates temporary continers (files system snapshots) for each build step. It then saves a final image containing everything and sets the primary command to run upon start.

```Dockerfile
# A dockerfile always has to start with a FROM command that basically imports a base image that can be another docker image or one you create from scratch.
FROM [image]

# Lets you run Linux commands like **cd, mkdir, cp**
RUN [command]

# Sets the working directory to the one you choose so you don't have to keep cd'ing into it
WORKDIR [path]

# Adds labels to the docker image
LABEL [key=value]

# Copy files from the host to the docker image
COPY [path/build context] [path in container]

# This is normally the command used to execute the app.
CMD [command]
```

## Docker Compose

Docker compose is used to start multiple contauners at the same time. Among other things, it helps us by making network communication between components easier and automates some of the long commands and arguments we pass to `docker run` normally. See [docker compose reference](https://docs.docker.com/compose/compose-file/)

**Commands**

```sh
# docker run equivalent
# -d: Detaches the terminal when running the containers
# -f: path to docker-compose file
docker-compose -f [path] up -d

# docker stop equivalent
docker-compose down

# docker ps equivalent, but it only shows the containers related to the docker-compose file
docker-compose ps
```