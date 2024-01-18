from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
import cv2
import os
from screeninfo import get_monitors


# Página do Reconhecimento facial
def face_recognition(request):
    # Your existing face recognition code here
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Abrir ficheiro treinado
    trainer_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trainer.yml')  # get current directory
    recognizer.read(trainer_path)

    # Abrir haarcascade ficherio
    face_cascade_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'haarcascade_frontalface_default.xml')  # get current directory
    faceCascade = cv2.CascadeClassifier(face_cascade_path)

    font = cv2.FONT_HERSHEY_SIMPLEX

    id = 0
    # names related to ids: The names associated to the ids: 1 for Mohamed, 2 for Jack, etc...
    #aluno = []
    #mycursor.execute("select nome from Aluno")
    #for i in mycursor:
    #    aluno += i
    names = ['None', 'Jose Conde', 'Barreto', 'Volodymyr'] # add a name into this list
    presence_rate = {0:0, 1:0, 2:0, 3:0}
    #Video Capture
    cam = cv2.VideoCapture(0)
    for monitor in get_monitors():
        width = monitor.width
        height = monitor.height

    cam.set(3, width)
    cam.set(4, height)
    # Min Height and Width for the  window size to be recognized as a face
    #minW = 0.1 * cam.get(3)
    #minH = 0.1 * cam.get(4)
    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=8,
            minSize=(30, 30),
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            if (confidence < 100):
                presence_rate[id] += 1
                id = names[id]
                confidence = "  {0}%".format(round(100 - confidence))
                cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
                
        cv2.imshow('camera', img)
        # Escape to exit the webcam / program
        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break

    print(presence_rate)

    cam.release()
    cv2.destroyAllWindows()
    #return render(request, 'your_template.html', {'presence_rate': presence_rate})


