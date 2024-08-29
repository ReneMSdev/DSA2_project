import csv


class Packages:
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
        self.size = 64  # Initial size of hash map
        self.map = [None] * self.size
        self.count = 0  # Number of elements in the hashmap
        self.resize_threshold = 0.7  # Resize hashmap when 70% full
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
                    self.insert(package_id, data)

    def _hash(self, package_id):
        """hash function to compute hash index."""
        # 'hash' function returns an integer hash value for a given key.
        # % is a modulus operator to ensure the hash value fits within bounds of array.
        # self.size represents the current capacity of the hashmap.
        return hash(package_id) % self.size

    def _resize(self):
        """Resize the hashmap to allow more entries."""
        print("Resizing map...")
        old_map = self.map
        self.size *= 2  # Double the size of the hashmap
        self.map = [None] * self.size
        self.count = 0  # Reset count before reinserting all elements

        for item in old_map:
            if item is not None:
                self.insert(item[0], item[1])  # Reinsert into new map

    def insert(self, package_id, data):
        """Insert or update a data for given package_id in the hashmap"""
        index = self._hash(package_id)
        original_index = index

        while self.map[index] is not None:
            if self.map[index][self.PACKAGE_ID] == package_id:
                # Update data if package_id already exists
                self.map[index] = (package_id, data)
                return
            index = (index + 1) % self.size
            if index == original_index:
                # Table is full, resize
                self._resize()
                return

        # Insert the new key and corresponding data
        self.map[index] = (package_id, data)
        self.count += 1

        # Check if resize is needed
        if self.count / self.size >= self.resize_threshold:
            self._resize()

    def get(self, package_id):
        """Get the value associated with a key."""
        index = self._hash(package_id)
        original_index = index

        while self.map[index] is not None:
            if self.map[index][self.PACKAGE_ID] == package_id:
                return self.map[index][1]  # 1 is index for data
            index = (index + 1) % self.size
            if index == original_index:
                break

        return None

    def get_all_packages(self):
        """ Return all non-None packages """
        all_packages = []
        for entry in self.map:
            if entry is not None:
                all_packages.append(entry[1])  # entry[1] contains package data

        # Sort all packages by package ID
        all_packages.sort(key=lambda package: int(package[self.PACKAGE_ID]))
        return all_packages

    def update_time_loaded(self, package_id, time_loaded):
        """Update the time loaded"""
        data = self.get(package_id)
        if data:
            # Update time loaded
            data[self.TIME_LOADED] = time_loaded
            # Update hashmap with new data
            self.insert(package_id, data)

    def update_time_delivered(self, package_id, time_delivered):
        data = self.get(package_id)
        if data:
            # Update delivery time
            data[self.TIME_DELIVERED] = time_delivered
            # Update hashmap with new data
            self.insert(package_id, data)

    def update_truck_id(self, package_id, truck_id):
        """ Update the truck ID for a package """
        data = self.get(package_id)
        if data:
            # Update the truck id
            data.append(truck_id)
            self.insert(package_id, data)

    def display(self):
        """Display hashmap for debugging purposes."""
        for index, item in enumerate(self.map):
            if item:
                print(f"Index {index}: {item}")
            else:
                print(f"Index {index}: Empty")


""" Testing """
# packages = Packages()
# print(packages.get_package_data("1"))
