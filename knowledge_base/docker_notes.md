# Docker Troubleshooting Notes

## Container keeps restarting

### Problem

A Docker container repeatedly starts and stops.

This usually means the application inside the container is crashing.

### Common Causes

## 1. Application Error

The application may have an internal error.

Check container logs:

docker logs <container_name>

Look for:
- stack traces
- database connection errors
- missing files
- configuration errors

## 2. Missing Environment Variables

Many applications require environment variables.

Example:

DATABASE_URL
API_KEY
PORT

If these values are missing, the application may fail during startup.

Check environment variables:

docker inspect <container_name>

## 3. Incorrect Port Configuration

The application may listen on a different port than Docker exposes.

Example:

Application:
3000

Docker:
8080

The ports must be mapped correctly.

Example:

docker run -p 8080:3000 application_name

## Useful Docker Commands

List running containers:

docker ps

View logs:

docker logs <container_name>

View container details:

docker inspect <container_name>

Restart container:

docker restart <container_name>

Remove container:

docker rm <container_name>