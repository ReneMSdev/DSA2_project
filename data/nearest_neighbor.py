from data.distance_calculator import DistanceCalculator
from data.hashmap import HashMap


class NearestNeighbor:
    # global variables
    HUB = "4001 South 700 East"

    def __init__(self):
        self.dc = DistanceCalculator()
        self.hashmap = HashMap()

    def calculate_route(self, package_list):
        # initialize starting point
        current_address = self.HUB
        route = []  # Initialize route array
        visited = set(route)  # Set to keep track of visited addresses
        total_distance = 0  # total distance traveled

        while len(route) < len(package_list):
            nearest_address = None
            shortest_distance = float('inf')  # Start with infinitely large distance

            for package_id in package_list:
                package_data = self.hashmap.get_package_data(package_id)
                if package_data:
                    address = package_data["address"]

                    # Skip if already visited(if multiple packages assigned to same address)
                    if address in visited:
                        continue

                    # Calculate distance from current address to this address
                    distance = self.dc.get_distance(current_address, address)

                    # Check if this address is the nearest
                    if distance < shortest_distance:
                        shortest_distance = distance
                        nearest_address = address

            # Update route and visited addresses
            if nearest_address:
                route.append(nearest_address)
                visited.add(nearest_address)
                total_distance += shortest_distance
                current_address = nearest_address  # Move to the next address

        return route, total_distance


""" Testing """
# nn = NearestNeighbor()
# package_list = ["1", "2", "3"]
# route, distance = nn.calculate_route(package_list)
# print("Optimized Route: ", route)
# print("Total Distance: ", distance)

