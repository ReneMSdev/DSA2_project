from email.headerregistry import Address

from data.distance_calculator import DistanceCalculator


class NearestNeighbor:
    # global variables
    HUB = "4001 South 700 East"
    ADDRESS = 0

    def __init__(self, hashmap):
        self.dc = DistanceCalculator()
        self.hashmap = hashmap

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
                if not package_data:
                    print(f"Package data for package {package_id} not found.")
                    continue

                address = package_data[self.ADDRESS]  # Index for Address

                # Skip if already visited(if multiple packages assigned to same address)
                if address in visited:
                    continue

                # Calculate distance from current address to this address
                distance = self.dc.get_distance(current_address, address)

                # Check if this address is the nearest
                if distance is not None and distance < shortest_distance:
                    shortest_distance = distance
                    nearest_address = address

            # Update route and visited addresses
            if nearest_address:
                route.append(nearest_address)
                visited.add(nearest_address)
                total_distance += shortest_distance
                current_address = nearest_address  # Move to the next address
                # print(f"Nearest address found: {nearest_address} with distance: {shortest_distance}")
            else:
                print("Nearest address not found")
                break

        return route, total_distance


""" Testing """
# nn = NearestNeighbor()
# package_list = ["1", "2", "3"]
# route, distance = nn.calculate_route(package_list)
# print("Optimized Route: ", route)
# print("Total Distance: ", distance)

