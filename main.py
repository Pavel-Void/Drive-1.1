import random

import pygame

WIN_WIDTH = 1024
WIN_HEIGHT = 768
FPS = 60
ROAD_STRIPES = 10

# цвета    R    G    B
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
PURPUL = (138, 43, 226)

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))


class Enemy(pygame.sprite.Sprite):
    image_list = ["Ambulance.png",
                  "Red_car.png",
                  "Black_car.png",
                  "Mini_truck.png",
                  "Mini_van.png",
                  "taxi.png"
                  ]

    def __init__(self, speed=6):
        super().__init__()
        img = random.choice(Enemy.image_list)
        self.image = pygame.image.load(img).convert_alpha()
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.generate_position()
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > WIN_HEIGHT:
            self.__init__(self.speed)

    def generate_position(self):
        self.rect.centerx = random.randrange(ROAD_STRIPES) * (WIN_WIDTH // ROAD_STRIPES) - (
                WIN_WIDTH // ROAD_STRIPES // 2) - Line.width // 2
        self.rect.bottom = random.randint(-WIN_HEIGHT, 0)
        if len(pygame.sprite.spritecollide(self, enemy_group, False)) > 1:
            self.generate_position()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, img="Car.png"):
        super().__init__()
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, event):
        player.rect.y = 650
        if event.type == pygame.KEYDOWN:
            keys[event.key] = True
        if event.type == pygame.KEYUP:
            keys[event.key] = False
        if keys[pygame.K_LEFT] and player.rect.centerx >= 0:
            player.rect.centerx -= 4
        if keys[pygame.K_RIGHT] and player.rect.centerx <= WIN_WIDTH:
            player.rect.centerx += 4


class Line(pygame.sprite.Sprite):
    width = 10
    height = 30

    def __init__(self, x):
        super().__init__()
        self.speed = 4
        self.rect = pygame.Rect(x, -Line.height, Line.width, Line.height)
        self.image = pygame.Surface((Line.width, Line.height))
        self.image.fill(WHITE)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > WIN_HEIGHT:
            self.kill()
        if 15 < self.rect.y <= 15 + self.speed:
            line_group.add(Line(self.rect.x))


class State:
    start = 0
    play = 1
    pause = 2
    gameover = 3


all_sprites_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
line_group = pygame.sprite.Group()
for i in range(10):
    enemy = Enemy()
    all_sprites_group.add(enemy)
    enemy_group.add(enemy)

player = Player(WIN_WIDTH // 2, WIN_HEIGHT - 100)
all_sprites_group.add(player)
for i in range(1, ROAD_STRIPES + 1):
    line_group.add(Line(WIN_WIDTH // ROAD_STRIPES * i - Line.width))

wallpaper = pygame.image.load("wallpaper.jpg")
crash = pygame.mixer.Sound("crash.wav")
crash.set_volume(0.5)
pygame.mixer.music.load("Kavinsky - Nightcall.mp3")
pygame.mixer.music.set_volume(0.1)
road = pygame.transform.scale(pygame.image.load("road.jpg"), (WIN_WIDTH, WIN_HEIGHT))

current_state = State.start
front = pygame.font.SysFont('Arial', 45)
keys = {
    pygame.K_LEFT: False,
    pygame.K_RIGHT: False,
}


def drawTextCenter(text, font, color, screen):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = WIN_WIDTH // 2
    text_rect.centery = WIN_HEIGHT // 2
    screen.blit(text_surface, text_rect)


background_shift_y = 0
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    if current_state == State.start:
        screen.blit(wallpaper, (0, 0))
        drawTextCenter('Drive...', front, PURPUL, screen)
        for event in events:
            if event.type == pygame.KEYDOWN:
                current_state = State.play
                pygame.mixer.music.play()
    elif current_state == State.play:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                current_state = State.pause
                pygame.mixer.music.pause()
        screen.blit(road, (0, background_shift_y))
        screen.blit(road, (0, -WIN_HEIGHT + background_shift_y))
        background_shift_y += 4
        player.update(event)
        if background_shift_y >= WIN_HEIGHT:
            background_shift_y = 0
        line_group.draw(screen)
        line_group.update()
        enemy_group.update()
        all_sprites_group.draw(screen)

        if pygame.sprite.spritecollideany(player, enemy_group):
            current_state = State.gameover
            pygame.mixer.music.stop()
            crash.play()

    elif current_state == State.pause:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                current_state = State.play
                pygame.mixer.music.unpause()
        screen.blit(road, (0, background_shift_y))
        screen.blit(road, (0, -WIN_HEIGHT + background_shift_y))
        line_group.draw(screen)
        all_sprites_group.draw(screen)
        drawTextCenter('Пауза', front, BLACK, screen)

    elif current_state == State.gameover:
        screen.blit(road, (0, background_shift_y))
        screen.blit(road, (0, -WIN_HEIGHT + background_shift_y))
        line_group.draw(screen)
        all_sprites_group.draw(screen)
        drawTextCenter('Вы проиграли :(', front, BLACK, screen)

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
