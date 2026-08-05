# Kubernetes Troubleshooting Notes

## Pod is stuck in CrashLoopBackOff

### Problem

A Kubernetes pod enters CrashLoopBackOff status.

This means the container starts but repeatedly crashes.

### Common Causes

## 1. Application Failure

The application inside the container has an error.

Check logs:

kubectl logs <pod_name>

## 2. Configuration Problem

The application may be missing:

- ConfigMap values
- Secrets
- Environment variables

Check pod configuration:

kubectl describe pod <pod_name>

## 3. Resource Limits

The container may not have enough resources.

Common issues:

- Out of memory
- CPU limit too low

Check resource usage:

kubectl top pods

## Useful Commands

List pods:

kubectl get pods

Describe pod:

kubectl describe pod <pod_name>

View logs:

kubectl logs <pod_name>

Check services:

kubectl get services

## Pod is not accessible

Possible causes:

- Service configuration error
- Wrong port
- Network policy blocking traffic

Check service:

kubectl describe service <service_name>