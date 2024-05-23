# Announcements
# Introduction

DeepRacer Usage Monitor is a lambda function that can be used by teams to monitor their costs and terminate any runaway training sessions.


# How to setup


# Features

## Completed
- Kill EC2 jobs running more than 4 hours based on stack name maching in DDB table per team refrence table


## In Progress
- Log the EC2 run times in DDB per day
- Kill EC2 jobs running more than 80 hours per month per team using DDB reference table , daily hour log and SSM param with max number of hours per month per team
- Find out a way to kill any Model training Job running through Deepracer service in AWS console. We want to rollout this feature after 2-3 week so everyone is using EC2 based training.

## Backlog


# Additional Documentation.


## Docker instructions
```shell
cd .devcontainer
docker image build -t devcontainer:latest .
cd ../
docker container run -v "$(pwd):/code" --name devcont -it devcontainer:latest /bin/zsh 

## reattach to topped container
docker start devcont
docker exec -it devcont /bin/zsh
```