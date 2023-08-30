#!/bin/bash

# Check if the user has provided a version and commit hash
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: deploy.sh <version> <commit hash>"
  exit 1
fi

# Get the version and commit hash from the user
version=$1
commit_hash=$2

# Build the Docker image
docker build -t my-chatapp:${version} .

# Tag the Docker image with the commit hash
docker tag my-chatapp:${version} my-chatapp:${commit_hash}


# Push the Docker image to GitHub Container Registry
echo "Pushing Docker image to GitHub Container Registry..."
docker push my-chatapp:${version}
docker push my-chatapp:${commit_hash}

echo "Done!"
