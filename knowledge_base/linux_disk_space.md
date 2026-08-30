# Linux Disk Space Problems

## Problem

A Linux system or application begins failing because the filesystem is full.

Symptoms may include:

- applications failing to write files
- database errors
- logging failures
- package installation failures
- inability to create temporary files

## Check Filesystem Usage

Run:

df -h

This shows filesystem capacity and usage.

If a filesystem is near 100% utilization, identify what is consuming the space.

## Find Large Directories

Run:

du -sh *

For a more detailed investigation, inspect large directories individually.

## Common Causes

### Large Log Files

Application or system logs may consume significant disk space.

Inspect log directories and determine whether old logs can be safely removed or rotated.

### Temporary Files

Temporary files may accumulate over time.

### Package Cache

Package managers may store cached packages.

### Application Data

Applications may generate large files such as uploads, caches, or database backups.

## Important Warning

Do not immediately delete files simply because they are large.

Determine what the file is used for before removing it.

Deleting active database files or application data can cause data loss.

## Troubleshooting Order

1. Run df -h.
2. Identify the full filesystem.
3. Find large directories.
4. Identify large files.
5. Determine whether files can safely be removed.
6. Clean up or configure log rotation where appropriate.
