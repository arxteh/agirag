#!/bin/bash
echo "Start entrypoint.sh"

set -e

mkdir -p /var/run/sshd

ls /etc/ssh/ssh_host_* >/dev/null 2>&1 &&echo "Keys is found" ||echo "Key generation." && ssh-keygen -A

# Environment variables that are used if not empty:
# USER_PASSWORD

if [ -f /.ispasswordset ]; then
    echo "Password already set"
else
    echo "Set  password of user for sshd"
    echo 'ubuntu:'${USER_PASSWORD} |chpasswd
    touch /.ispasswordset
fi

echo "Run sshd"

exec "$@"