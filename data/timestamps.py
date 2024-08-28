from datetime import datetime


class Timestamps:
    def __init__(self):
        # Dictionary to store snapshots at different times
        # Key is the time (string), value is dictionary of package statuses
        self.snapshots = []

    def take_snapshot(self, current_time, hashmap):
        """
        Take a snapshot of all package statuses and delivery times
        at any given time.
        """
        snapshot = {}

        # Iterate over all packages in the hashmap
        for package_id in hashmap.map:
            if package_id:
                package_data = hashmap.get_package_data(package_id[0])  # input is package_id
                if package_data:
                    snapshot[package_id[0]] = {
                        'status': package_data['status'],
                        'time_delivered': package_data['time_delivered']
                    }

        # Check if there is already a snapshot for the current time minute
        existing_snapshot = next((snap for snap in self.snapshots if snap['time'] == current_time), None)

        if existing_snapshot:
            # Merge the new snapshot into the existing one
            for package_id, data in snapshot.items():
                existing_snapshot['snapshot'][package_id] = data
            print(f"Merged snapshot at {current_time}")
        else:
            # Append new snapshot
            self.snapshots.append({
                'time': current_time,
                'snapshot': snapshot
            })
            print(f"Snapshot taken at {current_time}")

    def get_snapshot(self, lookup_time):
        """
        Retrieve the closest previous snapshots of packages statuses / delivery times
        :param lookup_time: The time to look up the snapshot
        :return: Dictionary of package statuses
        """
        # Convert lookup_time to a datetime object for comparison
        lookup_time_obj = datetime.strptime(lookup_time, "%I:%M %p")
        nearest_snapshot = None
        nearest_time_diff = float('inf')

        for snapshot_entry in self.snapshots:
            snapshot_time_obj = datetime.strptime(snapshot_entry['time'], "%I:%M %p")
            time_diff = lookup_time_obj - snapshot_time_obj
            if 0 <= time_diff.total_seconds() < nearest_time_diff:
                nearest_time_diff = time_diff.total_seconds()
                nearest_snapshot = snapshot_entry['snapshot']

        if nearest_snapshot:
            return nearest_snapshot
        else:
            return "No data available for this time."
