import sqlite3
import csv
def fetch_order():
    # Kết nối đến cơ sở dữ liệu SQLite
    conn = sqlite3.connect('E:/scem-1/Supply-Chain-Event-Management/db/gorm.sqlite')
    cursor = conn.cursor()

    # Truy vấn dữ liệu vị trí từ cơ sở dữ liệu với trường area_code
    cursor.execute("SELECT id, receivers_address, weight, note FROM order_infos WHERE long_ship_id=0 and use_long_ship=1")
    rows = cursor.fetchall()

    # Tên file CSV để lưu dữ liệu
    csv_file = 'Data/order.csv'

    # Ghi dữ liệu vào file CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        
        # Viết header
        csv_writer.writerow(['Package ID', 'Address', 'Mass KILO', 'Special Note'])
        
        # Viết dữ liệu từ kết quả truy vấn
        csv_writer.writerows(rows)

    # Đóng kết nối cơ sở dữ liệu
    conn.close()
def clear_csv_file(file_path):
    with open(file_path, 'w', newline='') as csvfile:
        csvfile.truncate(0)  # Truncate file content
        # Nếu bạn muốn viết dòng header vào file sau khi xóa:
        # csv_writer = csv.writer(csvfile)
        # csv_writer.writerow(['Column1', 'Column2', 'Column3'])  # Ghi dòng header
