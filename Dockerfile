# Sử dụng Python image
FROM python:3.10-slim

# Đặt biến môi trường
ENV PYTHONUNBUFFERED=1

# Cài đặt curl
RUN apt-get update && apt-get install -y curl

# Tạo và đặt thư mục làm việc
WORKDIR /app

# Sao chép requirements.txt và cài đặt các dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . /app/

# Mở cổng 8000 cho FastAPI
EXPOSE 8000
# Mở cổng 8089 cho Locust
EXPOSE 8089

# Chạy ứng dụng FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
