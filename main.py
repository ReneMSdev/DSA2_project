from data.packages import Packages
from truck import Truck
from datetime import datetime
from tabulate import tabulate

""" Global Variables """
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
TIME_FORMAT = "%I:%M %p"

"""Initialize Data Structures"""
package_data = Packages()  # pd for "package data"
start_time = datetime.strptime("8:00 AM", TIME_FORMAT)

"""Initialize Truck Instances"""
truck1 = Truck(1, package_data, start_time)
truck2 = Truck(2, package_data, start_time)


""" Testing """

"""Load Packages"""

truck1.load_packages(["1", "2", "3"])
truck2.load_packages(["4", "5", "6"])


""" Look up Function """


def lookup_packages_by_time(package_data, user_time):
    """Lookup packages statuses at given time """
    user_time_dt = datetime.strptime(user_time, TIME_FORMAT)
    lookup_results = []

    # Retrieve all packages sorted by package ID
    packages = package_data.get_all_packages()

    # Iterate over packages to determine status
    for package in packages:
        package_id = package[PACKAGE_ID]
        address = package[ADDRESS]
        time_loaded = package[TIME_LOADED]
        time_delivered = package[TIME_DELIVERED]

        # Convert times to datetime obj for comparison
        time_loaded_dt = datetime.strptime(time_loaded, TIME_FORMAT) if time_loaded else None
        time_delivered_dt = datetime.strptime(time_delivered, TIME_FORMAT) if time_delivered else None

        # Determine status based on user_time
        if not time_loaded:  # package has not been loaded yet
            status = "AT HUB"
            time_delivered_display = ""
        elif time_delivered_dt and user_time_dt >= time_delivered_dt:
            status = "DELIVERED"
            time_delivered_display = time_delivered
        else:
            truck_id = package[-1]
            status = f"ON TRUCK {truck_id}"
            time_delivered_display = ""

        # append results in following format:
        lookup_results.append([package_id, address, status, time_loaded, time_delivered_display])

    # print results in a table format
    print(tabulate(lookup_results, headers=["Package ID", "Address", "Status", "Time Loaded", "Time Delivered"]))


user_time = input("Enter a time ex: 08:30 AM | ")
lookup_packages_by_time(package_data, user_time)
