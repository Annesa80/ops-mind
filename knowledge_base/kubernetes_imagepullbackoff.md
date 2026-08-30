# Kubernetes ImagePullBackOff

## Problem

A pod cannot start because Kubernetes cannot obtain the container image.

The pod may display:

ImagePullBackOff

or:

ErrImagePull

## First Investigation

Check the pod:

kubectl get pods

Describe it:

kubectl describe pod <pod_name>

Look at the Events section for image-related errors.

## Common Causes

### Incorrect Image Name

The image name or tag may be incorrect.

Example:

myregistry/application:v2

If that tag does not exist, Kubernetes cannot pull it.

### Private Registry Authentication

The registry may require authentication.

Check whether the pod has the appropriate imagePullSecrets.

### Registry Connectivity

The Kubernetes node may not be able to reach the registry.

Possible causes include:

- DNS problems
- firewall rules
- network restrictions
- registry outage

### Image Tag Does Not Exist

The deployment may reference a tag that was never pushed.

Verify the image in the container registry.

## Troubleshooting Order

1. Check pod events.
2. Verify image name.
3. Verify image tag.
4. Verify registry authentication.
5. Check node connectivity.
6. Verify that the image exists in the registry.

Useful commands:

kubectl describe pod <pod_name>

kubectl get pod <pod_name> -o yaml
