from sqlalchemy.orm import Session
from src.algorithm.check_face_algorithm import get_face_embedding 
from src.algorithm.base64_encode_decode import encode_embedding
from src.config.database import engine  # Import engine từ cấu hình database của bạn
from src.models.FaceInfo import FaceInfo  # Import model FaceInfo
from datetime import datetime

# Tạo một session factory
def get_session():
    return Session(bind=engine)

def check_exists_userId(userId):
    session = get_session()
    try:
        
        face_info = session.query(FaceInfo).filter(FaceInfo.userId == userId).first()

        if not face_info:
            return False
        return True
    except Exception as e:
        session.rollback()
        return f"Error: {e}"
    finally:
        session.close() 

def insertFacecode(image_path, userId):
    """
    Thêm faceCode vào cơ sở dữ liệu.
    """
    session = get_session()  # Tạo session
    try:
        embedding1 = get_face_embedding(image_path)
        baseString = encode_embedding(embedding1)

        new_face_info = FaceInfo(
            userId=userId,
            faceCode=baseString,
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow(),
        )

        session.add(new_face_info)
        session.commit()
        return "OK"
    except Exception as e:
        session.rollback()
        return f"Error: {e}"
    finally:
        session.close()

def updateFaceCode(image_path, userId):
    """
    Cập nhật faceCode cho một userId đã tồn tại.
    """
    session = get_session()  # Tạo session
    try:
        embedding1 = get_face_embedding(image_path)
        baseString = encode_embedding(embedding1)

        # Tìm bản ghi theo userId
        face_info = session.query(FaceInfo).filter(FaceInfo.userId == userId).first()

        if not face_info:
            return f"Error: FaceInfo with userId={userId} not found."

        # Cập nhật faceCode
        face_info.faceCode = baseString
        face_info.updatedAt = datetime.utcnow()  # Cập nhật thời gian

        session.commit()
        return "OK"
    except Exception as e:
        session.rollback()
        return f"Error: {e}"
    finally:
        session.close()
