#!/bin/sh
if [ "${1}" == "pre" ]; then
  cd /usr/local/bin/syncExtHdd && bash -c 'poetry run psync -cfg /usr/local/bin/syncExtHdd/disks_to_sync.json'
fi