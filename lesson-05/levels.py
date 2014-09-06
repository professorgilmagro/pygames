import pygame

import constants as const
import platforms
import utils


class Level():
    """
    Classe base para definicao de level
    """

    # Recebe as imagens de todos os levels do jogo
    platform_list = None
    enemy_list = None

    background = None
    sound = None
    world_shift = 0
    level_limit = -1000

    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

    def update(self):
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        # Desenha o fundo em azul
        screen.fill(const.BLUE)
        screen.blit(self.background, (self.world_shift // 3, 0))

        # Desenha todos os sprites na tela
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    def change_world(self, shift_x):
        """
        Ao mover o personagem para esquerda ou direita
        alteramos o scroll da tela
        """

        # Mantem o controle de deslocamento
        self.world_shift += shift_x

        # Passa por todas as listas de sprite e aplica a mudanca
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x


class Level_01(Level):
    """
    Define os objetos (plataformas) e fundo a ser utilizado no primeiro level
    """

    def __init__(self, player):
        Level.__init__(self, player)

        self.background = utils.load_image("background_01.jpg")
        self.sound = utils.load_sound("level1.ogg")

        """
        Array com o tipo de plataforma, posicao x, y e
        localizado dentro do sprite
        """
        level = [[platforms.GRASS_LEFT, 500, 500],
                 [platforms.GRASS_MIDDLE, 570, 500],
                 [platforms.GRASS_RIGHT, 640, 500],
                 [platforms.GRASS_LEFT, 800, 400],
                 [platforms.GRASS_MIDDLE, 870, 400],
                 [platforms.GRASS_RIGHT, 940, 400],
                 [platforms.GRASS_LEFT, 1000, 500],
                 [platforms.GRASS_MIDDLE, 1070, 500],
                 [platforms.GRASS_RIGHT, 1140, 500],
                 [platforms.STONE_PLATFORM_LEFT, 1120, 280],
                 [platforms.STONE_PLATFORM_MIDDLE, 1190, 280],
                 [platforms.STONE_PLATFORM_RIGHT, 1260, 280]]

        # Recupera as plataformas a partir das coordernadas em level
        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)

        # Adiciona movimento personalizado as plataformas
        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1350
        block.rect.y = 280
        block.boundary_left = 1350
        block.boundary_right = 1600
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)


class Level_02(Level):
    """
    Define os objetos (plataformas) e fundo a ser utilizado no segundo level
    """

    def __init__(self, player):

        Level.__init__(self, player)

        self.background = utils.load_image("background_02.jpg")
        self.sound = utils.load_sound("level2.ogg")

        level = [[platforms.STONE_PLATFORM_LEFT, 500, 550],
                [platforms.STONE_PLATFORM_MIDDLE, 570, 550],
                [platforms.STONE_PLATFORM_RIGHT, 640, 550],
                [platforms.STONE_PLATFORM_LEFT, 800, 400],
                [platforms.STONE_PLATFORM_MIDDLE, 870, 400],
                [platforms.STONE_PLATFORM_RIGHT, 940, 400],
                [platforms.STONE_PLATFORM_LEFT, 1000, 500],
                [platforms.STONE_PLATFORM_MIDDLE, 1070, 500],
                [platforms.STONE_PLATFORM_RIGHT, 1140, 500],
                [platforms.STONE_PLATFORM_LEFT, 1120, 280],
                [platforms.STONE_PLATFORM_MIDDLE, 1190, 280],
                [platforms.STONE_PLATFORM_RIGHT, 1260, 280]]

        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)

        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)


class Level_03(Level):
    """
    Define os objetos (plataformas) e fundo a ser utilizado no terceiro level
    """

    def __init__(self, player):

        Level.__init__(self, player)

        self.background = utils.load_image("background_03.png")
        self.sound = utils.load_sound("level3.ogg")

        level = [[platforms.STONE_PLATFORM_LEFT, 500, 550],
                [platforms.STONE_PLATFORM_MIDDLE, 570, 550],
                [platforms.STONE_PLATFORM_RIGHT, 640, 550],
                [platforms.STONE_PLATFORM_LEFT, 800, 400],
                [platforms.STONE_PLATFORM_MIDDLE, 870, 400],
                [platforms.STONE_PLATFORM_RIGHT, 940, 400],
                [platforms.STONE_PLATFORM_LEFT, 1000, 500],
                [platforms.STONE_PLATFORM_MIDDLE, 1070, 500],
                [platforms.STONE_PLATFORM_RIGHT, 1140, 500],
                [platforms.STONE_PLATFORM_LEFT, 1120, 280],
                [platforms.STONE_PLATFORM_MIDDLE, 1190, 280],
                [platforms.STONE_PLATFORM_RIGHT, 1260, 280]]

        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)

        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)


class Level_04(Level):
    """
    Define os objetos (plataformas) e fundo a ser utilizado no terceiro level
    """

    def __init__(self, player):

        Level.__init__(self, player)

        self.background = utils.load_image("background_04.png")
        self.sound = utils.load_sound("level4.ogg")

        level = [[platforms.STONE_PLATFORM_LEFT, 500, 550],
                [platforms.STONE_PLATFORM_RIGHT, 640, 550],
                [platforms.STONE_PLATFORM_MIDDLE, 570, 550],
                [platforms.STONE_PLATFORM_MIDDLE, 870, 400],
                [platforms.STONE_PLATFORM_LEFT, 800, 400],
                [platforms.STONE_PLATFORM_RIGHT, 940, 400],
                [platforms.STONE_PLATFORM_LEFT, 1000, 500],
                [platforms.STONE_PLATFORM_MIDDLE, 1070, 500],
                [platforms.STONE_PLATFORM_RIGHT, 1140, 500],
                [platforms.STONE_PLATFORM_LEFT, 1120, 280],
                [platforms.STONE_PLATFORM_MIDDLE, 1190, 280],
                [platforms.STONE_PLATFORM_RIGHT, 1260, 280]]

        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)

        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)
