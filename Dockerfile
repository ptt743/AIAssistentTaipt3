# Sử dụng image Python 3.11 bản slim để tối ưu dung lượng
FROM python:3.11-slim

# Thiết lập thư mục làm việc bên trong container
WORKDIR /app

# Copy file requirements vào trước để tận dụng cache của Docker
COPY requirements.txt .

# Cài đặt các thư viện
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn vào container
COPY . .

# Khai báo port mà container sẽ sử dụng
EXPOSE 8000

# Lệnh khởi động server bằng uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
