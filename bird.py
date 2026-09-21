from pygame import *
import random
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WIDTH, HEIGHT = 1000, 800
init()
WIN = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Flappy Bird")
clock = time.Clock()

BIRD_IMG = image.load(os.path.join(BASE_DIR, "bird.png"))
PIPE_IMG = image.load(os.path.join(BASE_DIR, "pipe.png"))


class Sprite:
    def __init__(self, x, y, w, h, img):
        self.rect = Rect(x, y, w, h)
        self.image = transform.scale(img, (w, h))

    def draw(self):
        WIN.blit(self.image, (self.rect.x, self.rect.y))


class Player(Sprite):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, BIRD_IMG)
        self.speed = 7

    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed


class Pipe:
    def __init__(self, x):
        self.gap = random.randint(160, 240)
        self.w = 80
        self.top_h = random.randint(50, HEIGHT - self.gap - 50)

        top_img = transform.flip(PIPE_IMG, False, True)
        self.top_sprite = Sprite(x, 0, self.w, self.top_h, top_img)

        bottom_y = self.top_h + self.gap
        bottom_h = HEIGHT - bottom_y
        self.bottom_sprite = Sprite(x, bottom_y, self.w, bottom_h, PIPE_IMG)

    def update(self):
        self.top_sprite.rect.x -= 5
        self.bottom_sprite.rect.x -= 5

    def draw(self):
        self.top_sprite.draw()
        self.bottom_sprite.draw()


player = Player(100, HEIGHT // 2 - 25, 60, 45)
pipes = []

SPAWNPIPE = USEREVENT + 1
time.set_timer(SPAWNPIPE, 1500)

running = True
while running:
    clock.tick(60)

    for e in event.get():
        if e.type == QUIT:
            running = False

        if e.type == SPAWNPIPE:
            pipes.append(Pipe(WIDTH))

    player.update()

    for pipe in pipes[:]:
        pipe.update()
        if pipe.top_sprite.rect.right < 0:
            pipes.remove(pipe)

    WIN.fill((30, 30, 30))

    for pipe in pipes:
        pipe.draw()

    player.draw()

    display.update()

quit()