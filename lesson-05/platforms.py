import pygame

import constants as const
from utils import SpriteSheet

GRASS_LEFT = (576, 720, 70, 70)
GRASS_RIGHT = (576, 576, 70, 70)
GRASS_MIDDLE = (504, 576, 70, 70)
STONE_PLATFORM_LEFT = (432, 720, 70, 40)
STONE_PLATFORM_MIDDLE = (648, 648, 70, 40)
STONE_PLATFORM_RIGHT = (792, 648, 70, 40)
YELLOW_BOX = (140, 0, 70, 70)
ARROW_RIGHT = (286, 215, 70, 70)
EXIT = (286, 360, 70, 70)


class Platform(pygame.sprite.Sprite):
    """
    Plataformas sobre a qual o jogador ira pular
    """

    def __init__(self, sprite_data):
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = SpriteSheet("tiles_spritesheet.png", const.BLACK)

        # Obtem a imagen a partir das posicoes e tamanho do sprite
        self.image = sprite_sheet.get_image(sprite_data[0],
                                            sprite_data[1],
                                            sprite_data[2],
                                            sprite_data[3])

        self.rect = self.image.get_rect()


class MovingPlatform(Platform):
    change_x = 0
    change_y = 0

    limit_top = 0
    limit_bottom = 0
    limit_left = 0
    limit_right = 0

    level = None
    player = None

    def update(self):
        # Movimenta para esquerda ou direita
        self.rect.x += self.change_x

        # Verfica possiveis colisoes
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                self.player.rect.left = self.rect.right

        # Movimenta para cima ou para baixo
        self.rect.y += self.change_y

        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom

        if(self.rect.bottom > self.limit_bottom
           or self.rect.top < self.limit_top):
            self.change_y *= -1

        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.limit_left or cur_pos > self.limit_right:
            self.change_x *= -1
