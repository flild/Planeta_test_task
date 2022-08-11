import zmq
import cv2

from loguru import logger

logger.add('logs/server.log', format='{time} {level} {message}', level='INFO', rotation='1 week')

def main():
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    logger.debug('Создание сокета')
    socket.bind("tcp://*:8000")
    logger.debug('Сервер запущен...')

    try:
        logger.info(f'Начало трансляции')
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
                    logger.debug('Видео началось заново')
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
    except Exception as e:
        logger.error(f'{Exception}')
    finally:
        socket.close()

if __name__ == '__main__':
    main()