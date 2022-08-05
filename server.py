import zmq
import cv2

context = zmq.Context()
socket = context.socket(zmq.PUSH)

socket.bind("tcp://*:8000")
print('server started...')
try:
    while True:
        # получим объект видео
        cap = cv2.VideoCapture('example.mp4')
        while (cap.isOpened()):
            # разбиваем по фреймам
            ret, frame = cap.read()
            if ret:
                # передаём по одному фрейму, один фрейм это картинка
                socket.send_pyobj(frame)
            else:
                # Сместим курсор на 0 фрейм
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
finally:
    socket.close()
