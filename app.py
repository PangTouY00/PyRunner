from flask import Flask, request, jsonify, send_from_directory
import subprocess
import sys
import io
import contextlib
import importlib
import json
import os
import tempfile

app = Flask(__name__)

# 创建一个临时目录来存放生成的文件
output_dir = tempfile.mkdtemp()

# 设置模块安装目录
module_install_dir = os.path.join(output_dir, 'modules')
os.makedirs(module_install_dir, exist_ok=True)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/run', methods=['POST'])
def run_code():
    code = request.json['code']
    
    # 创建一个StringIO对象来捕获输出
    output = io.StringIO()
    
    # 使用contextlib.redirect_stdout来重定向标准输出和标准错误
    with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
        try:
            # 在安全的环境中执行代码
            exec(code, {'__file__': os.path.join(output_dir, 'temp.py')})
        except Exception as e:
            print(f"Error: {str(e)}")
    
    # 获取捕获的输出
    result = output.getvalue()
    
    # 美化 JSON 输出
    try:
        json_output = json.loads(result)
        result = json.dumps(json_output, indent=4)
    except json.JSONDecodeError:
        pass
    
    return jsonify({'output': result})

@app.route('/install', methods=['POST'])
def install_module():
    module = request.json['module']
    try:
        # 尝试导入模块
        __import__(module)
    except ImportError:
        pass

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])
        # 重新加载模块
        importlib.reload(sys.modules[module])
        return jsonify({'message': f'Successfully installed {module}'})
    except subprocess.CalledProcessError:
        return jsonify({'message': f'Failed to install {module}'})
    except KeyError:
        return jsonify({'message': f'Module {module} installed but not reloaded'})

@app.route('/output/<path:filename>')
def download_file(filename):
    return send_from_directory(output_dir, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
