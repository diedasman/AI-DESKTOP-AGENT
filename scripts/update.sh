#!/bin/bash

# Navigate to project directory
cd ~/AI-DESKTOP-AGENT || exit 1

echo "Resetting local changes and syncing with GitHub..."

# Reset tracked files to match remote
git fetch origin
git reset --hard origin/master

# Clean untracked files/folders, but **exclude 'chats/'**
# The -e option tells git clean to exclude paths
git clean -fd -e chats/

echo "Pulling the latest version from GitHub..."
git pull origin master

echo "Update complete! You can now run the agent with './run.sh'."