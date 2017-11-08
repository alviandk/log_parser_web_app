# Log Parser Web App
> Log Parser with python running on Flask.

The flask app which parses the log and shows information about SQLi, 
remote file inclusion and web shells attacks.
Some Features Including:
- list of unique IP addresses
- list of unique IP addresses with country and number of hits
- list of all activity per IP address (can be filtered by this IP)
- detect SQLi with found entries
- detect remote file inclusion with found entries
- detect web shells with found entries

## Development setup

To running up this app with docker, you need list of these to be installed
on your computer:
- docker ([docker-installation])
- docker-machine ([docker-machine-instalation])
- docker-compose ([docker-compose-instalation])


## Installation
Installation process:
- clone this repo
- from terminal, change to this root app folder
- creating docker machine: 
```sh
docker-machine create -d virtualbox flask-dev
```
- check the installed docker machine:
```sh
eval "$(docker-machine env dev)"
```
- build the app with docker-compose:
```sh
docker-compose build
```
- running up the app:
```sh
docker-compose up -d
```
(The -d flag is used to run the containers in the background)
- get the ip of docker-machine:
```sh
docker-machine ip dev
```
- visit the ip on the browser with addition port number :5001 (http://ip-of-docker-machine:5001)

## Development Guide
- When you restart the computer you need to make sure that the docker-machine is running up.
To check it use command: `docker-machine ls`. Check if flask-dev state is running.
- If it's not running, run the command `docker-machine start flask-dev`
- When you make a change on the code, you need to rebuild with command: 
`docker-compose up -d --build`.
- get the ip of docker-machine (see the last two points of installation guide) and visit.
   
## User Guide

A few motivating and useful examples of how your product can be used. Spice this up with code 
blocks and potentially more screenshots.

_For more examples and usage, please refer to the [Wiki][wiki]._

[docker-installation]: https://docs.docker.com/engine/installation/
[docker-machine-instalation]: https://docs.docker.com/machine/install-machine/
[docker-compose-instalation]: https://docs.docker.com/compose/install/
