# James Clair, 000847594

import copy
import LoadData
import Time
import ShortestPath

from Hub import Hub
from Truck import Truck
from Package import Package
from Location import Location
from Data.PathToCoordinates import convert_paths_to_coordinates
from Data.visualize import visualize
def check_status(current_time, hub, packages):
    print()
    packages_by_status = hub.get_packages_by_status(packages)
    if ((Time.get_hours_float('8:35:00') <= current_time <= Time.get_hours_float('9:25:00') and hub.count == 0) or (
            Time.get_hours_float('9:35:00') <= current_time <= Time.get_hours_float('10:25:00') and hub.count == 1) or (
            Time.get_hours_float('12:03:00') <= current_time <= Time.get_hours_float('13:12:00') and hub.count == 2)):
        print('*** {0} Status Check ***'.format(Time.get_formatted_time(current_time)))
        print()
        print('loaded: ', end="")
        if packages_by_status.read('loaded') is not None:
            for package in packages_by_status.read('loaded'):
                print(package.package_id, end=", ")
        print()
        print('delivered: ', end="")
        for package in packages_by_status.read('delivered'):
            print(package.package_id, end=", ")
        print('\n*** End of Status check ***\n')
        hub.count = hub.count + 1


# Total runtime complexity = O(N) + O(N^3) + O(N^3) + O(N^3) = O(N^3)
def process_optimize():
    packages = LoadData.load_packages()
    distance_graph = LoadData.load_distances()

    hub = Hub()
    print("<------------Processing and loading special packages on trucks---------------->")
    trucks = [Truck(1, hub.drivers[0]), Truck(2, hub.drivers[1]), Truck(3),Truck(4)]
    packages_by_id = hub.get_packages_by_id(packages)
    unloaded_packages = []

    # Run-time complexity: O(N) * O(1) = O(N)
    for package in packages:
        print("Package: ", package.package_id, "and special note: ", package.special_note)
       
        if package.delivery_status == 'loaded':
           print("    result: ", package.package_id, "Has already been loaded.  Nothing to do.") 
        else:
            print("    result: ", package.package_id, "Not special, will be loaded after special packages are processed/loaded.")
            unloaded_packages.append(package)
    print("<------------Special packages loaded---------------->\n")
    
    # load all remainder of packages on trucks optimized for distance
    print("<------------Load packages---------------->")
    packages_by_address = hub.get_packages_by_address(unloaded_packages)
    loaded_packages = []
    # O(N) * (O(1) + O(N^2) + O(N) + O(1)) = O(N^3)
    while len(unloaded_packages) > 0:
        for truck in trucks:
            if len(unloaded_packages) == 0:
                break
            # if it's the trucks first iteration
            if truck.current_location == None:
                # set the trucks starting location
                truck.current_location = distance_graph.hub_vertex
            for v in distance_graph.adjacency_list:
                v.distance = float('inf')
                v.predecessor = None
            ShortestPath.dijkstra_shortest_path(distance_graph, truck.current_location)
            # find the location with the next closest distance
            closest_distance = float('inf')
            smallest = None
            # Run-time complexity: O(N)
            # print(len(unloaded_packages))
            for i in range(0, len(unloaded_packages)):
                if unloaded_packages[i].location.distance == float('inf'):
                    print("Package that inf",unloaded_packages[i])
                    
                if unloaded_packages[i].location.distance < closest_distance:
                    smallest = i
                    closest_distance = unloaded_packages[i].location.distance

            #check tinh dung dan 
            closest_truck_distance = float('inf')
            for other_truck in trucks:
                if other_truck.skip == False and other_truck != truck and other_truck.current_location != None:  # Không so sánh với chính xe đang xét
                    distance_to_truck = distance_graph.edge_weights[(unloaded_packages[smallest].location,other_truck.current_location)]
                    if distance_to_truck < closest_truck_distance:
                        closest_truck_distance = distance_to_truck
            if(closest_distance > closest_truck_distance):
                continue
            packages_at_stop = packages_by_address.read(unloaded_packages[smallest].location.label)
            if len(packages_at_stop) < (truck.MAX_LOAD - truck.package_count):
                starting_location = truck.current_location
                truck.current_location = unloaded_packages[smallest].location
                
                # load all packages at this address
                # run-time complexity O(1)
                for package in packages_at_stop:
                    print("Package: ", package.package_id, package.location.label)
                    if package.location.label == truck.current_location.label and truck.load_on_truck(package) and package not in loaded_packages:
                        loaded_packages.append(package)
                        unloaded_packages.remove(package)
                        truck.packages_list.append(package.package_id)
            
            else:
                truck.skip = True
                continue

    package_list_result={}
    for truck in trucks:
        package_list_result[truck.truck_id] = truck.packages_list
    print("<------------All packages loaded---------------->\n")

    # deliver all packages calculating distance
    print("<------------Deliver packages---------------->\n")
    trucks[0].start_time = hub.start_time
    trucks[1].start_time = Time.get_hours_float('09:05:00')
    trucks[2].start_time = max(min(trucks[0].time, trucks[1].time), Time.get_hours_float('10:20:00'))
    count = 0
    package_ids = []
   

    for truck in trucks:
        print("<------------Deliver Truck: ", truck.truck_id, " packages---------------->")
        packages_by_address = hub.get_packages_by_address(truck.delivery_queue)
        truck.current_location = distance_graph.hub_vertex
        # O(N) * (O(1) + O(N^2) + O(N) + O(1)) = O(N^3))
        while len(truck.delivery_queue) > 0:
            # Run-time complexity: O(1)
            for v in distance_graph.adjacency_list:
                v.distance = float('inf')
                v.predecessor = None
            # Using a simple list so O(N^2) runtime complexity
            ShortestPath.dijkstra_shortest_path(distance_graph, truck.current_location)
            # find the location with the next closest distance
            closest_distance = float('inf')
            smallest = None
            # Run-time complexity: O(N)
            for i in range(0, len(truck.delivery_queue)):
                if truck.delivery_queue[i].location.distance < closest_distance:
                    smallest = i
                    closest_distance = truck.delivery_queue[i].location.distance
            starting_location = truck.current_location
            truck.current_location = truck.delivery_queue[smallest].location
            truck.distance += closest_distance
            truck.time = truck.start_time + (truck.distance / truck.AVG_MPH)
            check_status(truck.time, hub, packages)
            truck.path.append(ShortestPath.get_shortest_path(starting_location, truck.current_location))

            for package in packages_by_address.read(truck.current_location.label):
                if package.location.label == truck.current_location.label:
                    truck.delivery_queue.remove(package)
                    package.deliver_package(truck.time)
                    package_ids.append(package.package_id)
                    count += 1
                    print(package, "\n")

        truck.time = truck.start_time + (truck.distance / truck.AVG_MPH)
        print("<------------Truck: ", truck.truck_id, " packages delivered---------------->\n")

    # report time finished and distance of each truck and total distance of all trucks
    total_distance = trucks[0].distance + trucks[1].distance + trucks[2].distance
    print("Total Distance", total_distance)
    truck_path=[]
    for truck in trucks:
        truck_path.append(truck.path)
    # visualize(truck_path)
    print(truck_path)
    coordinates_path = convert_paths_to_coordinates(truck_path)
    return total_distance,package_list_result,truck_path,coordinates_path
    
    # TODO: An interface that allows the user to enter a time to check the status of a package or all packages at a given time is not readily evident
    # print("<----------------------------STATUS CHECK------------------------------>")
    # print()
    # user_time_fmt = input("To check the delivery status, please enter a time in HH:MM:SS format: ")
    # user_time = Time.get_hours_float(user_time_fmt)
    # delivered_packages = []
    # undelivered_packages = []
    # for package in packages:
    #     if package.arrival_time < user_time:
    #         delivered_packages.append(package)
    #     else:
    #         undelivered_packages.append(package)

    # print("<-----------Delivered packages, at", user_time_fmt, "---------->")
    # for package in delivered_packages:
    #     print(
    #         "package_id: ", package.package_id,
    #         ", truck: ", package.truck_id,
    #         ", status: delivered",
    #         ", address: ", package.delivery_address,
    #         ", weight: ", package.package_weight,
    #         ", time delivered: ", Time.get_formatted_time(package.arrival_time)
    #         )
    # print("\n")
    # print("<-----------Undelivered packages, at", user_time_fmt, "---------->")
    # for package in undelivered_packages:
    #     print(
    #         "package_id: ", package.package_id,
    #         ", truck: ", package.truck_id,
    #         ", status: undelivered",
    #         ", address: ", package.delivery_address,
    #         ", weight: ", package.package_weight,
    #         ", time delivered: ", Time.get_formatted_time(package.arrival_time)

    #         )
    # print("\n")
            
    # final_report = input("Show FINAL REPORT? (y/n): ")
    # if final_report == "y":
    #     print("<----------------------------FINAL REPORT------------------------------>\n")
    #     print("Total # of packages delivered: ", count)
    #     print("Total distance traveled: ", total_distance, "\n")
    
    #     print("<------------Truck 1---------------->")
    #     print("Total distance: ", trucks[0].distance)
    #     print("Time Finished: ", Time.get_formatted_time(trucks[0].time), "\n")
    #     print(trucks[0].path)

    #     print("<------------Truck 2---------------->")
    #     print("Total distance: ", trucks[1].distance)
    #     print("Time Finished: ", Time.get_formatted_time(trucks[1].time), "\n")
    #     print(trucks[1].path)

    #     print("<------------Truck 3---------------->")
    #     print("Total distance: ", trucks[2].distance)
    #     print("Time Finished: ", Time.get_formatted_time(trucks[2].time), "\n")
    #     print(trucks[2].path)
    # else:
    #     print("Skipping Final Report")

if __name__ == "__main__":
    process_optimize()
    