from data.hashmap import HashMap
from truck import Truck
from data.timestamps import Timestamps


def lookup_status(timestamps, lookup_time):
    snapshot = timestamps.get_snapshot(lookup_time)
    if snapshot == "No data available for this time.":
        print(snapshot)
    else:
        print(f"Statuses at {lookup_time}")
        print("-------------------------------------")
        # Sort the snapshot dictionary by package ID
        sorted_snapshot = dict(sorted(snapshot.items(), key=lambda item: int(item[0])))
        for package_id, data in sorted_snapshot.items():
            status = data['status'].upper()
            print(f"Package {package_id} - Status: {status}, Time Delivered: {data['time_delivered']}")


"""Initialize Data Structures"""
package_data = HashMap()
timestamps = Timestamps()

"""Initialize Truck Instances"""
truck1 = Truck(1, package_data, timestamps)
truck2 = Truck(2, package_data, timestamps)
truck3 = Truck(3, package_data, timestamps)


""" Testing """
truck1.load_packages(["1","2","3"])
truck2.load_packages(["4","5","6"])

route1 = truck1.calculate_route()
route2 = truck2.calculate_route()
truck1.deliver_all_packages(route1)
truck2.deliver_all_packages(route2)

lookup_time = "08:25 AM"
lookup_status(timestamps, lookup_time)
# print(package_data.display())

