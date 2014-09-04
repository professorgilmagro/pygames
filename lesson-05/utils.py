import os
import pygame
import constants as const

"""
Permite o carregamento de midias
"""


def load_image(name, colorkey=None, resize=None):
    # Cria a imagem a partir do nome informado
    filename = os.path.join(const.MEDIA_DIR, name)
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

    return image, image.get_rect()


def load_sound(sound_name):
    # Carrega o som informado
    class NoneSound:
        def play(self):
            pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()

    fullname = os.path.join("data", sound_name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print "Nao foi possivel carregar o som:", fullname
        raise message
    return sound


def get_event_key(event):
    if event.type == pygame.KEYDOWN:
        return event.key
    return None
