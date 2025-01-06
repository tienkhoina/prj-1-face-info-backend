import dlib
import cv2
import numpy as np
from pathlib import Path

# Tạo đường dẫn đến mô hình bằng pathlib
model_path = Path(__file__).resolve().parent / "dlib_face_recognition_resnet_model_v1.dat"

# Kiểm tra xem mô hình có tồn tại không
if not model_path.is_file():
    raise FileNotFoundError(f"Không tìm thấy mô hình tại {model_path}")

# Tải mô hình nhận diện khuôn mặt
face_rec_model = dlib.face_recognition_model_v1(str(model_path))

# Tải mô hình phát hiện khuôn mặt
face_detector = dlib.get_frontal_face_detector()

shape_path = Path(__file__).resolve().parent / "shape_predictor_5_face_landmarks.dat"

def preprocess_with_dlib(image_path):
    """
    Dò và cắt khuôn mặt từ ảnh sử dụng dlib, sau đó trả về tensor.
    """
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    faces = face_detector(image, 1)

    if len(faces) == 0:
        print("Không phát hiện được khuôn mặt.")
        return None

    # Chọn khuôn mặt đầu tiên
    shape_predictor = dlib.shape_predictor(str(shape_path))
    face = dlib.get_face_chip(image, shape_predictor(image, faces[0]))
    return face

def get_face_embedding(image_path):
    """
    Trích xuất embedding của khuôn mặt từ ảnh.
    """
    face = preprocess_with_dlib(image_path)
    if face is None:
        print("Không phát hiện được khuôn mặt.")
        return None

    # Trích xuất đặc trưng khuôn mặt
    embedding = np.array(face_rec_model.compute_face_descriptor(face))
    return embedding

def compare_faces_dlibs(image1_path, image2_path, threshold=0.8):
    """
    So sánh hai khuôn mặt sử dụng Cosine Similarity.
    """
    emb1 = get_face_embedding(image1_path)
    emb2 = get_face_embedding(image2_path)

    if emb1 is None or emb2 is None:
        print("Không thể trích xuất embedding từ một trong hai ảnh.")
        return False

    similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
    print(f"Độ tương đồng cosine giữa hai khuôn mặt: {similarity}")
    return similarity > threshold

def get_distance_embedding(emb1, emb2):
    """
    Tính toán độ tương đồng giữa hai embedding.
    """
    similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
    return similarity
