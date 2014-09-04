import pygame
import utils
import constants as const


class Player(pygame.sprite.Sprite):
    """
    Esta classe representa o personagem na parte inferior que o jogador
    controla.
    """

    # Define a velocidade de movimento do jogador
    speed_x, speed_y = 0, 0

    # Garda as posicoes do spritesheet para animar o personagem enquanto anda
    walk_frames_left = []
    walk_frames_right = []

    # Indica a direcao que o personagem esta sendo movimentado
    direction = "R"

    # Lista de sprites de colisao
    level = None

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        sprite_sheet = SpriteSheet("ogre.png")

        # x, y, width, height

        # carrega todas as images (fatiadas) e a guarda nos frames
        for x in range(0, 4):
            pos_left = (110 * x, 145, 110, 145)
            pos_right = (110 * x, 290, 110, 145)
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

        # gravidade
        # self.calc_grav()

         # Movimenta para esquerda ou direita
        self.rect.x += self.speed_x
        pos = self.rect.x
        if self.direction == "R":
            frame = (pos // 23) % len(self.walk_frames_right)
            self.image = self.walk_frames_right[frame]
        else:
            frame = (pos // 23) % len(self.walk_frames_left)
            self.image = self.walk_frames_left[frame]

    def go_left(self):
        self.speed_x = -5
        self.direction = "L"

    def go_right(self):
        self.speed_x = 5
        self.direction = "R"

    def stop(self):
        self.speed_x = 0


class SpriteSheet(object):
    """ Classe usada para cortar imagens dentro de um spritesheet """

    sprite_sheet = None

    def __init__(self, file_name):

        # Carrega o sprite sheet.
        self.sprite_sheet = utils.load_image(file_name)[0]

    def get_image(self, x, y, width, height):
        """ Retorna uma imagem de um spritesheet maior
            a partir da localizacao x, y do item desejado
            e a largura e altura do sprite. """

        # Cria uma nova imagem em branco
        image = pygame.Surface([width, height]).convert()

        # Copia a imagem (sprite) para dentro da nova imagem
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Assume o branco como cor transparente
        image.set_colorkey(const.WHITE)

        # retorna a imagem
        return image
