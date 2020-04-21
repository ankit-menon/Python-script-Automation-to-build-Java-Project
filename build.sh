#!/bin/sh

#This is the shell script that would compile and build the java project.
#Will Generate the .Jar fule in the Target folder of the Project Workspace.

file="jb-hello-world-maven-0.1.0.jar"

Echo "lets build this java project"

#Maven Command to build and generate the .jar file
mvn -X package

#lets check the artifact in the Target folder
cd target/

ls -ltr 

#This block will check for the jar file in the target folder and print "not found" in case the jar is not present

if [ ! -f "$file" ]
then
    echo "$0: File '${file}' not found."
fi

