from data.packages import Packages
from truck import Truck
from datetime import datetime


"""Initialize Data Structures"""
package_data = Packages()
start_time = datetime.strptime("8:00 AM", "%I:%M %p")

"""Initialize Truck Instances"""
truck1 = Truck(1, package_data, start_time)
truck2 = Truck(2, package_data, start_time)


""" Testing """

"""Load Packages"""

# Divide the packages between the trucks (roughly 13 packages per truck)
truck1.load_packages(["1", "2", "3"])
truck2.load_packages(["4", "5", "6"])

print(package_data.get_package_data("1"))
print(package_data.get_package_data("2"))
print(package_data.get_package_data("3"))
print(package_data.get_package_data("4"))
print(package_data.get_package_data("5"))
print(package_data.get_package_data("6"))





