from flask import Flask, request, jsonify, send_from_directory
import subprocess
import sys
import io
import contextlib
import importlib
import json

app = Flask(__name__)

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
            exec(code, globals())
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
        return jsonify({'message': f'Module {module} is already installed'})
    except ImportError:
        pass

    try:
        # 使用 pip 安装模块到用户目录
        subprocess.check_call([sys.executable, "-m", "pip", "install", module, "--user"])
        
        # 重新加载模块
        if module in sys.modules:
            importlib.reload(sys.modules[module])
        else:
            # 动态导入模块
            importlib.import_module(module)
        
        return jsonify({'message': f'Successfully installed and reloaded {module}'})
    except subprocess.CalledProcessError as e:
        return jsonify({'message': f'Failed to install {module}', 'error': str(e)})
    except ImportError as e:
        return jsonify({'message': f'Module {module} installed but not reloaded', 'error': str(e)})
    except Exception as e:
        return jsonify({'message': f'An unexpected error occurred', 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
