#! /bin/sh

if [ -z "$1" ]
then
    echo "Usage: username. Example Users/johndoe/.config. Enter the johndoe."
    exit -1
fi
cp world_files/problem* /Users/$1/.config/rurple/worlds/samples/.
rm /Users/$1/.config/rurple/worlds/samples/*~