# Linux High CPU and Memory Usage

## High CPU Usage

## Problem

A Linux system becomes slow because one or more processes consume excessive CPU.

## Investigation

Run:

top

or:

htop

Identify processes consuming unusually high CPU.

Check whether the process is expected to perform intensive work.

## Common Causes

- runaway processes
- inefficient application code
- unexpected traffic
- background jobs
- infinite loops
- excessive parallel work

Investigate application logs and recent deployments to determine whether the behavior started after a change.

---

# High Memory Usage

## Problem

An application or server consumes most available memory.

Symptoms include:

- slow performance
- process termination
- out-of-memory errors
- swapping

## Investigation

Use:

free -h

and:

top

or:

htop

Identify which processes consume the most memory.

## Common Causes

- memory leaks
- unusually large workloads
- insufficient application limits
- excessive caching
- too many concurrent processes

## Containerized Applications

If the application runs inside Docker or Kubernetes, check the container or pod memory limits in addition to host memory usage.

A process may be killed because of a container memory limit even when the host still has available memory.

## Troubleshooting Order

1. Identify the affected resource.
2. Identify the process consuming CPU or memory.
3. Check recent deployments.
4. Inspect application logs.
5. Check configured resource limits.
6. Determine whether the workload is expected.
