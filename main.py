from data.hashmap import HashMap
from truck import Truck

"""Initialize Data Structures"""
package_data = HashMap()
package_data.load_data_into_hashmap()

"""Initialize Truck Instances"""
truck1 = Truck(1, package_data)
truck2 = Truck(2, package_data)
truck3 = Truck(3, package_data)

load1 = ["1","2","3",]

for package in load1:
    truck1.load_package(package)

print(truck1.packages)
truck1.deliver_package("2", "10:00 AM")
print(truck1.packages)
print(package_data.get("2"))

# package_data.display()

# package_id = input("Which Package ID do you want to search for: ")
# print(packages.get(package_id))
# package_hashmap.display_package_data(package_id)
# packages.update_status("1", "delivered")
# packages.update_time_delivered("1", "10:15")
# packages.display_package_data("1")

