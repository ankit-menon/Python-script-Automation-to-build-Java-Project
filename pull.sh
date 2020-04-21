#!/bin/sh

#create a new directory where the perforce depot will be cloned and a workspace will be initialised
echo "lets create a directoy and initialise git"
mkdir workspace
cd workspace

#clone the remote repository.
git p4 clone //streamsDepot/mainline/depot
cd depot
chmod 700 build.sh

#Redirect the changelist to a text file.
p4 changes > changelist.txt

touch output.txt

#redirecting the STDOUT and STDERR logs to a text file and trigger the build.
./build.sh | tee  output.txt




