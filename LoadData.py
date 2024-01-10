import csv
from pathlib import Path
from Hub import Hub
from Package import Package
from DistanceGraph import DistanceGraph
from PackagePropertyTable import PackagePropertyTable
from Location import Location

hub = Hub()

with open(Path(__file__).parent/'Data/order.csv', mode='r',encoding='utf-8') as packages:
    package_list = hub.package_list
    package_reader = csv.reader(packages, delimiter=',')
    count = 0
    for row in package_reader:
        if count > 0:
            package_id = int(row[0])
            package = Package(package_id=row[0], package_weight=row[2], special_note=row[3],
                                    delivery_address=row[1])
            package_list.append(package) 
        count += 1
    print("So luong: ",count-1)

with open(Path(__file__).parent/'Data/distance_matrix1.csv', mode='r',encoding='utf-8') as distances:
    distance_graph = DistanceGraph()
    distance_reader = csv.reader(distances, delimiter=',')
    count = 0
    locations = []

    for row in distance_reader:
        if count > 0:
            address = str(row[0])
            # address = str(row[1])[1:-8]
            location = Location(address)

            if location.label == "Hà Nội":
                location.label = 'hub'
                distance_graph.hub_vertex = location
            distance_graph.add_vertex(location)
            for package in package_list:
                if package.delivery_address == location.label:
                    package.location = location 

            for path in range(3, len(row)):
                if row[path] == '0.0':
                    break
                else:
                    v = list(distance_graph.adjacency_list.keys())[path - 3]
                   
                    distance_graph.add_undirected_edge(location
                                                       , list(distance_graph.adjacency_list.keys())[path - 3]
                                                       , float(row[path]))

        count += 1

def load_packages():
    return package_list


def load_distances():
    return distance_graph


def main():
    # Your existing code here...

    loaded_packages = load_packages()
    loaded_distances = load_distances()

    # Display specific attributes of loaded packages
    # for package in loaded_packages:
    #     print(f"Package ID: {package.package_id}")
    #     print(f"Delivery Address: {package.delivery_address}")
    #     print(f"Delivery Location: {package.location}")
    #     # Print other relevant attributes...

    # for vertex, edges in distance_graph.adjacency_list.items():
    #     print(f"Các cạnh kề của đỉnh {vertex.label}:")
    #     for edge in edges:
    #         weight = distance_graph.edge_weights[(vertex, edge)]
    #         print(f"{vertex.label} - {edge.label}, Trọng số: {weight}")
    #     print()

if __name__ == "__main__":
    main()
