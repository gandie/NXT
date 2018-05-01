import socket
import pygame
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("192.168.43.173", 14243))

print('Connected, starting receive loop')

done = False

while not done:
    received = []
    while True:
        data = sock.recv(230400)
        if not data:
            break
        else:
            received.append(data)
    dataset = ''.join(received)
    image = pygame.image.fromstring(dataset, (640, 480), "RGB")
    pygame.image.save(image, "test.jpg")
    time.sleep(1)
