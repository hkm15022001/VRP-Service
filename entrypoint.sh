#!/bin/bash

# Chạy lệnh python app.py trong background (&) và lưu PID của quá trình này
python app.py &
APP_PID=$!

# Chạy lệnh python consumer.py trong foreground
python Event/consumer.py

# Sau khi consumer.py kết thúc, kill quá trình app.py
kill $APP_PID