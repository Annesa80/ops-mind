# Docker Image Build Failures

## Problem

A Docker image fails to build.

Typical errors include:

- package installation failure
- missing files
- invalid Dockerfile instructions
- dependency conflicts
- permission errors
- network failures while downloading packages

## Inspect the Build Output

Run:

docker build -t application_name .

Read the build output carefully.

Identify the exact Dockerfile step that failed.

## Missing Files

A build may fail if a file referenced by COPY does not exist in the build context.

For example:

COPY requirements.txt /app/

If requirements.txt is not inside the build context, Docker cannot copy it.

## Incorrect Build Context

The final argument to docker build determines the build context.

Example:

docker build -t application_name .

The current directory is the build context.

Files outside the build context generally cannot be copied into the image.

## Dependency Installation Failure

Python applications may fail during:

pip install -r requirements.txt

Node applications may fail during:

npm install

Check whether the package version exists and whether the base image contains the required runtime.

## Permission Problems

Applications may fail during image creation when files cannot be written.

Review the user configured in the Dockerfile and the permissions of copied files.

## Troubleshooting Order

1. Identify the failing Dockerfile instruction.
2. Verify the build context.
3. Check referenced files.
4. Check dependency versions.
5. Check network connectivity.
6. Check file permissions.
