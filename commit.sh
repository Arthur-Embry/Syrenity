#!/bin/bash

# Take the commit message as an argument
message="$1"

# Check if a message was passed
if [ -z "$message" ]; then
  echo "Please provide a commit message."
  exit 1
fi

# remove all empty lines from app.env
sed -i '/^$/d' app.env

#read all lines of app.env into an array
mapfile -t lines < app.env

#concatenate all lines into a single string with @ as delimiter
string=$(printf "%s@" "${lines[@]}")

#append ^@^ to the string
string="$string^@^"

#set secret to the string
gh secret set APP_ENV -b "$string" &> /dev/null

# Add all changes to the Git index
git add .

# Commit the changes with the provided message
git commit -m "$message"

# Push the changes to the remote repository
git push