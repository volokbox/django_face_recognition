from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponse
from django.views.decorators import gzip
import cv2
import os
from screeninfo import get_monitors

# Página por defeito
def default_page(request):
    return HttpResponse("Reconhecimento Facial Executado")

# Página do Reconhecimento facial
def face_recognition(request):
    # atrinuit reconhecimento facial ao recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Abrir ficheiro treinado
    trainer_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trainer.yml')  # get current directory
    recognizer.read(trainer_path)

    # Abrir haarcascade ficherio
    face_cascade_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'haarcascade_frontalface_default.xml')  # get current directory
    faceCascade = cv2.CascadeClassifier(face_cascade_path)

    # Fonte da janela
    font = cv2.FONT_HERSHEY_SIMPLEX

    id = 0
    # names related to ids: The names associated to the ids: 1 for Mohamed, 2 for Jack, etc...
    #aluno = []
    #mycursor.execute("select nome from Aluno")
    #for i in mycursor:
    #    aluno += i
    names = ['None', 'Jose Conde', 'Barreto', 'Volodymyr'] # add a name into this list

    # Taxa de presença
    presence_rate = {0:0, 1:0, 2:0, 3:0}

    # Captura de Video
    cam = cv2.VideoCapture(0)

    # Resolução do Video
    cam.set(3, 853) 
    cam.set(4, 480)
    
    while True:
        # Captura um frame da camara
        ret, img = cam.read()

        # Converte a imagem para escala de cinza, para o reconhecimento facial ser executado corretamente
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Deteta caras na imagem
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=8,
            minSize=(30, 30),
        )

        # Para cada cara na imagem do frame
        for (x, y, w, h) in faces:
            # Desenha um retângulo à volta da cara
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Faz predict do rosto
            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

            # Verifica se a probabilidade do predict é alta suficiente
            if (confidence < 100):
                # Atualiza a taxa de presença associada ao id
                presence_rate[id] += 1
                id = names[id] # Mostra o nome através do id
                # Formata o valor da probabilidade
                confidence = "  {0}%".format(round(100 - confidence))

                # Adiciona o nome e a probabilidade à imagem no frame
                cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        # Meter em Full Screen o Reconhecimento Facial
        cv2.namedWindow("camera", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("camera", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN) 

        cv2.imshow('camera', img)    # Mostrar janela com o Reconhecimento Facial

        # Escape para sair da janela do Reconhecimento Facial
        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break

    print(presence_rate)

    cam.release()
    cv2.destroyAllWindows()
    return default_page(request)



def take_photos(request):
        # count faces in the db
        # Assuming the "images" directory is in the same directory as your current Python file
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images') 
        count = 0

        for path in os.listdir(image_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(image_path, path)):
                count += 1

        # if count equals zero, then faces = 0
        if(count != 0):
            faces = count/100
        else:
            faces = 0

        # Check if folder exists
        if not os.path.exists('images'):
            os.makedirs('images')

        face_cascade_Path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'haarcascade_frontalface_default.xml')
        faceCascade = cv2.CascadeClassifier(face_cascade_Path)

        # Check if the cascade was loaded successfully
        if faceCascade.empty():
            print("Error: Could not load the face cascade.")
            return HttpResponseServerError("Internal Server Error: Could not load the face cascade.")
        
        cam = cv2.VideoCapture(0)
        cam.set(3,640)
        cam.set(4,480)
        count = 0

        
        # For each person, enter one unique numeric face id
        face_id = faces + 1

        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
                count += 1
                # Save the captured image into the images directory
                cv2.imwrite("./images/Users." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
                cv2.imshow('image', img)
            # Press Escape to end the program.
            k = cv2.waitKey(100) & 0xff
            if k < 100:
                break
            # Take 30 face samples and stop video. You may increase or decrease the number of
            # images. The more the better while training the model.
            elif count >= 100:
                break

        cam.release()
        cv2.destroyAllWindows()

        return HttpResponse("Photos taken successfully")


