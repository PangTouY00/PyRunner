# 使用官方的 Alpine Python 运行时作为父镜像
FROM python:3.8-alpine

# 设置工作目录
WORKDIR /usr/src/app

# 复制当前目录内容到容器中的 /usr/src/app 目录
COPY . .

# 更新 pip
RUN pip install --upgrade pip

# 安装lxml的依赖库
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    libxml2-dev \
    libxslt-dev

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 5000

# 运行应用
CMD ["python", "./app.py"]
