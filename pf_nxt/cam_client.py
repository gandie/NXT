import socket
import pygame
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('Connected, starting receive loop')

done = False
sock.connect(("192.168.43.173", 14243))

while True:

    print('next')

    received = []
    while True:
        data = sock.recv(230400)
        if not data:
            break
        else:
            received.append(data)
    dataset = ''.join(received)
    # print(dataset)
    try:
        image = pygame.image.fromstring(dataset, (640, 480), "RGB")
        pygame.image.save(image, "test.jpg")
        print('success!')
    except:
        pass
    # time.sleep(1)
