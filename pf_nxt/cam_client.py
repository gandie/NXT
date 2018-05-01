import socket
import pygame
import time


while True:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect(("192.168.43.173", 14243))
    except:
        print('connect failed')
        pass
    print('next')

    received = []
    while True:
        data = sock.recv(230400)
        if not data:
            break
        else:
            received.append(data)
    dataset = ''.join(received)
    print('received')
    # print(dataset)
    try:
        image = pygame.image.fromstring(dataset, (640, 480), "RGB")
        pygame.image.save(image, "test.jpg")
        print('success!')
    except:
        print('failed')
        pass
    sock.close()
    time.sleep(.5)
