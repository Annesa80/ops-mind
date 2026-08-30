# Incident Response Procedure

## Purpose

Use this procedure when a production system experiences unexpected behavior or an outage.

The objective is to restore service safely while collecting enough information to identify the root cause.

## Step 1 — Understand the Problem

Determine:

- what is failing
- which users are affected
- when the problem started
- whether the problem is intermittent or continuous
- whether the issue affects one service or multiple services

## Step 2 — Collect Information

Gather:

- application logs
- infrastructure metrics
- deployment history
- error messages
- affected service names
- timestamps

Avoid making changes before collecting basic evidence unless immediate mitigation is required.

## Step 3 — Check Recent Changes

Determine whether the problem started after:

- application deployment
- configuration change
- infrastructure change
- database migration
- dependency update

A recent change is a useful investigation clue but should not automatically be assumed to be the root cause.

## Step 4 — Identify Possible Causes

Common categories include:

- application failures
- database failures
- network failures
- resource exhaustion
- configuration errors
- dependency failures

## Step 5 — Mitigate

If possible, restore service using the safest available mitigation.

Examples include:

- rollback a deployment
- restart an unhealthy service
- scale a service
- disable a failing feature

Mitigation should be reversible when possible.

## Step 6 — Verify Recovery

After mitigation:

1. Confirm service health.
2. Check application logs.
3. Verify error rates.
4. Confirm affected functionality works.
5. Continue monitoring for recurrence.

## Step 7 — Document the Incident

Record:

- timeline
- symptoms
- root cause
- mitigation
- permanent fix
- lessons learned

## Escalation

Escalate the incident when:

- the root cause is unclear
- the issue affects critical production services
- data integrity may be affected
- the available mitigation is risky
- the incident exceeds the team's response capability
