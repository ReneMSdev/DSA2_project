from datetime import datetime, timedelta
from data.nearest_neighbor import NearestNeighbor
from data.timestamps import Timestamps
# from data.distance_calculator import DistanceCalculator
# from data.hashmap import HashMap


class Truck:
    # Global variable(s)
    HUB = "4001 South 700 East"

    """add input here so all trucks use the same package data!!!"""
    def __init__(self, truck_id, package_data, timestamps):
        self.truck_id = truck_id
        self.packages = []  # List to store Package IDs loaded onto truck
        self.start_time = datetime.strptime("8:00 AM", "%I:%M %p")
        # Fixed start time as a datetime object ^^^
        self.current_time = self.start_time  # Initialize current time with start time
        self.current_location = self.HUB  # Starting location (HUB)
        self.distance_traveled = 0
        self.travel_time = 0
        self.speed = 18  # Truck speed in miles per hour
        self.nn = NearestNeighbor()  # nearest neighbor algorithm
        self.hashmap = package_data  # Reference to hashmap object for updating
        self.timestamps = timestamps  # Timestamps instance to track snapshots

    def load_packages(self, package_list):
        """Load package onto truck by adding its ID to the list of packages"""
        self.packages = package_list

    def deliver_package(self, package_id):
        """Deliver a package and update its status and delivery time"""
        new_status = "DELIVERED"
        if package_id in self.packages:
            delivery_time_str = self.current_time.strftime("%I:%M %p")  # Convert current_time to string format
            self.hashmap.update_status(package_id, new_status)
            self.hashmap.update_time_delivered(package_id, delivery_time_str)
            print(f"Package {package_id} delivered at {delivery_time_str}")
        else:
            print(f"Package {package_id} not loaded on Truck {self.truck_id}")

    def calculate_travel_time(self, distance):
        # Calculate the time to travel the given distance at current speed
        travel_time_hours = distance / self.speed
        travel_time_minutes = round(travel_time_hours * 60)
        return travel_time_minutes

    def update_time(self, distance):
        """ Update the current time based on distance traveled """
        # calculate the minutes passed
        minutes_passed = self.calculate_travel_time(distance)

        # Update the time by adding the minutes passed
        self.current_time += timedelta(minutes=minutes_passed)

    def calculate_route(self):
        """ Calculate the delivery route using Nearest Neighbor algorithm """
        route, total_distance = self.nn.calculate_route(self.packages)
        return route

    def deliver_all_packages(self, route):
        """ Deliver all packages based on calculated route and take snapshot"""
        for location in route:
            if location != self.current_location:  # Check to avoid calculating distance from the current location
                distance_to_next = self.nn.dc.get_distance(self.current_location, location)
                self.update_time(distance_to_next)  # Update time using distance to next location
                self.distance_traveled += distance_to_next  # add distance to total distance_traveled
                self.current_location = location

                # Deliver all packages at current location
                for package_id in self.packages:
                    package_data = self.hashmap.get_package_data(package_id)
                    # if there is package data and the address matches location continue with delivery
                    if package_data and package_data['address'] == location:
                        self.deliver_package(package_id)  # Deliver the package
                        # Take a snapshot after each delivery
                        self.timestamps.take_snapshot(self.current_time.strftime("%I:%M %p"), self.truck_id, self.hashmap)

        self.return_to_hub(route[-1])  # Return to hub from final location

    def return_to_hub(self, last_location):
        """ Return to Hub after all deliveries """
        distance_to_hub = self.nn.dc.get_distance(last_location, self.HUB)
        self.update_time(distance_to_hub)  # Update time when returning to Hub
        self.distance_traveled += distance_to_hub  # Update total distance traveled
        self.current_location = self.HUB  # set current location to Hub
        print(f"Truck {self.truck_id} returned to the hub at {self.current_time.strftime('%I:%M %p')}."
              f"\nTotal distance traveled: {self.distance_traveled} miles.")


""" Testing """
# truck = Truck(1)
# load = ["1","2","3","4","5","23", "15", "8"]
# truck.load_package(load)
# route = truck.calculate_route()
# truck.deliver_all_packages(route)
# packages = truck.hashmap
# for item in load:
#     print(packages.get_package_data(item))
