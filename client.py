import zmq
import cv2

from loguru import logger
#настройки логгера, а именно папка сохранения логов, в каком виде вести логоирование, через какое время удалять логи
logger.add('logs/client.log', format='{time} {level} {message}', level='INFO', rotation='1 week')
def main():
    #Соединение с сервером
    context = zmq.Context()
    socket = context.socket(zmq.PULL)

    socket.connect("tcp://localhost:8000")
    logger.debug("Присоеденились")

    # Настройки для отображения видео
    down_width = 400
    down_height = 400
    down_points = (down_width, down_height)
    print('Чтобы закрыть видео нажмите q')
    try:
        while True:
            # Принимаем по картинке
            image = socket.recv_pyobj()
            image = cv2.resize(image, down_points, interpolation=cv2.INTER_LINEAR)
            # показываем по одной картинке, что в итоге сложится в видео
            cv2.imshow('frame', image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                logger.info('Пользователь отключился')
                break
    except Exception as e:
        logger.error(f'{Exception}')

    finally:
        #Закроем все окна и все сокеты
        cv2.destroyAllWindows()
        socket.close()

if __name__ == '__main__':
    main()
