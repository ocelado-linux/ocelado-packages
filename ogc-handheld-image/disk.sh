#!/bin/bash
set -euxo pipefail

# MicroOS: writable /etc as its own subvolume on a read-only root
/usr/libexec/setup-etc-subvol

findmnt -no UUID /
findmnt
