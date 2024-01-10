import pandas as pd
import folium
from geopy.geocoders import Nominatim
import os
def visualize(paths):

    # Màu cho từng path
    colors = ['blue', 'green', 'red','yellow','black','pink']

    current_directory = os.path.dirname(__file__)
    file_path = os.path.join(current_directory,  'delivery_locations.csv')
    df = pd.read_csv(file_path)

    # Tạo bản đồ
    m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=7)

    # Tạo một geolocator để tìm các địa điểm
    geolocator = Nominatim(user_agent="geoapiExercises")

    # Duyệt qua từng path và tạo đường đi trên bản đồ
    for idx, path in enumerate(paths):
        # Thay thế "hub" bằng "Hà Nội"
        cities = [step.replace('hub', 'Hà Nội').split(' -> ')[1] for step in path]
        cities.insert(0, 'Hà Nội')
        # Tạo đường đi dựa trên path của xe
        for i in range(len(cities) - 1):
            start = df.loc[df['City'] == cities[i]]
            end = df.loc[df['City'] == cities[i + 1]]

            start_location = (start['Latitude'].values[0], start['Longitude'].values[0])
            end_location = (end['Latitude'].values[0], end['Longitude'].values[0])

            folium.Marker(start_location, popup=cities[i]).add_to(m)
            folium.Marker(end_location, popup=cities[i + 1]).add_to(m)
            folium.PolyLine(locations=[start_location, end_location], color=colors[idx]).add_to(m)

    # Lưu bản đồ vào một file HTML để xem
    m.save("templates/route_map.html")
    print("save route!!")