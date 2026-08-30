# Kubernetes Service Connection Problems

## Problem

A Kubernetes application is running, but clients cannot connect to it through a Service.

Typical symptoms include:

- connection refused
- timeout
- no response
- Service has no endpoints

## Check the Service

List Services:

kubectl get services

Describe the Service:

kubectl describe service <service_name>

Pay attention to:

- port
- targetPort
- selector
- endpoints

## Check Endpoints

A Service must have matching pods.

Check:

kubectl get endpoints <service_name>

If there are no endpoints, the Service selector may not match any pods.

## Common Cause: Incorrect Selector

For example, a Service may select:

app=api

while the pod has:

app=backend

The Service will not route traffic to that pod.

## Common Cause: Incorrect targetPort

The Service's targetPort must correspond to the port where the application is listening inside the pod.

For example:

port: 80

targetPort: 8080

means clients connect to port 80 while traffic is forwarded to port 8080 on the pod.

## Troubleshooting Order

1. Check the Service.
2. Check Service selectors.
3. Check endpoints.
4. Check pod labels.
5. Verify targetPort.
6. Verify that the application is listening on the expected port.
7. Check pod logs.

Useful commands:

kubectl get services

kubectl describe service <service_name>

kubectl get endpoints <service_name>

kubectl get pods --show-labels
