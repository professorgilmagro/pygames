#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Gilmar S. Santos <gilmar.pythonman@outlook.com>

import pygame
import os
import utils
import constants as const

from player import Player

os.environ["SDL_VIDEO_CENTERED"] = "1"


def main():
    pygame.init()

    screen = pygame.display.set_mode(const.SCREEN_MODE)
    pygame.display.set_caption("Arcade Game")
    pygame.mouse.set_visible(False)

    player = Player()

    # prepara o personagem na tela
    active_sprite_list = pygame.sprite.Group()
    player.rect.x = 340
    player.rect.y = const.SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            key = utils.get_event_key(event)
            if key == pygame.K_LEFT:
                player.go_left()

            if key == pygame.K_RIGHT:
                player.go_right()

            if key == pygame.K_UP:
                player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.move_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.move_x > 0:
                    player.stop()

        screen.fill(const.BLACK)
        active_sprite_list.update()
        active_sprite_list.draw(screen)

        clock.tick(60)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
