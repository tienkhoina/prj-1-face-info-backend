from sqlalchemy.orm import Session
from src.algorithm.check_face_algorithm import get_face_embedding,compare_faces_dlibs,get_distance_embedding
from src.algorithm.base64_encode_decode import encode_embedding,decode_embedding
from src.config.database import engine  # Import engine từ cấu hình database của bạn
from src.models.FaceInfo import FaceInfo  # Import model FaceInfo
from datetime import datetime

# Tạo session
def get_session():
    return Session(bind=engine)

# Hàm handleLogin
def handleLogin(image_path):
    session = get_session()
    try:
        # Lấy danh sách userId có faceCode gần giống với ảnh đầu vào
        face_embedding = get_face_embedding(image_path)  # Trích xuất embedding cho ảnh đầu vào
        all_face_info = session.query(FaceInfo).all()

        for face_info in all_face_info:
            decoded_face_code = decode_embedding(face_info.faceCode)
            distance = get_distance_embedding(face_embedding, decoded_face_code)
            
            if distance >= 0.8:  # Nếu khoảng cách nhỏ hơn 0.8, thì xác nhận người dùng
                return face_info.userId
        
        return -1  # Trả về -1 nếu không tìm thấy khớp

    except Exception as e:
        return f"Error: {e}"
    finally:
        session.close()
