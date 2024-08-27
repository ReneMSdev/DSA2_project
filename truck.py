from datetime import datetime, timedelta


class Truck:
    def __init__(self, truck_id, package_data):
        self.truck_id = truck_id
        self.packages = []  # List to store Package IDs
        self.hashmap = package_data  # Reference to hashmap object for updating
        self.current_location = ""
        self.current_time = "8:00 AM"
        self.distance_traveled = 0
        self.travel_time = 0
        self.speed = 18

    def load_package(self, package_id):
        """Load package onto truck by adding its ID to the list of packages"""
        package = self.hashmap.get(package_id)
        if package:
            self.packages.append(package_id)
            print(f"Package {package_id} loaded onto Truck {self.truck_id}")
        else:
            print(f"Package {package_id} not found in the HashMap.")

    def deliver_package(self, package_id, delivery_time):
        """Deliver a package and update its status and delivery time"""
        # self.current_location = self.hashmap.get
        new_status = "Delivered"
        if package_id in self.packages:
            self.hashmap.update_status(package_id, new_status)
            self.hashmap.update_time_delivered(package_id, delivery_time)
            print(f"Package {package_id} delivered at {delivery_time}")
        else:
            print(f"Package {package_id} not loaded on Truck {self.truck_id}")

    def calculate_travel_time(self, distance):
        # Calculate the time to travel the given distance at current speed
        travel_time_hours = distance / self.speed
        travel_time_minutes = round(travel_time_hours * 60)
        return travel_time_minutes

    def update_time(self, distance):
        # Calculate the minutes passed
        minutes_passed = self.calculate_travel_time(distance)

        # convert current_time to a datetime object
        time_format = "%I:%M %p"  # Time format to match ex: "8:00 AM"
        current_time_object = datetime.strptime(self.current_time, time_format)

        # Update the time by adding the minutes passed
        updated_time_object = current_time_object + timedelta(minutes=minutes_passed)

        # Convert updated time back to string format
        self.current_time = updated_time_object.strftime(time_format)

        return None
