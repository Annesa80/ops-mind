# Linux Permission Denied

## Problem

A Linux command or application fails with:

Permission denied

This usually means the current user does not have sufficient permission to access or modify a resource.

## Check File Permissions

Run:

ls -l filename

Example:

-rw-r--r-- 1 alice developers 1200 config.txt

The permission bits determine who can read, write, or execute the file.

## Check Ownership

Run:

ls -l filename

The output shows the file owner and group.

If the wrong user owns the file, access may fail.

## Change Permissions

For example:

chmod 755 script.sh

This gives the owner read, write, and execute permissions while giving the group and others read and execute permissions.

Avoid changing permissions blindly. Grant only the access required by the application.

## Change Ownership

Example:

chown user:group filename

Use this when the file belongs to the wrong user or group.

## Directory Permissions

A user may have permission to read a file but still be unable to access it if they lack execute permission on the parent directory.

Check the permissions of parent directories as well.

## Troubleshooting Order

1. Identify the failing resource.
2. Run ls -l.
3. Check ownership.
4. Check parent directory permissions.
5. Determine whether the process runs as the expected user.
6. Modify permissions only when necessary.
