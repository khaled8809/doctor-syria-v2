#!/bin/bash

# Build the Docker image
docker build -t doctor-syria .

# Tag the image for AWS ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
docker tag doctor-syria:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/doctor-syria:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/doctor-syria:latest

# Update ECS service
aws ecs update-service --cluster doctor-syria-cluster --service doctor-syria-service --force-new-deployment
