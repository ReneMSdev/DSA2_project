import csv


class HashMap:
    # Define global variables for hashmap
    ADDRESS = 0
    CITY = 1
    STATE = 2
    ZIP = 3
    DEADLINE = 4
    WEIGHT = 5
    STATUS = 6
    TIME_DELIVERED = 7
    NOTES = 8

    def __init__(self):
        self.size = 64  # Initial size of hash map
        self.map = [None] * self.size
        self.count = 0  # Number of elements in the hashmap
        self.resize_threshold = 0.7  # Resize hashmap when 70% full

    def _hash(self, key):
        """hash function to compute hash index."""
        # 'hash' function returns an integer hash value for a given key.
        # % is a modulus operator to ensure the hash value fits within bounds of array.
        # self.size represents the current capacity of the hashmap.
        return hash(key) % self.size

    def _resize(self):
        """Resize the hashmap to allow more entries."""
        print("Resizing map...")
        old_map = self.map
        self.size *= 2  # Double the size of the hashmap
        self.map = [None] * self.size
        self.count = 0  # Reset count before reinserting all elements

        for item in old_map:
            if item is not None:
                self.put(item[0], item[1])  # Reinsert into new map

    def put(self, key, value):
        """Insert or update a key-value pair in the hashmap"""
        index = self._hash(key)
        original_index = index

        while self.map[index] is not None:
            if self.map[index][0] == key:
                # Update value if key already exists
                self.map[index] = (key, value)
                return
            index = (index + 1) % self.size
            if index == original_index:
                # Table is full, resize
                self._resize()
                return

        # Insert the new key-value pair
        self.map[index] = (key, value)
        self.count += 1

        # Check if resize is needed
        if self.count / self.size >= self.resize_threshold:
            self._resize()

    def get(self, key):
        """Get the value associated with a key."""
        index = self._hash(key)
        original_index = index

        while self.map[index] is not None:
            if self.map[index][0] == key:
                return self.map[index][1]
            index = (index + 1) % self.size
            if index == original_index:
                break

        return None

    def get_package_data(self, key):
        """Get package data as a dictionary with named fields"""
        data = self.get(key)
        if data:
            address = data[self.ADDRESS]
            city = data[self.CITY]
            state = data[self.STATE]
            zip = data[self.ZIP]
            deadline = data[self.DEADLINE]
            weight = data[self.WEIGHT]
            status = data[self.STATUS]
            time_delivered = data[self.TIME_DELIVERED]
            notes = data[self.NOTES]

            # Return as a dictionary of values
            return {
                "address": address, "city": city,"state": state,
                "zip": zip, "deadline": deadline,"weight(kg)": weight,
                "status": status,"time_delivered": time_delivered,
                "notes": notes,
            }
        return None

    def display_package_data(self, key):
        package_data = self.get_package_data(key)
        if package_data:
            print(f"\nPackage ID: {key}")
            for field, value in package_data.items():
                print(f"{field.capitalize()}: {value}")

    def update_status(self, key, new_status):
        """Update the status of a package"""
        data = self.get(key)
        if data:
            # Update status
            data[self.STATUS] = new_status
            # Update hashmap with new data
            self.put(key, data)

    def update_time_delivered(self, key, time_delivered):
        data = self.get(key)
        if data:
            # Update delivery time
            data[self.TIME_DELIVERED] = time_delivered
            # Update hashmap with new data
            self.put(key, data)

    def display(self):
        """Display hashmap for debugging purposes."""
        for index, item in enumerate(self.map):
            if item:
                print(f"Index {index}: {item}")
            else:
                print(f"Index {index}: Empty")

    def load_data_into_hashmap(self):
        """Read CSV file and load contents into hashmap"""
        file_path = 'data/csv_files/WGUPS Package File.csv'

        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)

            for row in csv_reader:
                package_id = row[0]  # First Column used for package_id.
                data = row[1:]  # The remaining Columns is where the data will be stored.
                self.put(package_id, data)
        print("Data loaded into HashMap.")
