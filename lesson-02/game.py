#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Gilmar S. Santos <gilmar.pythonman@outlook.com>

import sys
import pygame

pygame.init()

size = width, height = 800, 600
speed = [2, 2]

pygame.display.set_caption("Bola saltitante")
screen = pygame.display.set_mode(size)

ball = pygame.image.load("ball.png")
ball_rect = ball.get_rect()
sound = pygame.mixer.Sound("bouche.wav")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    ball_rect = ball_rect.move(speed)
    if ball_rect.left < 0 or ball_rect.right > width:
        speed[0] = -speed[0]
        sound.play()

    if ball_rect.top < 0 or ball_rect.bottom > height:
        speed[1] = -speed[1]
        sound.play()

    screen.fill((32, 98, 48))
    screen.blit(ball, ball_rect)
    pygame.display.flip()
