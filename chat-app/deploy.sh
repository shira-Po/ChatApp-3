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

# Check if the Docker build was successful
if [ $? -ne 0 ]; then
  echo "Docker build failed"
  exit 1
fi

# Check if the commit hash exists
if docker image inspect my-chatapp:${commit_hash} > /dev/null 2>&1; then
  # The commit hash exists
  read -p "Do you want to tag and push the image to GitHub? (y/n) " tag_and_push

  if [[ "$tag_and_push" == "y" ]]; then
    # Tag the Docker image with the commit hash
    docker tag my-chatapp:${version} my-chatapp:${commit_hash}

    # Push the Docker image to GitHub Container Registry
    docker push my-chatapp:${commit_hash}

    # Push to GitHub
    git tag ${version}
    git push origin ${version}
  fi
else
  # The commit hash does not exist
  echo "The commit hash my-chatapp:${commit_hash} does not exist."
fi

# Ask the user if they want to push the image to Artifact Registry
read -p "Do you want to push the image to Artifact Registry? (y/n) " push_to_artifact_registry

if [[ "$push_to_artifact_registry" == "y" ]]; then
  # Impersonate the artifact-admin-sa service account
  gcloud auth activate-service-account artifact-admin-sa@grunitech-mid-project.iam.gserviceaccount.com

  # Configure Docker to use the Artifact Registry
  gcloud auth configure-docker me-west1-docker.pkg.dev

  # Tag the image with the Artifact Registry repository URI
  docker tag my-chatapp:${version} me-west1-docker.pkg.dev/grunitech-mid-project/shira-polak-chat-app-images:${version}

  # Push the image to Artifact Registry
  docker push me-west1-docker.pkg.dev/grunitech-mid-project/shira-polak-chat-app-images:${version}
fi
