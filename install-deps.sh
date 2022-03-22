#!/bin/bash

# This scripts install the dependencies needed to run Cellenics by Biomage and clones the repositories.


# log outputs the provided string with a timestamp
log() {
	d=$(date "+%Y-%m-%d %H:%M:%S")
	printf "$d $1$2$3"
}

# color variables.
red="\033[31m"
green="\033[32m"
yellow="\033[33m"
blue="\033[34m"
reset="\033[0;m"


# Install docker
log "checking for docker:"
command -v docker > /dev/null 2>&1
if [ $? -eq 0 ]; then
	printf "$green ok$reset\n"
else
	printf "$red not found, please install:$reset\n"
	# the following line is not working
	log "\tcurl -o ~/Downloads/Docker.dmg https://download.docker.com/mac/stable/Docker.dmg && open ~/Downloads/Docker.dmg\n"
	log "\n"
	exit 1
fi

# Install Git
log "checking for git:"
command -v git > /dev/null 2>&1
if [ $? -eq 0 ]; then
	printf "$green exists$reset\n"
else
	printf " does not exist, installing"
	brew install git > /dev/null 2>&1
	if [ $? -eq 0 ]; then
		printf "$green ok$reset\n"
	else
		printf "$red failed with code $?$reset\n"
		exit 1
	fi
fi

# Install NPM.
log "checking for NPM:"
command -v "npm" > /dev/null 2>&1
if [ $? -eq 0 ]; then
	printf "$green exists$reset\n"
else
	printf " does not exist, installing"
	brew install npm > /dev/null 2>&1
	if [ $? -eq 0 ]; then
		printf "$green ok$reset\n"
	else
		printf "$red failed with code $?$reset\n"
		exit 1
	fi
fi


# Install and configure aws-cli
log "checking for aws-cli:"
command -v "aws" > /dev/null 2>&1
if [ $? -eq 0 ]; then
	printf "$green exists$reset\n"
else
	printf " does not exist, installing"
	curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
	sudo installer -pkg AWSCLIV2.pkg -target /
	if [ $? -eq 0 ]; then
		printf "$green ok$reset\n"
	else
		printf "$red failed with code $?$reset\n"
		exit 1
	fi
fi

log "configuring aws-cli \n"

log "-------------------\n"
log "before running:\n"
log "make sure that you have an AWS console account, you will need you access key & secret access key\n"
log "if you don't have an aws account, you can use the mock credentials from aws set-up tutorial provided below"
log "when prompted set the following field values:\n"
log " * access key id: AKIAIOSFODNN7EXAMPLE\n"
log " * secret access key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY\n"
log " * region: eu-west-1\n"
log " * output format is: json\n"
log "press enter to continue\n"
log "-------------------\n"
read ok

# Configure aws-cli
aws configure
if [ $? -eq 0 ]; then
	printf "$green ok$reset\n"
else
	printf "$red failed with code $?$reset\n"
	exit 1
fi

# Clone biomage repositories
DEFAULT_BIOMAGE_HOME=${HOME}/github.com/hms-dbmi-cellenics/
BASE_REPO_SSH="git@github.com:hms-dbmi-cellenics"

printf "Enter desired path for biomage repositories [default: ${DEFAULT_BIOMAGE_HOME}]:\n"
read biomage_home

if [ "${biomage_home}" == "" ]; then
	biomage_home=${DEFAULT_BIOMAGE_HOME}
fi

mkdir -p ${biomage_home}
prev=$(pwd)
cd ${biomage_home}

printf "Cloning repositories into: %"
for repo in iac ui api developer-docs worker data-ingest pipeline inframock biomage-utils roadmap; do
 	git clone "${BASE_REPO_SSH}/${repo}" "${biomage_home}/${repo}"
done

cd ${prev}