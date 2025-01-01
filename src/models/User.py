from sqlalchemy import Column, String, Boolean, DateTime,Integer
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from src.config.database import Base  # Import Base từ file database.py

# Định nghĩa model User
class User(Base):
    __tablename__ = 'Users'  # Tên bảng trong cơ sở dữ liệu

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255))  # email kiểu String, với độ dài tối đa 255 ký tự
    password = Column(String(255))  # password kiểu String, với độ dài tối đa 255 ký tự
    firstName = Column(String(255))  # firstName kiểu String
    lastName = Column(String(255))  # lastName kiểu String
    address = Column(String(255))  # address kiểu String
    phonenumber = Column(String(20))  # phonenumber kiểu String (tối đa 20 ký tự)
    gender = Column(Boolean)  # gender kiểu Boolean
    image = Column(MEDIUMTEXT)  # image kiểu MEDIUMTEXT (chuỗi văn bản dài)
    roleId = Column(String(50))  # roleId kiểu String
    positionId = Column(String(50))  # positionId kiểu String
    createdAt = Column(DateTime)  # createdAt kiểu DateTime
    updatedAt = Column(DateTime)  # updatedAt kiểu DateTime

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, firstName={self.firstName}, lastName={self.lastName})>"
