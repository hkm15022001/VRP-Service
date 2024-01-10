import sqlite3
import csv

# Kết nối đến cơ sở dữ liệu SQLite
conn = sqlite3.connect('E:/scem-1/Supply-Chain-Event-Management/db/gorm.sqlite')
cursor = conn.cursor()

# Truy vấn dữ liệu vị trí từ cơ sở dữ liệu với trường area_code
cursor.execute("SELECT city, latitude, longitude, area_code, region FROM delivery_locations")
rows = cursor.fetchall()

# Tên file CSV để lưu dữ liệu
csv_file = 'delivery_locations.csv'

# Ghi dữ liệu vào file CSV
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    csv_writer = csv.writer(file)
    
    # Viết header
    csv_writer.writerow(['City', 'Latitude', 'Longitude', 'Area_Code', 'Region'])
    
    # Viết dữ liệu từ kết quả truy vấn
    csv_writer.writerows(rows)

# Đóng kết nối cơ sở dữ liệu
conn.close()
