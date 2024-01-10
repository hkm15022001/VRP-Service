import pandas as pd
import os

def get_city_coordinates(city_names):
    current_directory = os.path.dirname(__file__)
    file_path = os.path.join(current_directory, 'delivery_locations.csv')
    df = pd.read_csv(file_path)

    city_coordinates = []

    # Lặp qua danh sách tên thành phố
    for city_name in city_names:
        # Tìm tọa độ của thành phố
        city_data = df[df['City'] == city_name]
        if not city_data.empty:
            # Lấy tọa độ và thêm vào danh sách kết quả
            latitude = city_data['Latitude'].values[0]
            longitude = city_data['Longitude'].values[0]
            city_coordinates.append((latitude, longitude))

    return city_coordinates

def convert_paths_to_coordinates(paths):
    current_directory = os.path.dirname(__file__)
    file_path = os.path.join(current_directory, 'delivery_locations.csv')
    df = pd.read_csv(file_path)

    paths_coordinates = []

    # Duyệt qua từng đường đi trong paths
    for path in paths:
        cities = []
        # Thay thế "hub" bằng "Hà Nội" và trích xuất tên thành phố
        cities.extend([step.replace('hub', 'Hà Nội').split(' -> ')[1] for step in path])
        cities.insert(0, 'Hà Nội')
        # Lấy tọa độ của các thành phố trong danh sách cities
        city_coordinates = get_city_coordinates(cities)
        paths_coordinates.append(city_coordinates)

    return paths_coordinates

# Danh sách các đường đi
paths = [['hub -> Bắc Ninh', 'Bắc Ninh -> Bắc Giang', 'Bắc Giang -> Hải Dương', 'Hải Dương -> Hải Phòng', 'Hải Phòng -> Quảng Ninh'],
         ['hub -> Vĩnh Phúc', 'Vĩnh Phúc -> Phú Thọ', 'Phú Thọ -> Tuyên Quang', 'Tuyên Quang -> Bắc Kạn', 'Bắc Kạn -> Lạng Sơn', 'Lạng Sơn -> Hà Giang', 'Hà Giang -> Lào Cai', 'Lào Cai -> Lai Châu'],
         ['hub -> Hưng Yên', 'Hưng Yên -> Hà Nam', 'Hà Nam -> Nam Định', 'Nam Định -> Thái Bình', 'Thái Bình -> Ninh Bình', 'Ninh Bình -> Hòa Bình', 'Hòa Bình -> Sơn La', 'Sơn La -> Điện Biên']]

coordinates = convert_paths_to_coordinates(paths)
print(coordinates)