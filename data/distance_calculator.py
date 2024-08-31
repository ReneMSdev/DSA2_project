import pandas as pd
import numpy as np


class DistanceCalculator:
    def __init__(self):
        self.file_path = 'data/csv_files/WGUPS Distance Table.csv'
        self.address_to_index = {}  # empty dictionary to store address indexes
        self.adjacency_matrix = None  # initialize the matrix with NaN values
        self.cleaned_addresses = []  # stores the cleaned addresses
        self._load_and_clean_data()  # Load data and process addresses

    def _load_and_clean_data(self):
        # Load CSV file into a DataFrame
        distance_table = pd.read_csv(self.file_path)

        # Extract the location names (columns and rows)
        locations = distance_table.columns[2:]  # Skip the first two columns

        # Clean and store addresses
        self.cleaned_addresses = self._clean_addresses(locations)

        # Determine the number of locations
        num_locations = len(locations)

        # Initialize an adjacency matrix with zeros
        self.adjacency_matrix = np.zeros((num_locations, num_locations))

        # fill in the adjacency matrix with distances
        for i in range(num_locations):
            for j in range(num_locations):
                # Retrieve the distance value from the dataframe
                distance_value = distance_table.iloc[i, j + 2]  # Offset by 2 to skip non-distance columns
                if pd.notna(distance_value):  # Check if the value is non NaN
                    self.adjacency_matrix[i, j] = distance_value

        # Create a dictionary to map addresses to indices
        self.address_to_index = {address: index for index, address in enumerate(self.cleaned_addresses)}

    @staticmethod
    def _clean_addresses(locations):
        # Initialize a list for cleaned addresses
        cleaned_addresses = []

        # Loop through each location to extract just the street address
        for location in locations:
            # Remove newline characters and extra spaces, standardizing the address format
            street_address = location.split('\n')[1] if '\n' in location else location
            street_address = street_address.split(',')[0].strip()
            cleaned_addresses.append(street_address)

        return cleaned_addresses

    def get_distance(self, address1, address2):
        # Get indices from addresses
        index1 = self.address_to_index.get(address1)
        index2 = self.address_to_index.get(address2)

        if index1 is None or index2 is None:
            print(f"Error: One or both addresses '{address1}' or '{address2}' not found")
            return None

        # one of these variables will contain the real distance
        distance1 = self.adjacency_matrix[index1, index2]
        distance2 = self.adjacency_matrix[index2, index1]

        # Check to make sure 0.0 is not returned
        if distance1 != 0.0:
            return distance1
        elif distance2 != 0.0:
            return distance2
        else:
            print(f"Warning: Distance between '{address1}' and '{address2}' is 0.0 or not found.")
            return None


""" testing """
# dc = DistanceCalculator()
# print(dc.cleaned_addresses)
# print(dc.adjacency_matrix)
# address_one = "4001 South 700 East"
# address_two = "5025 State St"
# distance = dc.get_distance(address_one, address_two)
# print(distance)
