# Kubernetes Pod Stuck in Pending

## Problem

A Kubernetes pod remains in the Pending state and never starts running.

Check the status:

kubectl get pods

Example:

NAME       READY   STATUS    RESTARTS
api-pod    0/1     Pending   0

## First Investigation

Describe the pod:

kubectl describe pod <pod_name>

The Events section near the bottom of the output often explains why scheduling failed.

## Common Causes

### Insufficient CPU

The cluster may not have enough available CPU to satisfy the pod's resource request.

Check:

kubectl describe nodes

### Insufficient Memory

The requested memory may be greater than the available capacity of eligible nodes.

Review the pod resource requests.

### Node Selector Problems

A pod may require a node with a specific label.

If no node matches the selector, the pod cannot be scheduled.

### Taints and Tolerations

A node may have a taint that prevents the pod from being scheduled unless the pod has a matching toleration.

### Persistent Volume Problems

A pod may remain Pending because a required PersistentVolumeClaim cannot be bound.

Check:

kubectl get pvc

## Troubleshooting Order

1. Check pod status.
2. Describe the pod.
3. Inspect scheduling events.
4. Check node resources.
5. Check node selectors.
6. Check taints and tolerations.
7. Check PersistentVolumeClaims.

Useful commands:

kubectl get pods

kubectl describe pod <pod_name>

kubectl describe nodes

kubectl get pvc
