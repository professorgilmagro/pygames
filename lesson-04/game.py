import pygame
import os

# centraliza jogo na tela
os.environ["SDL_VIDEO_CENTERED"] = "1"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SCREEN_SIZE = 800, 600
MOVE_SPEED = 5

pygame.init()


def load_image(name, colorkey=None, resize=None):
    filename = os.path.join("data", name)
    image = pygame.image.load(filename).convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)

    if type(resize) in (tuple, list):
        image = pygame.transform.scale(image, resize)

    return image


def get_event_key(event):
    if event.type == pygame.KEYDOWN:
        return event.key
    return None


def main():
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Guerra nas estrelas")
    pygame.mouse.set_visible(False)
    shoot_sound = pygame.mixer.Sound("media/laser.wav")
    pos = x, y = 0, 0

    # Carrega as images
    bkg_imge = load_image("background.jpg", None, SCREEN_SIZE)
    player_image = load_image("ship.png", BLACK)
    pygame.key.set_repeat(1)
    clock = pygame.time.Clock()

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif get_event_key(event) == pygame.K_SPACE:
                shoot_sound.stop()
                shoot_sound.play()
            elif get_event_key(event) == pygame.K_RIGHT:
                x += MOVE_SPEED
            elif get_event_key(event) == pygame.K_LEFT:
                x -= MOVE_SPEED
            elif get_event_key(event) == pygame.K_UP:
                y -= MOVE_SPEED
            elif get_event_key(event) == pygame.K_DOWN:
                y += MOVE_SPEED

        screen.blit(bkg_imge, pos)
        screen.blit(player_image, [x, y])
        pygame.display.flip()

        clock.tick(180)

    pygame.quit()

if __name__ == "__main__":
    main()
