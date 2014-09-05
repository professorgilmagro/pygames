#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Gilmar S. Santos <gilmar.pythonman@outlook.com>

import pygame
import os

import utils
import levels
import constants as const

from player import Player

os.environ["SDL_VIDEO_CENTERED"] = "1"


def main():
    pygame.init()

    screen = pygame.display.set_mode(const.SCREEN_MODE)
    pygame.display.set_caption("Arcade Game")
    pygame.mouse.set_visible(False)

    player = Player()
    music = utils.load_sound("8_bit_theme.wav")

    # prepara o personagem na tela
    active_sprite_list = pygame.sprite.Group()
    player.rect.x = 340
    player.rect.y = const.SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    # Cria os niveis do jogo
    level_list = []
    level_list.append(levels.Level_01(player))

    # Set the current level
    level_number = 0
    current_level = level_list[level_number]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

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

        if not pygame.mixer.get_busy():
            music.play()

        screen.fill(const.BLACK)
        active_sprite_list.update()
        current_level.update()

        # controla o scrolling do game
        if player.rect.x >= 500:
            diff = player.rect.x - 500
            player.rect.x = 500
            current_level.shift_world(-diff)

        if player.rect.x <= 120:
            diff = 120 - player.rect.x
            player.rect.x = 120
            current_level.shift_world(diff)

        active_sprite_list.draw(screen)

        clock.tick(60)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
