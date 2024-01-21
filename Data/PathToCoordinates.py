import os
import csv

def read_csv(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data

def get_city_coordinates(city_names, data):
    city_coordinates = []

    for city_name in city_names:
        for row in data:
            if row['City'] == city_name:
                latitude = float(row['Latitude'])
                longitude = float(row['Longitude'])
                city_coordinates.append((latitude, longitude))
                break

    return city_coordinates

def convert_paths_to_coordinates(paths, data):
    paths_coordinates = []

    for path in paths:
        cities = [step.replace('hub', 'Hà Nội').split(' -> ')[1] for step in path]
        cities.insert(0, 'Hà Nội')
        city_coordinates = get_city_coordinates(cities, data)
        paths_coordinates.append(city_coordinates)

    return paths_coordinates

# Đọc dữ liệu từ tệp CSV
current_directory = os.path.dirname(__file__)
file_path = os.path.join(current_directory, 'delivery_locations.csv')
data = read_csv(file_path)

# Danh sách các đường đi
paths = [['hub -> Bắc Ninh', 'Bắc Ninh -> Bắc Giang', 'Bắc Giang -> Hải Dương', 'Hải Dương -> Hải Phòng', 'Hải Phòng -> Quảng Ninh'],
         ['hub -> Vĩnh Phúc', 'Vĩnh Phúc -> Phú Thọ', 'Phú Thọ -> Tuyên Quang', 'Tuyên Quang -> Bắc Kạn', 'Bắc Kạn -> Lạng Sơn', 'Lạng Sơn -> Hà Giang', 'Hà Giang -> Lào Cai', 'Lào Cai -> Lai Châu'],
         ['hub -> Hưng Yên', 'Hưng Yên -> Hà Nam', 'Hà Nam -> Nam Định', 'Nam Định -> Thái Bình', 'Thái Bình -> Ninh Bình', 'Ninh Bình -> Hòa Bình', 'Hòa Bình -> Sơn La', 'Sơn La -> Điện Biên']]

coordinates = convert_paths_to_coordinates(paths, data)
print(coordinates)
