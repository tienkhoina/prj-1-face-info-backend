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
    session = get_session()  # Lấy session
    try:
        # Lấy toàn bộ bản ghi từ bảng FaceInfo
        all_face_info = session.query(FaceInfo).all()
        for face_info in all_face_info:
            if get_distance_embedding(get_face_embedding(image_path),decode_embedding(face_info.faceCode))>=0.8:
                return face_info.userId
        return -1                

    except Exception as e:
        return f"Error: {e}"
    finally:
        # Đóng session
        session.close()
