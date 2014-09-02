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

pygame.init()
SCREEN_SIZE = (1280, 1024)
MAX_MISS = 3


def load_image(name, colorkey=None, resize=None):
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
        print 'Não foi possível carregar o som:', fullname
        raise message
    return sound


class Sock(pygame.sprite.Sprite):
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


class Character(pygame.sprite.Sprite):
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
        self._move = 2
        self.dizzy = 0

    @property
    def move(self):
        return self._move

    @move.setter
    def move(self, value):
        self._move = value

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
        if (self.rect.left < self.area.left
           or self.rect.right > self.area.right):
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
            self.rect.topleft = randint(40, 600), randint(40, 800)

    def punched(self):
        i = 1
        if self.move < 0:
            i = -1

        self.move += i
        self.sound.play()
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image


class Score():
    """Gera o placar de pontuação do jogo"""
    def __init__(self):
        self.score = 0
        self.miss = 0
        self._increase = 1
        self._hit_val = 1

    @property
    def increase(self):
        return self._increase

    @increase.setter
    def increase(self, value):
        if value is False or value < 0:
            value = -1
        else:
            value = 1

        self._increase = value

    def render_score(self):
        font = pygame.font.Font(None, 40)
        self.score += self._hit_val * self.increase
        return font.render(
            "Score: %s" % self.score, True, (255, 255, 255)
        )

    def render_miss(self):
        font = pygame.font.Font(None, 30)
        return font.render(
            "Erros: %s" % self.miss, True, (255, 255, 0)
        )


def main():
    """Esta função é chamada quando o programa for iniciado."""
    screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
    pygame.display.set_caption("O invasor do Espaço")
    pygame.mouse.set_visible(False)

    # Cria o fundo
    background = load_image("bkg.jpg")[0]
    background = pygame.transform.scale(background, SCREEN_SIZE)

    # Cria o texto
    font = pygame.font.Font(None, 36)
    text = font.render("O invasor deve ser detido.", True, (255, 255, 255))
    textpos = text.get_rect(centerx=background.get_width() / 2)
    background.blit(text, textpos)

    # Mostra o fundo e pontuação inicial
    screen.blit(background, (0, 0))
    screen.blit(load_image("dragao.gif")[0], (80, 60))
    pygame.display.flip()

    # Prepara os objetos do jogo
    clock = pygame.time.Clock()
    whiff_sound = load_sound("miss.wav")
    person = Character()
    fist = Sock()
    all_sprites = pygame.sprite.RenderPlain((fist, person))

    # Carrega os sons
    pygame.mixer.music.load("data/intro.wav")
    pygame.mixer.music.play()
    game_over_sound = load_sound("game_over.ogg")
    theme_sound = load_sound("theme.ogg")

    # game over message
    font = pygame.font.Font(None, 40)
    game_over = font.render("Game Over!", True, (255, 255, 0))

    pos = game_over.get_rect(
        centerx=screen.get_width() / 2,
        centery=screen.get_height() / 2
    )

    score = Score()

    pygame.display.toggle_fullscreen()
    while True:
        clock.tick(360)

        if pygame.mixer.music.get_busy():
            continue

        theme_sound.play()
        score.increase = 0

        # Escuta os eventos do mouse e teclado
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            elif (event.type == pygame.MOUSEBUTTONDOWN
                  and score.miss < MAX_MISS):
                if fist.punch(person):
                    score.increase = True
                    person.punched()
                else:
                    score.increase = False
                    score.miss += 1
                    whiff_sound.play()
            elif event.type is pygame.MOUSEBUTTONUP:
                fist.unpunch()

        screen.blit(background, (0, 0))
        screen.blit(score.render_score(), (10, 10))
        screen.blit(score.render_miss(), (10, 50))

        if score.miss == MAX_MISS:
            screen.blit(*load_image("end.jpg", 1, SCREEN_SIZE))
            screen.blit(game_over, pos)
            pygame.display.flip()
            theme_sound.stop()
            game_over_sound.play()
            continue

        # Redesenha e atualiza todo o cenário
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()

#Game Over

# Quando o script é executado, invoca a função 'main'
if __name__ == "__main__":
    main()
