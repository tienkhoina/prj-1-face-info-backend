from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
from pathlib import Path
import logging
from datetime import datetime
from src.controller.userController import Login, updateFace

# Cấu hình logging
logging.basicConfig(level=logging.DEBUG)

# Khởi tạo Flask app
app = Flask(__name__)

# Kích hoạt CORS (để API có thể được gọi từ các domain khác)
CORS(app)

# Route cho API login (POST)
@app.route('/api/login', methods=['POST'])
def login():
    return Login()

# Route cho API update face code (POST)
@app.route('/api/update-face', methods=['POST'])
def update_face():
    return updateFace()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2902)
