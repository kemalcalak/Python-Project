import cv2
from deepface import DeepFace

cap = cv2.VideoCapture(0)

# Duygulara karşılık gelen emoji görüntüleri
emojis = {
    "angry": cv2.imread("emojipng/angry.png"),
    "disgust": cv2.imread("emojipng/disgust.png"),
    "fear": cv2.imread("emojipng/fear.png"),
    "happy": cv2.imread("emojipng/happy.png"),
    "sad": cv2.imread("emojipng/sad.png"),
    "surprise": cv2.imread("emojipng/surprise.png"),
    "neutral": cv2.imread("emojipng/neutral.png")
}

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Yüz tespiti yap
    faces = face_cascade.detectMultiScale(frame, 1.1, 4)

    # Yüz tespit edildiyse
    if len(faces) > 0:
        cv2.putText(frame, "Yuz tespit edildi", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        
        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            dominant_emotion = result[0]["dominant_emotion"]
            
            # Emoji görüntüsünü yeniden boyutlandır
            emoji_resized = cv2.resize(emojis[dominant_emotion], (100, 100))  # 100x100 boyutunda bir emoji boyutu belirledim. İstediğiniz boyuta göre ayarlayabilirsiniz.
            
            # "Yüz Var" yazısının hemen altına emoji görüntüsünü çiz
            frame[40:140, 10:110] = emoji_resized
        except Exception as e:
            print(e)
    else:
        cv2.putText(frame, "Yuz tespit edildi", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    cv2.imshow('Duygu Tespiti @drmurataltun', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
