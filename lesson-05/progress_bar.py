import pygame


class ProgressBar:
    def __init__(self, rect, **kwargs):
        self.rect = pygame.Rect(rect)
        self.max_width = self.rect.width
        self.timer = 0.0
        self.time = 1.0
        self.complete = False
        self.process_kwargs(kwargs)
        self.ratio = self.rect.width / 100.0
        if self.text:
            self.text = self.font.render(self.text, True, self.font_color)

    def process_kwargs(self, kwargs):
        settings = {
            "color": (0, 0, 0),
            "bg_color": (255, 255, 255),
            "bg_buff": 1,
            "increment": 1,
            "percent": 0,
            "text": None,
            "font": pygame.font.Font(None, 20),
            "font_color": (0, 0, 0),
            "text_always": False
        }

        for kwarg in kwargs:
            if kwarg in settings:
                settings[kwarg] = kwargs[kwarg]
            else:
                raise AttributeError(
                    "{} nao faz parte do atributos aceitaveis.".format(kwarg)
                )

        # Cria os atributos para cada chave
        self.__dict__.update(settings)

    def update(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.timer > 1000 / self.time:
            self.percent += self.increment
            self.timer = self.current_time

        return self

    def render(self, screen):
        width = self.percent * self.ratio
        self.complete = False

        if self.percent >= 100:
            width = self.rect.width
            self.complete = True

        pygame.draw.rect(
            screen, self.bg_color,
            (self.rect.left - self.bg_buff,
             self.rect.top - self.bg_buff,
             self.max_width + self.bg_buff * 2,
             self.rect.height + self.bg_buff * 2)
        )

        pygame.draw.rect(
            screen, self.color,
            (self.rect.left,
             self.rect.top,
             width, self.rect.height))

        if self.text:
            if self.complete or self.text_always:
                text_rect = self.text.get_rect(center=self.rect.center)
                screen.blit(self.text, text_rect)


class Loader:
    def __init__(self, screen):
        pygame.init()
        self.screen = screen
        self.done = False
        self.clock = pygame.time.Clock()

        config = {
            "text": "Carregando",
            "color": (0, 0, 200),
            "bg_color": (255, 255, 255),
            "increment": 20,
            "text_always": True,
        }

        pos_x = 10
        pos_y = screen.get_rect().centery
        width = screen.get_rect().width - 20
        height = 25

        self.bar = ProgressBar((pos_x, pos_y, width, height), **config)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

    def update(self):
        self.bar.update()

    def render(self):
        self.bar.render(self.screen)

    def run(self):
        while not self.done:
            self.done = self.bar.complete
            self.events()
            self.update()
            self.render()
            pygame.display.update()
            self.clock.tick(60)
