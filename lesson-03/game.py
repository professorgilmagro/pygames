#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Gilmar S. Santos <gilmar.pythonman@outlook.com>

"""
Jogo simples para desenvolver habilidades em pygame
utilizando os recursos mais comuns:
    1 - fonts
    2 - mixer
    3 - carregamento de midias
    4 - background
    5 - sprite
    6 - eventos de mouse
    7 - movimentos básicos dentro da área do jogo

Fonte: http://www.pygame.org/docs
"""

from pygame.locals import *

try:
    import os
    import sys
    import random
    import pygame
except Exception, e:
    print "Não foi possível carregar o módulo. Erro: '%s'" % (e)
    sys.exit()

if not pygame.font:
    print 'Aviso: Fontes desabilitadas!'
if not pygame.mixer:
    print 'Aviso: Som desabilitado!'


def load_image(name, colorkey=None):
    # Cria a imagem a partir do nome informado
    fullname = os.path.join("data", name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Não foi possível carregar a imagem:', fullname
        raise message

    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
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
        print 'Não foi possível carregar o som:', fullname
        raise message
    return sound


class sock(pygame.sprite.Sprite):
    #movimenta o punho pela tela seguindo o mouse
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("punch-md.png", -1)
        self.image = pygame.transform.scale(self.image, (40, 60))
        self.punching = 0

    def update(self):
        "Movimenta o punho de acordo com a posição do mouse"
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        if self.punching:
            self.rect.move_ip(5, 10)

    def punch(self, target):
        "Verifica se houve colisão entre este objeto e o objeto informado"
        if not self.punching:
            self.punching = 1
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unpunch(self):
        "Volta para o estado inicial"
        self.punching = 0


class character(pygame.sprite.Sprite):
    """Movimenta o personagem pela tela. Dispara o som quando é atingido e
    o muda de posição"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('dragao.gif', -1)
        self.sound = load_sound("punch.wav")
        self.image = pygame.transform.scale(self.image, (150, 200))
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 50, 10
        self.move = 1
        self.dizzy = 0

    def update(self):
        "faz o personagem andar ou rotacionar dependendo do status"
        if self.dizzy:
            self._swing()
        else:
            self._walk()

    def _walk(self):
        """movimenta o personagem no cenário e o gira horizontamente quando
        atinge as extremidades"""
        newpos = self.rect.move((self.move, 0))
        if self.rect.left < self.area.left \
           or self.rect.right > self.area.right:
            self.move = -self.move
            newpos = self.rect.move((self.move, 0))
            self.image = pygame.transform.flip(self.image, 1, 0)

        self.rect = newpos

    def _swing(self):
        "cria o efeito de girar"
        center = self.rect.center

        self.dizzy = self.dizzy + 12
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
            self.rect = self.image.get_rect(center=center)
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.dizzy)
            self.rect = self.image.get_rect()
            randint = random.randint
            self.rect.topleft = randint(10, 200), randint(10, 300)

    def punched(self):
        self.sound.play()
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image


class score():
    """Gera o placar de pontuação do jogo"""
    def __init__(self):
        self.score = 0
        self.increase = 1

    def render(self, increase=1):
        font = pygame.font.Font(None, 40)
        self.score += self.increase * increase
        return font.render(
            "Score: %s" % self.score, True, (255, 255, 255)
        )


def main():
    """Esta função é chamada quando o programa for iniciado."""

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("O invasor do Espaço")
    pygame.mouse.set_visible(False)

# Cria o fundo
    background = load_image("bkg.jpg")[0]

# Cria o texto
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("O invasor deve ser detido.", True, (255, 255, 255))
        textpos = text.get_rect(centerx=background.get_width() / 2)
        background.blit(text, textpos)

        point = score()
        points = point.render(0)

# Mostra o fundo e pontuação inicial
    screen.blit(background, (0, 0))
    screen.blit(load_image("dragao.gif")[0], (80, 60))
    pygame.display.flip()

# Prepara os objetos do jogo
    clock = pygame.time.Clock()
    whiff_sound = load_sound("miss.wav")
    person = character()
    fist = sock()
    all_sprites = pygame.sprite.RenderPlain((fist, person))

    pygame.mixer.music.load("data/intro.wav")
    pygame.mixer.music.play()

    while True:
        clock.tick(360)

        if pygame.mixer.music.get_busy():
            continue

    # Escuta os eventos do mouse e teclado
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == MOUSEBUTTONDOWN:
                if fist.punch(person):
                    points = point.render(1)
                    person.punched()
                else:
                    whiff_sound.play()
                    points = point.render(-1)
            elif event.type is MOUSEBUTTONUP:
                fist.unpunch()

    # Redesenha todo o cenário
        screen.blit(background, (0, 0))
        screen.blit(points, (10, 10))
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()

#Game Over

# Quando o script é executado, invoca a função 'main'
if __name__ == "__main__":
    main()
