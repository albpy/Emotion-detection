import cv2
import numpy as np
from tensorflow.keras.models import load_model

model = load_model('emotions.h5')
emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

# the webcam feed
cap = cv2.VideoCapture(0)
facecasc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
while True:
    # Find haar cascade to draw bounding box around face
    ret, frame = cap.read()
    if not ret:
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facecasc.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=5)
    
     # Draw bounding boxes around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        face_gray = gray[y:y + h, x:x + w]
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(face_gray, (48, 48)), -1), 0)
        prediction = model.predict(cropped_img)
        emotion = int(np.argmax(prediction))
        cv2.putText(frame, emotion_dict[emotion], (x+30, y+60), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
    cv2.imshow('Video', cv2.resize(frame,(1080,720),interpolation = cv2.INTER_CUBIC))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()