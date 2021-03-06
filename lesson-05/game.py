#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Gilmar S. Santos <gilmar.pythonman@outlook.com>

import os
import pygame

import utils
import levels
import constants as const

from player import Player
from progress_bar import Loader

os.environ["SDL_VIDEO_CENTERED"] = "1"


def main():
    pygame.init()

    screen = pygame.display.set_mode(const.SCREEN_MODE)
    pygame.display.set_caption("Arcade Game")
    pygame.display.set_icon(utils.load_image("icon.png"))
    pygame.mouse.set_visible(False)

    player = Player()

    # preload
    initial_bkg = utils.load_image("initial_background.jpg")
    screen.blit(initial_bkg, (0, 0))

    loader = Loader(screen)
    loader.render()
    pygame.display.update()

    # Cria os niveis do jogo
    level_list = []
    level_list.append(levels.Level_01(player))
    level_list.append(levels.Level_02(player))
    level_list.append(levels.Level_03(player))
    level_list.append(levels.Level_04(player))

    # Set the current level
    level_number = 0
    current_level = level_list[level_number]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

     # prepara o personagem na tela
    player.rect.x = 340
    player.rect.y = const.SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    clock = pygame.time.Clock()
    running = True

    while running:
        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            running = False

        if loader.run():
            continue

        key_down = utils.get_event_key(event, pygame.KEYDOWN)
        if key_down == pygame.K_LEFT:
            player.go_left()

        if key_down == pygame.K_RIGHT:
            player.go_right()

        if key_down == pygame.K_UP:
            player.jump()

        key_up = utils.get_event_key(event, pygame.KEYUP)
        if key_up == pygame.K_LEFT and player.move_x < 0:
            player.stop()
        if key_up == pygame.K_RIGHT and player.move_x > 0:
            player.stop()

        if not pygame.mixer.get_busy():
            current_level.sound.play()

        screen.fill(const.GREEN)
        active_sprite_list.update()
        current_level.update()

        # controla o scrolling do game
        if player.rect.x >= 500:
            diff = player.rect.x - 500
            player.rect.x = 500
            current_level.change_world(-diff)

        if player.rect.x <= 120:
            diff = 120 - player.rect.x
            player.rect.x = 120
            current_level.change_world(diff)

         # Avança para o próximo level
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            player.rect.x = 120
            if level_number < len(level_list) - 1:
                level_number += 1
                current_level.sound.stop()
                current_level = level_list[level_number]
                player.level = current_level
                player.level.sound.play()

        current_level.draw(screen)
        active_sprite_list.draw(screen)

        clock.tick(60)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
