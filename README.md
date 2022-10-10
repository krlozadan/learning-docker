# Learning Docker

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

## Common commands to run a container:

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

`docker container run -it --name <name> --rm -p <host port>:<container port> -d -e ENV=value <image name> --restart on-failure`

`-it`: Creates a pseudo terminal that allows comminucation between the host and the container. 
You can use for instance the **Ctrl + C** combo to stop the container

`--name name`: Gives a name to the container about to get created

`--rm`: This instructs Docker to remove the stopped container from the container registry

`-p <host_port>:<container_port>`: This maps the host with the container ports. If the host port is not provided it will get 1 randomly

`-d`: Runs the container in the background

`-e`: Set environment variables

`--net network_name`: 

`--restart`: Sets the restart rule. **No** by default, you can limit the number of times it restarts too. 
**Note:** You cannot use the --rm and the --restart flag at the same time

`-v [src-path]:[dest-path]`: Mounts a volume that helps bypassing the Union file system allowing to share files between the host and the container. The paths must be absolute or you can use $PWD for the src-path. This is perfect for development mode.

## Commands to stop a container

Docker uses [signals](https://en.wikipedia.org/wiki/Signal_(IPC)) to stop running containers

```sh
# Sends a SIGTERM signal: if handled by the process, it can do a clean up and give it time to shut down
docker stop [container]

# Sends a SIGKILL signal: forces a process to terminate immediately
docker kill [container]

# Remove all stopped containers along with unused networks, dangling images and build cache
docker system prune
```

## Profiling and Debugging

Logs:

```sh
# Get all the output logged by the specified container
# You can follow the logs as they come in by adding the follow argument
docker logs [container] [-f/--follow]

# Stats about network and memory usage
docker stats [container]
```

## Execute commands inside a running container

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

## Dockerfile

A dockerfile always has to start with a **FROM** command that basically imports a base image that can be another docker image or one you create from scratch. 

**RUN** lets you run Linux commands like **cd, mkdir, cp**

**WORKDIR** Sets the working directory to the one you choose so you don't have to keep cd'ing into it

**LABEL** Adds labels to the docker image

**CMD** This is normally the command used to execute the app. 

## Network

Docker networks enable the connection between docker containers and services using a drivers subsystem. To list the available drivers use `docker network ls`. By default this list includes: 
- Bridge: This is the default network driver where standalone containers get attached to so they can communicate with each other. You can check the container IP address by using the command `docker container exec <container_name> ifconfig`. 
- Host: Use this to isolate the container and use the host's networking directly
- None: Diasbles the networking for the specified containers

To create a new network bridge driver: `docker network create --driver bridge <name>`