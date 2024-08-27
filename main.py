from data.hashmap import HashMap
from truck import Truck


"""Initialize Data Structures"""
package_data = HashMap()

"""Initialize Truck Instances"""
truck1 = Truck(1, package_data)
truck2 = Truck(2, package_data)
truck3 = Truck(3, package_data)


""" Testing """
load1 = ["1","2","3",]

for package in load1:
    truck1.load_package(package)

print(truck1.packages)
truck1.deliver_package("2", "10:00 AM")
print(truck1.packages)
print(package_data.get("2"))
