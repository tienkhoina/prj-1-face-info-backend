import os
import base64
from flask import request, jsonify
from datetime import datetime
from src.service.CRUDservice import check_exists_userId,insertFacecode,updateFaceCode
from src.algorithm.check_face_algorithm import get_face_embedding
from src.service.userservice import handleLogin
from sqlalchemy.orm import Session
from src.algorithm.check_face_algorithm import get_face_embedding 
from src.algorithm.base64_encode_decode import encode_embedding
from src.config.database import engine  # Import engine từ cấu hình database của bạn
from src.models.FaceInfo import FaceInfo  # Import model FaceInfo
from src.models.User import User
from datetime import datetime


def get_session():
    return Session(bind=engine)
def updateFace():
    try:
        # Lấy dữ liệu từ request
        data = request.get_json()
        image_base64 = data.get('image')  # Lấy chuỗi base64 từ data
        userId = data.get('userId')  # Lấy userId từ data

        if not image_base64 or not userId:
            return jsonify({"error": "Missing 'image' or 'userId' in request"}), 400

        # Đường dẫn thư mục lưu file ảnh
        image_dir = os.path.join(os.path.dirname(__file__), 'image')
        os.makedirs(image_dir, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại

        # Đường dẫn file ảnh
        image_path = os.path.join(image_dir, f"face{userId}.jpg")

        # Ghi chuỗi base64 thành file ảnh
        with open(image_path, "wb") as image_file:
            image_file.write(base64.b64decode(image_base64))
        emb =get_face_embedding(image_path=image_path)

        if emb is None:
            return jsonify({"message":"not have a face"}),200
        check = check_exists_userId(userId)
        if check:
            updateFaceCode(image_path,userId)
        else:
            insertFacecode(image_path,userId)
        return jsonify({"messeage":"OK"}),200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def Login():
    session = get_session()
    try:
        # Lấy dữ liệu từ request
        data = request.get_json()
        image_base64 = data.get('image')  # Lấy chuỗi base64 từ data
        

        if not image_base64:
            return jsonify({"error": "Missing 'image' in request"}), 400

        # Đường dẫn thư mục lưu file ảnh
        image_dir = os.path.join(os.path.dirname(__file__), 'image')
        os.makedirs(image_dir, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại

        # Tạo tên file ảnh với ngày giờ hiện tại
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = os.path.join(image_dir, f"login_{timestamp}.jpg")

        # Ghi chuỗi base64 thành file ảnh
        with open(image_path, "wb") as image_file:
            image_file.write(base64.b64decode(image_base64))
        emb =get_face_embedding(image_path)
        if emb is None:
            return jsonify({
                "name":"Not have a face",
                "email":"Not have a face"
            }),200
        
        userId = handleLogin(image_path)
        if userId == -1:
            return jsonify({
                "name":"Not found user",
                "email":"Not found user"
            }),200
        else:
            user = session.query(User).filter(User.id == userId).first()
            return jsonify({
                "id": userId,
                "name":user.firstName + ' ' + user.lastName,
                "email":user.email
            }),200
        

        

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Xóa file ảnh khi kết thúc
        if os.path.exists(image_path):
            os.remove(image_path)