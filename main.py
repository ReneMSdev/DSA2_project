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
start_time1 = datetime.strptime("08:00 AM", TIME_FORMAT)
start_time2 = datetime.strptime("09:05 AM", TIME_FORMAT)

"""Initialize Truck Instances"""
truck1 = Truck(1, package_data, start_time1)
truck2 = Truck(2, package_data, start_time2)

# First load
load1_truck1 = ['1','6','13','14','15','16','19','20','29','30','31','34','37','40','2','4']
load1_truck2 = ['25','3','18','28','32','36','38','5','7','8','10','11','12','17']
truck1.load_packages(load1_truck1)
truck2.load_packages(load1_truck2)

# Second load
load2_truck1 = ['26','27','33','35','39']
load2_truck2 = ['9','21','22','23','24']
truck1.load_packages(load2_truck1)
truck2.load_packages(load2_truck2)

# Display truck reports
truck1.display_report()
print(" ")
truck2.display_report()


# Function to look up package statuses with user time as input
def lookup_packages_by_time(package_data, user_time):
    """Lookup packages statuses at given time """
    user_time_dt = datetime.strptime(user_time, TIME_FORMAT)
    lookup_results = []
    package_9_address_change_time = datetime.strptime("10:20 AM", TIME_FORMAT)

    # Retrieve all packages sorted by package ID
    packages = package_data.get_all_packages()

    # set to track processed package IDs to avoid duplicate displayed data
    processed_packages = set()

    # Iterate over packages to determine status
    for package in packages:
        package_id = package[PACKAGE_ID]

        # Skip duplicate package IDs
        if package_id in processed_packages:
            continue
        processed_packages.add(package_id)
        address = package[ADDRESS]
        time_loaded = package[TIME_LOADED]
        time_delivered = package[TIME_DELIVERED]

        # Convert times to datetime obj for comparison
        time_loaded_dt = datetime.strptime(time_loaded, TIME_FORMAT) if time_loaded else None
        time_delivered_dt = datetime.strptime(time_delivered, TIME_FORMAT) if time_delivered else None

        # Special case for package 9 address display
        if package_id == '9':
            if user_time_dt < package_9_address_change_time:
                address = '300 State St'
            else:
                address = '410 S State St'

        # Determine status based on user_time
        if not time_loaded:  # package has not been loaded yet
            status = "AT HUB"
            status_color = "\033[91m"  # Red
            time_loaded_display = ""
            time_delivered_display = ""
        elif time_loaded_dt and user_time_dt < time_loaded_dt:
            # user time is before the package was loaded
            status = "AT HUB"
            status_color = "\033[91m"  # Red
            time_loaded_display = ""
            time_delivered_display = ""
        elif time_delivered_dt and user_time_dt >= time_delivered_dt:
            status = "DELIVERED"
            status_color = "\033[92m"  # Green
            time_loaded_display = time_loaded
            time_delivered_display = time_delivered
        else:
            truck_id = package[-1]
            status = f"ON TRUCK {truck_id}"
            status_color = "\033[93m"  # Yellow
            time_loaded_display = time_loaded
            time_delivered_display = ""

        colored_row = [
            f"{status_color}{package_id}\033[0m",
            f"{status_color}{address}\033[0m",
            f"{status_color}{status}\033[0m",
            f"{status_color}{time_loaded_display}\033[0m",
            f"{status_color}{time_delivered_display}\033[0m"
        ]
        lookup_results.append(colored_row)

    # print results in a table format
    print(tabulate(lookup_results, headers=["Package ID", "Address", "Status", "Time Loaded", "Time Delivered"]))


user_time = input("\nEnter a time: ")
lookup_packages_by_time(package_data, user_time)

