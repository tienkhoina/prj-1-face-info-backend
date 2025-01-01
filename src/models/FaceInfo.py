from sqlalchemy import Column, Integer, String,DateTime
from sqlalchemy.dialects.mysql import MEDIUMTEXT  # Import MEDIUMTEXT từ MySQL dialect
from src.config.database import Base  # Import Base từ file database.py

# Định nghĩa model FaceInfo
class FaceInfo(Base):
    __tablename__ = 'FaceInfo'  # Tên bảng trong cơ sở dữ liệu

    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer)  # userId là kiểu Integer
    faceCode = Column(MEDIUMTEXT)  # faceCode là kiểu MEDIUMTEXT
    createdAt = Column(DateTime)  # createdAt kiểu DateTime
    updatedAt = Column(DateTime)  # updatedAt kiểu DateTime


    def __repr__(self):
        return f"<FaceInfo(id={self.id}, userId={self.userId}, faceCode={self.faceCode})>"
