from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponse, HttpResponseServerError
from django.views.decorators import gzip
import cv2
import os
from screeninfo import get_monitors
from PIL import Image
import numpy as np

# Página por defeito
def default_page(request):
    return HttpResponse("Reconhecimento Facial Executado")

# Página do Reconhecimento facial
def face_recognition(request):
    # Atribuir o reconhecimento facial ao recognizer
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

    #aluno = []
    #mycursor.execute("select nome from Aluno")
    #for i in mycursor:
    #    aluno += i

    names = ['None', 'Jose Conde', 'Barreto', 'Volodymyr'] # add a name into this list

    # Taxa de presença
    presence_rate = {0:0, 1:0, 2:0, 3:0}

    # Captura de Video
    cam = cv2.VideoCapture(0)

    # Resolução do Video 16:9
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


# Página para tirar fotografias das caras
def take_photos(request):
        # Contar número de fotogradias na pasta  
        # Encontrar a pasta das imagens das caras
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images') 
        count = 0

        # Para caminho na pasta        
        for path in os.listdir(image_path):
            # Verifica se o caminho atual for um ficheiro
            if os.path.isfile(os.path.join(image_path, path)):
                count += 1    # Caso sim, adiciona um valor ao contador dos ficheiros

        # Se contador for igual a zero, assume-se que não há caras
        # Se não, o número de caras descobre-se através da divisão da variável count por 100
        # visto que para cada cara, são tiradas 100 fotografias de cada vez
        if(count != 0):
            faces = count/100
        else:
            faces = 0


        os.chdir('pages') # Ir para o ficheiro pages

        # Verifica se a pasta existe
        if not os.path.exists('images'):
            os.makedirs('images')


        # Abrir haarcascade ficherio
        face_cascade_Path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'haarcascade_frontalface_default.xml')
        faceCascade = cv2.CascadeClassifier(face_cascade_Path)

        # Veririca se o haarcascade foi aberto
        if faceCascade.empty():
            print("Erro: Não foi possível abrir o ficheiro haarcascade.")
            return HttpResponseServerError("Internal Server Erro: Não foi possível abrir o ficheiro haarcascade.")
        
        # Captura de Vídeo
        cam = cv2.VideoCapture(0)

        # Resolução do Vídeo 16:9
        cam.set(3,853)
        cam.set(4,480)

        # Atualizar variavel count
        count = 0
        
        # Para cada pessoa cria-se um face_id único
        face_id = faces + 1

        while(True):
            # Capturar um frame da camara
            ret, img = cam.read()

            # Converte a imagem para escala de cinza, para o reconhecimento facial ser executado corretamente
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Detetar cara no frame
            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
            for (x,y,w,h) in faces:
                # Desenhar um retângulo à volta da cara detetada
                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
                count += 1

                # Guardar a imagem capturada na pasta 'images'
                cv2.imwrite("./images/Users." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

                # Meter em Full Screen o Tirar Fotografias
                cv2.namedWindow("image", cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.imshow('image', img)

            # Escape para sair da janela
            k = cv2.waitKey(100) & 0xff
            if k < 100:
                break
            # Capturar 100 amostras de cara e parar o vídeo. Pode-se aumentar ou diminuir o número de
            # imagens. Quanto mais, melhor ao treinar o modelo.
            elif count >= 100:
                break

        cam.release()
        cv2.destroyAllWindows()

        return HttpResponse("Fotografias foram tiradas com sucesso!")


# Página para criar ficheiro treinado 
def train_photos(request):
    #Directory path name where the face images are stored.
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')

    recognizer = cv2.face.LBPHFaceRecognizer_create() 
    #Haar cascade file
    cascade = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'haarcascade_frontalface_default.xml')  # get current directory
    detector = cv2.CascadeClassifier(cascade)

    def getImagesAndLabels(path):
        imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
        faceSamples=[]
        ids = []
        for imagePath in imagePaths:
            # convert it to grayscale
            PIL_img = Image.open(imagePath).convert('L')
            img_numpy = np.array(PIL_img,'uint8')
            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = detector.detectMultiScale(img_numpy)
            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(id)
        return faceSamples, ids
    faces,ids = getImagesAndLabels(path)
    recognizer.train(faces, np.array(ids))

    
    # Save the model into the current directory.
    folder = os.path.dirname(os.path.abspath(__file__))
    trained_file_path = os.path.join(folder, 'trainer.yml')
    recognizer.write(trained_file_path)

    return HttpResponse("Photos treinadas")
