# Docker Networking and Connection Problems

## Problem

An application running inside Docker cannot connect to another service.

Typical symptoms include:

- connection refused
- connection timeout
- host not found
- failed database connection
- failed API connection

## Container-to-Container Communication

Containers on the same Docker network can communicate using container or service names.

For example:

DATABASE_HOST=postgres

The application should not normally use localhost to reach another container.

Inside a container, localhost refers to the current container.

## Check Docker Networks

List available networks:

docker network ls

Inspect a network:

docker network inspect <network_name>

Verify that the expected containers are connected to the same network.

## Common Cause: Using localhost

Suppose an application container connects to:

localhost:5432

If PostgreSQL is running in another container, this configuration is usually incorrect.

The application should instead use the PostgreSQL container or service name.

Example:

postgres:5432

## Common Cause: Incorrect Published Port

Published ports are primarily used to expose container services to the host.

For example:

docker run -p 8080:3000 application

The application listens on port 3000 inside the container.

The host accesses it through port 8080.

Container-to-container communication normally uses the container's internal port rather than the host's published port.

## Troubleshooting

1. Check that both containers are running.
2. Check that both containers share a Docker network.
3. Verify the hostname.
4. Verify the internal service port.
5. Check application configuration.
6. Inspect container logs.

Useful commands:

docker ps

docker network ls

docker network inspect <network_name>

docker logs <container_name>
