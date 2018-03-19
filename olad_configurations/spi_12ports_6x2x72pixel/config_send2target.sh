#!/bin/bash

rootfs=~/mydata/acme/arietta/debian_8.10_jessie/target-rootfs
target_config="$rootfs/home/light/.ola/"

# update local image
echo "update local target rootfs"
cp target_config/* $target_config

# copy to remote device
echo "copy to remote target"
scp -v $target_config* "light@arietta.local:/home/light/.ola/"
