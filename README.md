To have that script that sync periodically your hard drives:
  1. ``sudo su`` (login as root)
  2. copy the project under ``/usr/local/bin``
  3. install the project
      1. ``cd /usr/local/bin/syncExtHdd``
      2. ``python3.10 -m pip install poetry``
      3. ``poetry install``
      4. Copy the file ``disks_to_sync.template.json`` to ``disks_to_sync.json`` and edit it to put the uuid of your disks
          - to get the uuid of your disks, once you have plugged them, run ``lsblk -f`` and look at the UUID column
      5. test: ``poetry run psync -cfg /usr/local/bin/syncExtHdd/disks_to_sync.json``
      6. If everything is ok, you should see something like: ``Synced disk: myDiskLabel (xxxxeeee-xxxx-xxxx-xxxx-xxxxffffeeee)``
  4. ``cd /etc/systemd/system/``
  5. ``ln -s /usr/local/bin/syncExtHdd/systemd.service/sync_ext_hdd.service``
  6. ``systemctl enable sync_ext_hdd`` for automatic start at boot
  7. ``systemctl start sync_ext_hdd`` to start it now
  8. ``journalctl -u sync_ext_hdd -f`` to see the logs (after 2 minutes)

To have that script that sync your hard drives when you suspend or hibernate your computer:
  1. ``sudo su`` (login as root)
  2. copy the project under ``/usr/local/bin`` (if not already done)
  3. copy the script ``sync_before_sleep.sh`` under ``/usr/lib/systemd/system-sleep/``
  4. ``chmod +x /usr/lib/systemd/system-sleep/sync_before_sleep.sh``