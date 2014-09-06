import pygame
import utils
import constants as const
from platforms import MovingPlatform


class Player(pygame.sprite.Sprite):
    """
    Esta classe representa o personagem na parte inferior que o jogador
    controla.
    """

    # Define a velocidade de movimento do jogador
    move_x, move_y = 0, 0

    # Garda as posicoes do spritesheet para animar o personagem enquanto anda
    walk_frames_left = []
    walk_frames_right = []

    # Indica a direcao que o personagem esta sendo movimentado
    direction = "R"

    # Lista de sprites de colisao
    level = None

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        sprite_sheet = utils.SpriteSheet("ogre.png", const.WHITE)

        # x, y, width, height

        # carrega todas as images (fatiadas) e a guarda nos frames
        for x in xrange(0, 4):
            pos_left = (107 * x, 145, 107, 145)
            pos_right = (107 * x, 290, 107, 145)
            self.walk_frames_left.append(sprite_sheet.get_image(*pos_left))
            self.walk_frames_right.append(sprite_sheet.get_image(*pos_right))

         # Defina a imagem inicial
        self.image = self.walk_frames_right[0]

        # Recupera a area da imagem
        self.rect = self.image.get_rect()

    def update(self):
        """
        Move o personagem.
        """

        # Gravidade
        self.calc_gravity()

         # Movimenta para esquerda ou direita
        self.rect.x += self.move_x
        pos = self.rect.x + self.level.world_shift
        if self.direction == "R":
            frame = (pos // 30) % len(self.walk_frames_right)
            self.image = self.walk_frames_right[frame]
        else:
            frame = (pos // 30) % len(self.walk_frames_left)
            self.image = self.walk_frames_left[frame]

        # Verica se houve colisao com as plataformas (horizontal)
        block_hit_list = pygame.sprite.spritecollide(
            self, self.level.platform_list, False
        )

        for block in block_hit_list:
            if self.move_x > 0:
                self.rect.right = block.rect.left
            elif self.move_x < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.move_y

         # Verica se houve colisao com as plataformas (vertical)
        block_hit_list = pygame.sprite.spritecollide(
            self, self.level.platform_list, False
        )

        for block in block_hit_list:
            if self.move_y > 0:
                self.rect.bottom = block.rect.top
            elif self.move_y < 0:
                self.rect.top = block.rect.bottom

            self.move_y = 0

            if isinstance(block, MovingPlatform):
                self.rect.x += block.change_x

    def calc_gravity(self):
        """
        Calcula o efeito gravidade
        """
        if self.move_y == 0:
            self.move_y = 1
        else:
            self.move_y += .35

        # verifica se estamos no chao e fazemos os ajustes
        if (self.rect.y >= const.SCREEN_HEIGHT - self.rect.height
           and self.move_y >= 0):
            self.move_y = 0
            self.rect.y = const.SCREEN_HEIGHT - self.rect.height

    def go_left(self):
        self.move_x = -5
        self.direction = "L"

    def go_right(self):
        self.move_x = 5
        self.direction = "R"

    def stop(self):
        self.move_x = 0

    def jump(self):
        self.rect.y += 2

        # verifica se houve colisao ao subir (bater a cabeca em alguma coisa)
        platform_hit_list = pygame.sprite.spritecollide(
            self, self.level.platform_list, False
        )

        self.rect.y -= 2

        list_len = len(platform_hit_list)
        if (list_len > 0 or self.rect.bottom >= const.SCREEN_HEIGHT):
            self.move_y = -10
            utils.load_sound("jump.wav").play()
