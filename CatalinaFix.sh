#!/bin/bash

clear

echo This script will run 'sudo codesign --sign - --force --deep resources/bin/*' for each binary, except Futurerestore
echo This will allow Vieux to run the binaries when needed and prevent errors from occuring
echo Only run this if you are on Catalina and are having issues!
echo This script will ask for your password in order to run the commands, this is not stored anywhere. You can check the contents of the script with "cat CatalinaFix.sh" to verify this.

echo 

sudo codesign --sign - --force --deep resources/bin/tsschecker

echo 

sudo codesign --sign - --force --deep resources/bin/igetnonce

echo 

sudo codesign --sign - --force --deep resources/bin/irecovery

echo 
echo Done!
echo If you are still having the same issues after running this script then please refer to https://github.com/MatthewPierson/Vieux#macos-catalina-security-issues for an alternative fix

