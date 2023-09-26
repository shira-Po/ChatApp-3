#!/bin/bash

# Check if the user has provided a version
if [ -z "$1" ]; then
  echo "Usage: deploy.sh <version>"
  exit 1
fi

# Get the version
version=$1

# Check if the Docker image exists
if docker image inspect my-chatapp:${version} > /dev/null 2>&1; then
  # The Docker image exists
  echo "The Docker image my-chatapp:${version} already exists."

  read -p "Do you want to push the image to Artifact Registry? (y/n) " push_to_artifact_registry

  if [[ "$push_to_artifact_registry" == "y" ]]; then
    # Impersonate the artifact-admin-sa service account
    gcloud auth activate-service-account artifact-admin-sa@grunitech-mid-project.iam.gserviceaccount.com

    # Configure Docker to use Artifact Registry
    gcloud auth configure-docker me-west1-docker.pkg.dev

    # Tag the image with the Artifact Registry repository URI
    docker tag my-chatapp:${version} me-west1-docker.pkg.dev/grunitech-mid-project/shira-polak-chat-app-images/my-chatapp:${version}

    # Push the image to Artifact Registry
    docker push me-west1-docker.pkg.dev/grunitech-mid-project/shira-polak-chat-app-images/my-chatapp:${version}
  fi
else
  # The Docker image does not exist
  echo "The Docker image my-chatapp:${version} does not exist."

  # Build the Docker image
  docker build -t my-chatapp:${version} .

  read -p "Do you want to push the image to Artifact Registry? (y/n) " push_to_artifact_registry

  if [[ "$push_to_artifact_registry" == "y" ]]; then
    # Impersonate the artifact-admin-sa service account
    gcloud auth activate-service-account artifact-admin-sa@grunitech-mid-project.iam.gserviceaccount.com

    # Configure Docker to use Artifact Registry
    gcloud auth configure-docker me-west1-docker.pkg.dev

    # Tag the image with the Artifact Registry repository URI
    docker tag my-chatapp:${version} me-west1-docker.pkg.dev/grunitech-mid-project/shira-polak-chat-app-images/my-chatapp:${version}

    # Push the image to Artifact Registry
    docker push me-west1-docker.pkg.dev/grunitech-mid-project/shira-polak-chat-app-images/my-chatapp:${version}
  fi
fi
