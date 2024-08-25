import csv


class HashMap:
    def __init__(self):
        self.size = 64  # Initial size of hash map
        self.map = [None] * self.size
        self.count = 0  # Number of elements in the hashmap
        self.resize_threshold = 0.7  # Resize hashmap when 70% full

    def _hash(self, key):
        """hash function to compute hash index."""
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
