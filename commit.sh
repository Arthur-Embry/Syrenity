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

#add one empty line to the end of app.env
echo "" >> app.env

#set string to empty
string=""

#read all lines from app.env
while read -r line; do
  #set the string to the line
  string_temp="$line"
  #append the string to the string with a ,
  string="$string$string_temp,"
done < app.env

#set secret to the string
gh secret set APP_ENV -b "$string" &> /dev/null

#print the string
echo $string

# Add all changes to the Git index
git add .

# Commit the changes with the provided message
git commit -m "$message"

# Push the changes to the remote repository
git push