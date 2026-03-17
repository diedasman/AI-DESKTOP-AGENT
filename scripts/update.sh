#!/bin/bash

cd ~/AI-DESKTOP-AGENT || exit 1

# Make sure scripts are executable
chmod +x scripts/run.sh 
chmod +x scripts/update.sh

echo "Resetting local changes and syncing with GitHub..."

git fetch origin
git reset --hard origin/master
git clean -fd -e chats/

git pull origin master

echo "Update complete! 'chats/' folder preserved and scripts are executable."
echo "Starting the agent..."
./scripts/run.sh