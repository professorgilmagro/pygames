#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Gilmar S. Santos <gilmar.pythonman@outlook.com>

import pygame
import random


def random_rgb_color():
    """
        Gera uma cor aleatória em RGB
    """
    return(
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )


def main():
    """
        Executa o game
    """
    pygame.init()

    # cria uma tela no tamanho 600 x 480
    screen = pygame.display.set_mode((600, 480))
    pygame.display.set_caption(
        "Tela do jogo - Clique para mudar a cor de fundo"
    )

    # Cor inicial
    color = (255, 0, 0)

    while True:
        event = pygame.event.wait()

        screen.fill(color)
        pygame.display.flip()

        if event.type == pygame.MOUSEBUTTONDOWN:
            color = random_rgb_color()

        elif event.type == pygame.QUIT:
            pygame.quit()
            return

        elif event.type == pygame.MOUSEBUTTONUP:
            pygame.display.set_caption("Cor atual RGB {0}".format(str(color)))


if __name__ == "__main__":
    main()
