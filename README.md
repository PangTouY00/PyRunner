# Online Python IDE

这是一个基于 Flask 的在线 Python IDE，允许用户在浏览器中编写和运行 Python 代码。用户还可以安装 Python 模块，并将生成的文件保存到一个特定的目录中。

## 功能

- 在线编写和运行 Python 代码
- 安装 Python 模块
- 将生成的文件保存到一个特定的目录中
- 支持多架构（AMD64 和 ARMv7）

## 项目结构

```plaintext
PyRunner/
├── .dockerignore
├── .github/
│   └── workflows/
│       └── docker-publish.yml
├── Dockerfile
├── app.py
├── index.html
├── requirements.txt
└── README.md
```

## 快速开始
## 1. 克隆项目
```git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
## 2. 构建 Docker 镜像
```
docker build -t your-dockerhub-username/pyrunner:latest .
```
## 3. 运行 Docker 容器
```
docker run -p 5000:5000 -v $(pwd)/output:/app/output your-dockerhub-username/pyrunner:latest
```
或直接用现成的
```
docker run -d \
  --restart unless-stopped \
  --name pyrunner \
  -p 5022:5000 \
  w1770946466/pyrunner:latest
```

## 4. 访问应用
在浏览器中访问 http://localhost:5000，你应该能够看到你的 Flask 应用正在运行。

## 使用说明
## 运行代码
在代码编辑器中输入 Python 代码。

点击“Run Code”按钮运行代码。

输出结果将显示在“Output”区域。

## 安装模块
点击“Install Module”按钮。

在弹出的输入框中输入模块名称。

点击“Install Module”按钮安装模块。

安装结果将显示在“Output”区域。

## 贡献
欢迎贡献代码！请 fork 仓库并提交 Pull Request。

## 许可证
本项目采用 MIT 许可证。有关更多信息，请参阅 LICENSE 文件。
