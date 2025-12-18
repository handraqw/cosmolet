import pygame
import random

# Настройки окна
WIDTH, HEIGHT = 640, 480

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Космолет")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
SHIP_COLOR = (0, 255, 255)
BULLET_COLOR = (255, 255, 0)
METEOR_COLOR = (255, 80, 80)
BG_COLOR = (10, 10, 16)

class Ship:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 40
        self.size = 32
        self.alive = True

    def move(self, dx):
        self.x = min(max(self.x + dx, self.size//2), WIDTH - self.size//2)

    def draw(self):
        # Треугольник
        points = [
            (self.x, self.y - self.size//2),
            (self.x - self.size//2, self.y + self.size//2),
            (self.x + self.size//2, self.y + self.size//2)
        ]
        pygame.draw.polygon(screen, SHIP_COLOR, points)

    def rect(self):
        return pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        self.y -= 10

    def draw(self):
        pygame.draw.rect(screen, BULLET_COLOR, (self.x-3, self.y-14, 6, 14))

    def rect(self):
        return pygame.Rect(self.x-3, self.y-14, 6, 14)

class Meteor:
    def __init__(self):
        self.radius = random.randint(14, 28)
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = -self.radius
        self.speed = random.randint(2, 5)

    def move(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.circle(screen, METEOR_COLOR, (self.x, self.y), self.radius)

    def rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)

def main():
    ship = Ship()
    bullets = []
    meteors = []
    spawn_counter = 0
    run = True

    while run:
        clock.tick(50)
        screen.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_SPACE and ship.alive:
                    bullets.append(Bullet(ship.x, ship.y - ship.size//2))

        keys = pygame.key.get_pressed()
        if ship.alive:
            if keys[pygame.K_LEFT]:
                ship.move(-7)
            if keys[pygame.K_RIGHT]:
                ship.move(7)

        # Меториты появляются
        spawn_counter += 1
        if ship.alive and spawn_counter > 25:
            meteors.append(Meteor())
            spawn_counter = 0

        # Движение и удаление пуль
        for b in bullets:
            b.move()
        bullets[:] = [b for b in bullets if b.y > -20]

        # Движение и удаление метеоров
        for m in meteors:
            m.move()
        meteors[:] = [m for m in meteors if m.y < HEIGHT + m.radius]

        # Проверка столкновений пуля/метеорит
        for b in bullets[:]:
            for m in meteors[:]:
                if b.rect().colliderect(m.rect()):
                    try:
                        bullets.remove(b)
                        meteors.remove(m)
                    except ValueError:
                        pass

        # Проверка столкновения корабля и метеора
        if ship.alive:
            for m in meteors:
                if ship.rect().colliderect(m.rect()):
                    ship.alive = False

        # Рисуем всё
        if ship.alive:
            ship.draw()
        else:
            font = pygame.font.SysFont("Arial", 48)
            text = font.render("GAME OVER", True, WHITE)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))

        for b in bullets:
            b.draw()
        for m in meteors:
            m.draw()

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()