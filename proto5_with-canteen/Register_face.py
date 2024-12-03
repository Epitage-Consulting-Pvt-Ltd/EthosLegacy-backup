import cv2
import os

class FaceRegistration:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.camera = cv2.VideoCapture(0)  # Use the appropriate camera index if needed

    def capture_faces(self):
        face_id = input("Enter the ID for the person: ")
        name = input("Enter the name of the person: ")

        if not os.path.exists('dataset'):
            os.makedirs('dataset')

        count = 0
        while True:
            ret, frame = self.camera.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                count += 1
                cv2.imwrite(f'dataset/User.{face_id}.{count}.jpg', gray[y:y+h, x:x+w])

            cv2.imshow('Capturing Faces', frame)
            if cv2.waitKey(1) & 0xFF == ord('q') or count >= 30:
                break

        self.camera.release()
        cv2.destroyAllWindows()

        return face_id, name

# Usage
if __name__ == "__main__":
    face_registrator = FaceRegistration()
    face_id, name = face_registrator.capture_faces()
