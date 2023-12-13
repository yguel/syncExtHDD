import json
import os
import subprocess
import sys
import time
from typing import List, Tuple, Optional
from typeguard import typechecked
import click

@typechecked
def get_disk_list() -> dict:
    """Get the list of disks on the system.

    Returns:
        dict: A dictionary of the disks on the system.
    """
    disk_list = {}
    cmd = "lsblk -J -f"
    try:
        output = subprocess.check_output(cmd, shell=True)
        output = output.decode("utf-8")
        disk_list = json.loads(output)
    except subprocess.CalledProcessError as e:
        print("Error: {}".format(e))
    return disk_list

@typechecked
def get_disk_info(disk_uuid : str) -> Optional[dict]:
    """Get the disk information from the disk list.

    Args:
        disk_uuid (str): The UUID of the disk we want to get information for.

    Returns:
        dict: The disk information.
    """
    disk_info = {}
    disk_list = get_disk_list()
    for disk in disk_list["blockdevices"]:
        if disk["uuid"] == disk_uuid:
            disk_info = disk
            return disk_info
        elif "children" in disk:
            for child in disk["children"]:
                if child["uuid"] == disk_uuid:
                    disk_info = child
                    return disk_info
    return None

@typechecked
def sync_disk(disk_uuid : str ) -> bool:
    """Sync the disk with the given UUID.

    Args:
        disk_uuid (str): The UUID of the disk to sync.

    Returns:
        bool: True if the disk was synced, False otherwise.
    """
    disk_info = get_disk_info(disk_uuid)
    if disk_info:
        disk_paths = disk_info["mountpoints"]
        if len(disk_paths) == 0:
            print("Warning: Disk {} is not mounted.".format(disk_uuid))
            return True
        elif len(disk_paths) > 1:
            print("Warning: Disk {} is mounted in multiple locations. Syncing the first location: {}".format(disk_uuid, disk_paths[0]))
        disk_path = disk_paths[0]
        cmd = "sync {}".format(disk_path)
        try:
            subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as e:
            print("Error: {}".format(e))
            return False
        return True
    return False

@click.command()
@click.option("--config", "-cfg", type=click.Path(exists=True, dir_okay=False), default="disks_to_sync.json", help="The path to the configuration file listing the disks to synchronize.")
@click.option("--frequency", "-freq", type=int, required=False, help="The frequency in seconds to synchronize the disks.")
def main(config : str, frequency : Optional[int] = None):
    """Sync the disks listed in the configuration file.
    """
    disks_to_sync = None
    try:
        with open(config, "r") as f:
            disks_to_sync = json.load(f)
    except Exception as e:
        print("ERROR, impossible to load configuration file: {}".format(e))
        sys.exit(1)
    if "disks" not in disks_to_sync:
        print("ERROR, no disks to sync in configuration file.")
        sys.exit(1)
    disks = disks_to_sync["disks"]
    logs = {}
    nb_loops = 0
    while True:
        for k,disk in enumerate(disks):
            if "uuid" not in disk:
                print("ERROR, no UUID for disk number {}.".format(k))
                sys.exit(1)
            uuid = disk["uuid"]
            label = None
            if "label" in disk:
                label = disk["label"]
            if uuid not in logs:
                logs[uuid] = {"label": label, "nb_sync": 0, "last_sync": None, "nb_sync_error" : 0}
            ret = sync_disk(uuid)
            if ret:
                logs[uuid]["nb_sync"] += 1
                logs[uuid]["last_sync"] = time.monotonic()
                if frequency is None:
                    if label is not None:
                        print("Synced disk: {} ({})".format(label,uuid))
                    else:
                        print("Synced disk: {}".format(uuid))
            else:
                if "label" in disk_uuid:
                    print("Failed to sync disk: {} ({})".format(label, uuid))
                else:
                    print("Failed to sync disk: {}".format(uuid))
                if frequency is not None:
                    log[uuid]["nb_sync_error"] += 1
            
        # Handle frequency
        if frequency is None:
            return
        else:
            # Handle logs
            nb_loops += 1
            time_elapsed = nb_loops * frequency
            log_time_frame = 120
            if time_elapsed >= log_time_frame:
                nb_loops= 0
                if len(logs) == 0:
                    print("No disk synced in the last {} seconds.".format(log_time_frame))
                for disk in disks:
                    uuid = disk["uuid"]
                    if uuid in logs:
                        label = logs[uuid]["label"]
                        nb_sync = logs[uuid]["nb_sync"]
                        last_sync = logs[uuid]["last_sync"]
                        if last_sync is not None:
                            print("Disk {} ({}) was synced {} times in the last {} seconds (last time: {}).".format(label, uuid, nb_sync, log_time_frame, last_sync))
                    else:
                        label = None
                        if "label" in disk:
                            label = disk["label"]
                        print("Disk {} ({}) was never synced in the last {} seconds.".format(label, uuid, log_time_frame))
                logs = {}
            # SLEEP FOR THE REMAINING TIME
            sys.stdout.flush()
            time.sleep(frequency)
