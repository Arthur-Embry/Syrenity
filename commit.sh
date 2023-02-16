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


# read the file into a string
string=$(cat app.env)


# set the delimiter to a newline character
IFS=$'\n'

# use command substitution to insert the string into the array
array=$(echo "$string")

# restore the default IFS value
unset IFS

#concatenate the array into a string with , as a separator
string=$(printf ",%s" "${array[@]}")


# output the string
echo "$string"

#set secret to the string
gh secret set APP_ENV -b "$string" &> /dev/null

# Add all changes to the Git index
git add .

# Commit the changes with the provided message
git commit -m "$message"

# Push the changes to the remote repository
git push