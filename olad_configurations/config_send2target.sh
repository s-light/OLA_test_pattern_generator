#!/bin/bash

rootfs=~/mydata/acme/arietta/debian_8.10_jessie/target-rootfs
remote_target_config="$rootfs/home/light/.ola/"


LIME='\033[1;32m'
# No Color
NC='\033[0m'

# update local
echo -e "${LIME}update local host config${NC}"
cp -v $1host_config/* ~/.ola/
echo -e "${LIME}update local target rootfs${NC}"
cp -v $1target_config/* $remote_target_config

# copy to remote device
echo -e "${LIME}copy to remote target${NC}"
scp -v $remote_target_config* "light@arietta.local:/home/light/.ola/"
echo -e "${LIME}done :-)${NC}"
