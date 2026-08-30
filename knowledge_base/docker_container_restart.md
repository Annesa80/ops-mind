# Docker Container Repeatedly Restarting

## Problem

A Docker container repeatedly starts and stops shortly after launch.

A restarting container usually indicates that the main application process is exiting or being terminated.

## Initial Investigation

First check the container status:

docker ps -a

Then inspect the container logs:

docker logs <container_name>

Look for:

- application stack traces
- database connection failures
- missing configuration
- permission errors
- invalid command-line arguments
- port binding errors

## Check the Container Exit Code

Inspect the container:

docker inspect <container_name>

Pay attention to the container exit code.

An exit code of 0 can indicate that the application exited normally, while a non-zero exit code commonly indicates an application failure.

## Common Causes

### Application Failure

The application may be crashing during startup.

Check:

docker logs <container_name>

Look for exceptions, failed dependencies, and configuration errors.

### Missing Environment Variables

Applications commonly require environment variables such as:

DATABASE_URL

API_KEY

PORT

Inspect the configured environment:

docker inspect <container_name>

### Incorrect Port Configuration

The application may listen on one port while Docker publishes another.

For example, if the application listens on port 3000:

docker run -p 8080:3000 application_name

The host port is 8080 while the container port is 3000.

### Container Resource Limits

The process may be terminated because of memory or CPU constraints.

Inspect the container configuration and resource usage.

## Recommended Troubleshooting Order

1. Check container status.
2. Read container logs.
3. Inspect the exit code.
4. Verify environment variables.
5. Verify port configuration.
6. Check resource limits.
7. Reproduce the application failure outside Docker if possible.

## Useful Commands

List containers:

docker ps -a

View logs:

docker logs <container_name>

Inspect configuration:

docker inspect <container_name>

Restart container:

docker restart <container_name>