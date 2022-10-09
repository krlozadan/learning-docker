# Learning Docker

## Common commands to run a web application:

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

## Profiling

Logs:
`docker container logs -f <image name>`

`-f`: Get logs in realtime, as they come in

Stats about network and memory usage

`docker container stats <image name>`

## Dockerfile

A dockerfile always has to start with a **FROM** command that basically imports a base image that can be another docker image or one you create from scratch. 

**RUN** lets you run Linux commands like **cd, mkdir, cp**

**WORKDIR** Sets the working directory to the one you choose so you don't have to keep cd'ing into it

**LABEL** Adds labels to the docker image

**CMD** This is normally the command used to execute the app. 

## Exec

`docker container exec [options] [container] [command]` lets you run commands inside a running container. 
Example: `docker container exec -it web1 sh` will use an interactive terminal to traverse the container file system.
If you have a mounted volume and you create a file in the container it might get copied to the docker host. If this happens and you're Running Linux check if the owner of the file in the Docker host is the root. If that's the case, then use the `--user $(id -u):$(id -g)` flag in the exec command to use the current logged in user instead of root

## Network

Docker networks enable the connection between docker containers and services using a drivers subsystem. To list the available drivers use `docker network ls`. By default this list includes: 
- Bridge: This is the default network driver where standalone containers get attached to so they can communicate with each other. You can check the container IP address by using the command `docker container exec <container_name> ifconfig`. 
- Host: Use this to isolate the container and use the host's networking directly
- None: Diasbles the networking for the specified containers

To create a new network bridge driver: `docker network create --driver bridge <name>`