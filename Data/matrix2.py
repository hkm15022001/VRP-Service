import sqlite3
import csv
from geopy.distance import geodesic

# Kết nối đến cơ sở dữ liệu SQLite
conn = sqlite3.connect('E:/scem-1/Supply-Chain-Event-Management/db/gorm.sqlite')
cursor = conn.cursor()

# Truy vấn dữ liệu vị trí từ cơ sở dữ liệu với trường area_code
cursor.execute("SELECT city, latitude, longitude, area_code, region FROM delivery_locations")
rows = cursor.fetchall()

# Chuyển dữ liệu từ cơ sở dữ liệu thành danh sách tuples, bao gồm area_code
locations = [(row[0], row[3], (row[1], row[2], row[4])) for row in rows]

# Sắp xếp lại locations theo Region
locations = sorted(locations, key=lambda x: x[2][2])

# Tạo ma trận khoảng cách
num_locations = len(locations)
distance_matrix = [[0] * num_locations for _ in range(num_locations)]

# Tính toán khoảng cách giữa các điểm và lưu vào ma trận khoảng cách
for i in range(num_locations):
    for j in range(num_locations):
        distance_matrix[i][j] = geodesic(locations[i][2][:2], locations[j][2][:2]).kilometers

# Đóng kết nối đến cơ sở dữ liệu
conn.close()

# Ghi ma trận khoảng cách vào file CSV với City names làm header và AreaCode, Region
with open('distance_matrix1.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Ghi hàng header với City names, AreaCode, Region
    header_row = ["", "AreaCode", "Region"] + [location[0] for location in locations]
    writer.writerow(header_row)

    # Ghi dữ liệu với City names, AreaCode, Region và giá trị khoảng cách
    for i, row in enumerate(distance_matrix):
        # Sắp xếp lại dữ liệu khoảng cách theo thứ tự của Region
        reordered_row = [row[locations.index(location)] for location in locations]
        data_row = [locations[i][0], locations[i][1], locations[i][2][2]] + reordered_row
        writer.writerow(data_row)

# In ra thông tin về ma trận
num_rows = len(distance_matrix)
num_columns = len(distance_matrix[0])

print(f"Số hàng: {num_rows}")
print(f"Số cột: {num_columns}")
print("Ma trận khoảng cách đã được ghi vào distance_matrix1.csv")
