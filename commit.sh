#!/bin/bash

# Take the commit message as an argument
message="$1"

# Check if a message was passed
if [ -z "$message" ]; then
  echo "Please provide a commit message."
  exit 1
fi

# Add all changes to the Git index
git add .

# Commit the changes with the provided message
git commit -m "$message"

# Push the changes to the remote repository
git push