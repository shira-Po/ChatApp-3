#!/bin/bash

# Check if the user has provided a version and commit hash
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: deploy.sh <version> <commit hash>"
  exit 1
fi

# Get the version and commit hash from the user
version=$1
commit_hash=$2

# Check if the Docker image exists
if docker image inspect my-chatapp:${version} > /dev/null 2>&1; then
  # The Docker image exists
  echo "The Docker image my-chatapp:${version} already exists."
  read -p "Do you want to rebuild the image? (y/n) " rebuild

  if [[ "$rebuild" == "y" ]]; then
    # Delete the existing Docker image
    docker rmi my-chatapp:${version}

    # Build the Docker image
    docker build -t my-chatapp:${version} .
  fi
else
  # The Docker image does not exist
  echo "The Docker image my-chatapp:${version} does not exist."

  # Build the Docker image
  docker build -t my-chatapp:${version} .
fi

# Check if the Docker build was successful
if [ $? -ne 0 ]; then
  echo "Docker build failed"
  exit 1
fi

# Push the Docker image to GitHub Container Registry
echo "Pushing Docker image to GitHub Container Registry..."
docker push my-chatapp:${version}

# Tag the Docker image with the commit hash
docker tag my-chatapp:${version} my-chatapp:${commit_hash}


# Check if the Docker push was successful
if [ $? -ne 0 ]; then
  echo "Docker push failed"
  exit 1
fi

# Push to GitHub
git tag ${version}
git push origin ${version}

# Check if the Git push was successful
if [ $? -ne 0 ]; then
  echo "Git push failed"
  exit 1
fi

echo "Done!"
