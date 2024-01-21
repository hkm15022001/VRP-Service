# Sử dụng Python Slim image thay vì Alpine để giảm dung lượng
FROM python:3.9.5-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy file requirements.txt vào thư mục /app
COPY requirements.txt .

# Cài đặt các dependencies từ requirements.txt
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install -r requirements.txt
# Copy tất cả các file còn lại trong thư mục hiện tại vào thư mục /app trong image
COPY . .

# Thiết lập biến môi trường PORT với giá trị 5555

# Copy entrypoint.sh vào thư mục làm việc
COPY entrypoint.sh /app/entrypoint.sh

# Thay đổi quyền cho entrypoint.sh để có thể thực thi
RUN chmod +x /app/entrypoint.sh

# Sử dụng entrypoint.sh làm lệnh CMD
CMD ["/app/entrypoint.sh"]