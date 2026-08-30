# Database Connection Troubleshooting

## Problem

An application cannot connect to its database.

Typical errors include:

- connection refused
- connection timeout
- authentication failed
- host not found
- too many connections

## Step 1 — Verify Database Availability

Determine whether the database service is running.

For a containerized database, check:

docker ps

For Kubernetes:

kubectl get pods

## Step 2 — Verify Host and Port

Check the application's database configuration.

Common settings include:

DATABASE_HOST
DATABASE_PORT
DATABASE_NAME
DATABASE_USER

Make sure the hostname and port match the actual database service.

## Step 3 — Check Network Connectivity

A connection may fail even when the database is running.

Check:

- DNS resolution
- network connectivity
- firewall rules
- Docker networks
- Kubernetes Services

## Step 4 — Check Credentials

Authentication errors may indicate:

- incorrect username
- incorrect password
- expired credentials
- wrong database name

Do not print database passwords in logs.

## Step 5 — Check Connection Limits

The database may reject new connections because the maximum number of connections has been reached.

Inspect database metrics and application connection-pool configuration.

## Common Docker Scenario

If the application and database run in separate Docker containers, the application should normally connect using the database container or service name rather than localhost.

Example:

DATABASE_HOST=postgres

## Common Kubernetes Scenario

If the database is exposed through a Kubernetes Service, verify:

kubectl get services

and confirm the application uses the correct Service hostname and port.

## Troubleshooting Order

1. Verify database availability.
2. Verify hostname and port.
3. Verify network connectivity.
4. Verify credentials.
5. Check database connection limits.
6. Inspect application logs.
