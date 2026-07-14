import cv2
import os
import glob
from src.config import SAVE_DIR, MAX_IMAGES

class CameraManager:
    def __init__(self):
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)
        
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception("カメラに接続できませんでした。")

    def read_frame(self):
        ret, frame = self.cap.read()
        return ret, frame

    def draw_time(self, frame, display_time):
        cv2.putText(frame, display_time, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 3)
        cv2.putText(frame, display_time, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        return frame

    def draw_bbox(self, frame, x1, y1, x2, y2, confidence):
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
        label = f"HORNET: {confidence*100:.1f}%"
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        return frame

    def save_image(self, frame, filename):
        # 画質を50に落として保存し、ファイルサイズを劇的に軽くする処理
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
        cv2.imwrite(filename, frame, encode_param)
        
        # 古い画像の削除（ローテーション）
        files = sorted(glob.glob(os.path.join(SAVE_DIR, "*.jpg")))
        if len(files) > MAX_IMAGES:
            os.remove(files[0])

    def release(self):
        self.cap.release()