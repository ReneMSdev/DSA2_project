from datetime import datetime, timedelta
from data.nearest_neighbor import NearestNeighbor
from tabulate import tabulate


class Truck:
    # Global variable(s)
    HUB = "4001 South 700 East"
    LOCATION = 1
    TIME_FORMAT = "%I:%M %p"

    def __init__(self, truck_id, package_data, start_time):
        self.truck_id = truck_id
        self.packages = []  # List to store Package IDs loaded onto truck
        self.start_time = start_time  # Start time is a parameter
        self.current_time = self.start_time  # Initialize current time with start time
        self.current_location = self.HUB  # Starting location (HUB)
        self.distance_traveled = 0
        self.speed = 18  # Truck speed in miles per hour
        self.hashmap = package_data  # Reference to hashmap object for updating
        self.nn = NearestNeighbor(package_data)  # nearest neighbor algorithm
        self.packages_delivered = 0

    def load_packages(self, package_list):
        """Load all packages onto truck from list of package IDs"""
        self.packages = package_list  # Load packages from package_list

        # Update the time_loaded of package
        for package_id in package_list:
            self.hashmap.update_time_loaded(package_id, self.current_time.strftime(self.TIME_FORMAT))
            self.hashmap.update_truck_id(package_id, self.truck_id)

        route = self.calculate_route()  # calculate route once packages are loaded
        self.deliver_all_packages(route)  # deliver all packages after optimal calculating route

    def deliver_package(self, package_id):
        """Deliver a package and update delivery time"""
        if package_id in self.packages:
            delivery_time = self.current_time.strftime(self.TIME_FORMAT)  # current time string

            # Update delivery time
            self.hashmap.update_time_delivered(package_id, delivery_time)
            self.packages_delivered += 1

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
                    package_data = self.hashmap[package_id]
                    # if there is package data and the address matches location continue with delivery
                    if package_data and package_data[self.LOCATION] == location:
                        self.deliver_package(package_id)  # Deliver the package

        # Call return_to_hub after delivering all packages
        self.return_to_hub(self.current_location)

    def return_to_hub(self, last_location):
        """ Return to Hub after all deliveries """
        distance_to_hub = self.nn.dc.get_distance(last_location, self.HUB)
        self.update_time(distance_to_hub)  # Update time when returning to Hub
        self.distance_traveled += distance_to_hub  # Update total distance traveled
        self.current_location = self.HUB  # set current location to Hub
        # print(f"Truck {self.truck_id} returned to the hub at {self.current_time.strftime('%I:%M %p')}."
        #       f"\nTotal distance traveled: {round(self.distance_traveled, 1)} miles.")

    def display_report(self):
        """Display a summary report for this truck"""
        total_distance = round(self.distance_traveled, 1)
        start_time = self.start_time.strftime(self.TIME_FORMAT)
        current_time = self.current_time.strftime(self.TIME_FORMAT)
        # calculate time passed in hours and minutes
        time_passed = self.current_time - self.start_time
        hours, remainder = divmod(time_passed.total_seconds(), 3600)
        minutes, _ = divmod(remainder, 60)
        time_passed_str = f"{int(hours)}hr {int(minutes)} min"
        packages_delivered = self.packages_delivered

        # prepare data
        report_data = [
            ["Truck", f"Truck {self.truck_id}"],
            ["Total Distance", f"{total_distance} miles"],
            ["Start Time", start_time],
            ["End Time", current_time],
            ["Total Time", time_passed_str],
            ["Packages Delivered", packages_delivered]
        ]

        # Print the truck report using tabulate
        print(tabulate(report_data, headers=["Truck Report", ""]))


""" Testing """
# truck = Truck(1)
# load = ["1","2","3","4","5","23", "15", "8"]
# truck.load_package(load)
# route = truck.calculate_route()
# truck.deliver_all_packages(route)
# packages = truck.hashmap
# for item in load:
#     print(packages.get_package_data(item))
