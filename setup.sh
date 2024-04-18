#!/bin/bash

# Install Hasura DDN CLI
curl -L https://graphql-engine-cdn.hasura.io/ddn/cli/v1/get.sh | bash

# Prompt for Personal Access Token (PAT)
read -p "Please enter your Personal Access Token (PAT): " pat

# Login using PAT
echo "Logging in using PAT..."
ddn login --pat $pat

# Ask if the user wants to create a new project
read -p "Do you want to create a new project? (yes/no): " createProject

if [[ "$createProject" == "yes" ]]; then
  echo "Creating a new project..."
  ddn create project --dir .
fi
