""" Student ID: 011913812 """
from data.packages import Packages
from data.truck import Truck
from datetime import datetime
from data.lookup import lookup_packages_by_time

TIME_FORMAT = "%I:%M %p"

"""Initialize Data Structures"""
package_data = Packages()  # pd for "package data"
start_time1 = datetime.strptime("08:00 AM", TIME_FORMAT)
start_time2 = datetime.strptime("09:05 AM", TIME_FORMAT)

"""Initialize Truck Instances"""
truck1 = Truck(1, package_data, start_time1)
truck2 = Truck(2, package_data, start_time2)
truck3 = Truck(3, package_data, start_time1)

"""Load trucks and deliver routes"""
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

"""Display truck reports"""
truck1.display_report()
print(" ")
truck2.display_report()
print(" ")
truck3.display_report()

"""Look up address statuses with user input"""
while True:
    user_time = input("\nEnter a time (or 'q' to quit): ")
    if user_time.lower() == 'q':
        print("Exiting the program.")
        break
    # Validate time format
    try:
        # Attempt to parse time to ensure it's in the correct format
        datetime.strptime(user_time, TIME_FORMAT)
    except ValueError:
        print(f"Incorrect time format. Please enter the time in the format 'HH:MM am/pm'.")
        continue  # Ask for input again if the format is incorrect
    # Perform the lookup if the time format is correct
    lookup_packages_by_time(package_data, user_time)
    another_search = input("\nWould you like to search for another time? (yes/no): ")
    if another_search.lower() not in ['yes','y']:
        print("Exiting the program.")
        break

