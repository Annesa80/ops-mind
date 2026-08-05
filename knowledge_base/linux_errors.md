# Linux Error Troubleshooting Guide

## Permission denied error

### Problem

A user receives permission denied when accessing a file.

### Possible Causes

## 1. Incorrect File Permissions

Check permissions:

ls -l filename

Change permissions:

chmod 755 filename

## 2. Wrong File Ownership

Check ownership:

ls -l filename

Change owner:

chown user:group filename

---

# Disk space problem

## Symptoms

Applications fail because the disk is full.

Check disk usage:

df -h

Find large files:

du -sh *

## Solution

Remove unnecessary files:

- old logs
- temporary files
- unused packages

---

# Process using too much CPU

Check running processes:

top

or:

htop

Find the problematic process and investigate its logs.