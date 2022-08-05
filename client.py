import zmq
import cv2

context = zmq.Context()
socket = context.socket(zmq.PULL)

socket.connect("tcp://localhost:8000")
print("client started")

# Настройки для отображения видео
down_width = 400
down_height = 400
down_points = (down_width, down_height)
print('Чтобы закрыть видео нажмите q')
try:
    while True:
        image = socket.recv_pyobj()
        image = cv2.resize(image, down_points, interpolation=cv2.INTER_LINEAR)
        # показываем по одной картинке, что в итоге сложится в видео
        cv2.imshow('frame', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cv2.destroyAllWindows()
    socket.close()
