from datetime import datetime


class Timestamps:
    def __init__(self):
        # Dictionary to store snapshots at different times
        # Key is the time (string), value is dictionary of package statuses
        self.snapshots = {}

    def take_snapshot(self, current_time, truck_id, hashmap):
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
        # composite key (time, truck_id) to store snapshots uniquely
        self.snapshots[(current_time, truck_id)] = snapshot

    def get_snapshot(self, lookup_time):
        """
        Retrieve the closest previous snapshots of packages statuses / delivery times
        :param lookup_time: The time to look up the snapshot
        :return: Dictionary of package statuses
        """
        # Convert lookup_time ot a datetime object for comparison
        lookup_time_obj = datetime.strptime(lookup_time, "%I:%M %p")
        # Extract only the time component from each key (which is a tuple)
        available_times = sorted(
            [(time, truck_id)
             for time, truck_id in self.snapshots.keys()
             if datetime.strptime(time, "%I:%M %p") <= lookup_time_obj],
            key=lambda x: datetime.strptime(x[0], "%I:%M %p")
        )

        # find the nearest available snapshot that is not later than the lookup time
        if available_times:
            nearest_snapshot = available_times[-1]
            return self.snapshots[nearest_snapshot]
        else:
            return "No data available for this time."
