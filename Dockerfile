# 使用官方的 Python 基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录下的所有文件到容器中的 /app 目录
COPY . /app

# 创建并激活虚拟环境
RUN python3 -m venv venv

# 激活虚拟环境并安装依赖
RUN . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

# 暴露端口
EXPOSE 5000

# 设置环境变量
ENV FLASK_APP=app.py

# 运行 Flask 应用
CMD ["venv/bin/python", "-m", "flask", "run", "--host=0.0.0.0"]
