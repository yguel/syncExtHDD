To have that script that sync periodically your hardrives:
  1. ``sudo su`` (login as root)
  2. copy the project under ``/usr/local/bin``
  3. ``cd /etc/systemd/system/``
  4. ``ln -s /usr/local/bin/syncExtHdd/systemd.service/sync_ext_hdd.service``
  5. ``systemctl enable sync_ext_hdd`` for automatic start at boot
  6. ``systemctl start sync_ext_hdd`` to start it now
  7. ``systemctl -u sync_ext_hdd -f`` to see the logs (after 2 minutes)

To have that script that sync your hardrives when you suspend or hibernate your computer:
  1. ``sudo su`` (login as root)
  2. copy the project under ``/usr/local/bin`` (if not already done)
  3. copy the script ``sync_before_sleep.sh`` under ``/usr/lib/systemd/system-sleep/``
  4. ``chmod +x /usr/lib/systemd/system-sleep/sync_before_sleep.sh``