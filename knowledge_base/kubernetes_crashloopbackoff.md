# Kubernetes CrashLoopBackOff

## Problem

A Kubernetes pod repeatedly starts and crashes.

The pod may eventually display:

CrashLoopBackOff

CrashLoopBackOff means Kubernetes is repeatedly restarting a container that has failed.

It does not identify the root cause by itself.

## First Investigation

Check the pod:

kubectl get pods

Describe the pod:

kubectl describe pod <pod_name>

Check current logs:

kubectl logs <pod_name>

If the container has restarted, check logs from the previous instance:

kubectl logs <pod_name> --previous

Previous logs are often useful when the current container has already restarted.

## Common Causes

### Application Crash

The application may terminate because of an unhandled exception or startup failure.

Check:

kubectl logs <pod_name>

### Missing Configuration

The application may require:

- ConfigMap values
- Secrets
- environment variables

Inspect the pod:

kubectl describe pod <pod_name>

### Database Connection Failure

The application may start but fail because it cannot connect to a required database.

Check:

- database hostname
- database port
- credentials
- network connectivity
- database availability

### Resource Limits

A container may be terminated because it exceeds its memory limit.

Check:

kubectl describe pod <pod_name>

Look for termination information indicating an out-of-memory condition.

Resource usage can also be inspected with:

kubectl top pods

## Recommended Troubleshooting Order

1. Check pod status.
2. Read current logs.
3. Read previous container logs.
4. Describe the pod.
5. Check configuration and secrets.
6. Check resource usage.
7. Verify dependencies such as databases.

## Useful Commands

kubectl get pods

kubectl describe pod <pod_name>

kubectl logs <pod_name>

kubectl logs <pod_name> --previous

kubectl top pods
