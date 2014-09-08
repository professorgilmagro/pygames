import os
import pygame
import constants as const

"""
Funcoes comuns
"""


def load_image(name, colorkey=None, resize=None):
    # Cria a imagem a partir do nome informado
    filename = os.path.join(const.IMAGE_DIR, name)
    try:
        image = pygame.image.load(filename)
    except pygame.error, message:
        print "Nao foi possivel carregar a imagem:", filename
        raise message

    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)

    if resize is not None:
        image = pygame.transform.scale(image, resize)

    return image


def load_sound(sound_name):
    # Carrega o som informado
    class NoneSound:
        def play(self):
            pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()

    filename = os.path.join(const.SOUND_DIR, sound_name)
    try:
        sound = pygame.mixer.Sound(filename)
    except pygame.error, message:
        print "Nao foi possivel carregar o som:", filename
        raise message
    return sound


def get_event_key(event, key_event):
    if event.type == key_event:
        return event.key
    return None


class SpriteSheet(object):
    """
    Classe usada para cortar imagens dentro de um spritesheet
    """

    sprite_sheet = None

    def __init__(self, file_name, colorkey=None):
        self.colorkey = colorkey

        # Carrega o sprite sheet.
        self.sprite_sheet = load_image(file_name)

    def get_image(self, x, y, width, height):
        """ Retorna uma imagem de um spritesheet maior
            a partir da localizacao x, y do item desejado
            e a largura e altura do sprite. """

        # Cria uma nova imagem em branco
        image = pygame.Surface([width, height]).convert()

        # Copia a imagem (sprite) para dentro da nova imagem
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Define a cor a ser utilizada para a transparencia
        if self.colorkey is not None:
            image.set_colorkey(self.colorkey)

        # retorna a imagem
        return image
