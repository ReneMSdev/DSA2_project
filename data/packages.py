import csv


class Packages:
    """Packages class uses no additional libraries or classes only csv for loading data"""
    # Define global variables for hashmap
    PACKAGE_ID = 0
    ADDRESS = 1
    CITY = 2
    STATE = 3
    ZIP = 4
    DEADLINE = 5
    WEIGHT = 6
    TIME_LOADED = 7
    TIME_DELIVERED = 8
    NOTES = 9

    def __init__(self):
        self.size = 10  # Initial size of hash map
        self.map = [[] for _ in range(self.size)]  # List of strings for separate chaining
        self._load_data_into_hashmap()

    def _load_data_into_hashmap(self):
        """Read CSV file and load contents into hashmap"""
        file_path = 'data/csv_files/WGUPS Package File.csv'

        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)

            for row in csv_reader:
                package_id = row[self.PACKAGE_ID].strip()  # First Column used for package_id.

                if package_id.isdigit():  # Check if package_id is numeric to avoid errors.
                    data = row[:]  # Store all data from each column
                    self[package_id] = data

    def _hash(self, package_id):
        """hash function to compute hash index."""
        return int(package_id) % self.size

    def __setitem__(self, package_id, data):
        """ Insert or update data for given package_id in hashmap"""
        index = self._hash(package_id)

        # Check if the package_id already exists in the chain
        for i, entry in enumerate(self.map[index]):
            if entry[0] == package_id:  # entry[0] is package_id
                self.map[index][int(i)] = (package_id, data)  # Update the data
                return

        # if package_id not found, add the new entry
        self.map[index].append((package_id, data))

    def __getitem__(self, package_id):
        """Get the value associated with package_id"""
        index = self._hash(package_id)

        # Look for the package_id in the chain at given index
        for entry in self.map[index]:
            if entry[0] == package_id:
                return entry[1]  # entry[1] is the data
        return None

    def __delitem__(self, package_id):
        """Remove the entry associated wih package_id"""
        index = self._hash(package_id)

        for entry in self.map[index]:
            if entry[0] == package_id:
                self.map[index].remove(entry)
                return True  # Return true if deletion was successful
        return False  # Return false if key was not found

    def get_all_packages(self):
        """ Return all non-None packages """
        all_packages = []
        for chain in self.map:
            for pid, data in chain:  # for (package_id, data) in chain
                all_packages.append(data)

        # Sort all packages by package ID
        all_packages.sort(key=lambda package: int(package[self.PACKAGE_ID]))
        return all_packages

    def update_time_loaded(self, package_id, time_loaded):
        """Update the time loaded"""
        data = self[package_id]
        if data:
            # Update time loaded
            data[self.TIME_LOADED] = time_loaded
            # Update hashmap with new data
            self[int(package_id)] = data

    def update_time_delivered(self, package_id, time_delivered):
        data = self[package_id]
        if data:
            # Update delivery time
            data[self.TIME_DELIVERED] = time_delivered
            # Update hashmap with new data
            self[package_id] = data

    def update_truck_id(self, package_id, truck_id):
        """ Update the truck ID for a package """
        data = self[package_id]
        if data:
            # Update the truck id
            data.append(truck_id)
            self[package_id] = data

    def display(self):
        """Display hashmap for debugging purposes."""
        for index, chain in enumerate(self.map):
            if chain:
                print(f"Index {index}: {chain}")
            else:
                print(f"Index {index}: Empty")


""" Testing """
# packages = Packages()
#
# package_data = packages["1"]
# print(f"Package data for ID '1': {package_data}")
