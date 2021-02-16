# -*- coding: utf-8 -*-
import pygame
from pygame import *
from player import *
from blocks import *
from win import *
import random
from enemy import *
# Объявляем переменные
WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 640  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#00A2E8"
win = 0


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


def main():
    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    pygame.display.set_caption("Super Mario Boy")  # Пишем в шапку
    bg = pygame.image.load("bg.jpg")

    hero = Player(55, 55)  # создаем героя по (x,y) координатам
    left = right = False  # по умолчанию - стоим
    up = False

    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться
    enemies = []

    entities.add(hero)

    level = [
        "----------------------------------",
        "-                                -",
        "-                              * -",
        "-                                -",
        "-                                -",
        "-                                -",
        "-                                -",
        "-                                -",
        "-                                -",
        "-                                -",
        "-                                -",
        "-                                -",
        "-                                -",
        "-                                -",
        "-                                -",
        "-                                -",
        "-                                -",
        "-                                -",
        "-                                -",
        "-                                -",
        "-                                -",
        "-                                -",
        "-                                -",
        "----------------------------------"]
    generate_level(level, len(level[0]))
    timer = pygame.time.Clock()
    x = y = 0  # координаты
    first = True
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "*":
                win = Win(x+1, y)
                entities.add(win)
                first = False
            if col == "/":
                en = Enemy(x, y)
                entities.add(en)
                enemies.append(en)

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    while 1:  # Основной цикл программы
        timer.tick(60)
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == QUIT:
                raise SystemExit
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False

        screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать

        camera.update(hero)  # центризируем камеру относительно персонажа
        hero.update(left, right, up, platforms, win, enemies)  # передвижение
        # entities.draw(screen) # отображение
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()  # обновление и вывод всех изменений на экран
        if hero.isWin or hero.isLose:
            pygame.quit()
            break


def generate_level(level, l):
    counter = 0
    while counter < 40:
        x = random.randint(0, len(level) - 1)
        y = random.randint(0, len(level[x]) - 1)
        if (level[x][y] == " ") and x > 2 and y > 2:
            level[x] = level[x][:y] + "-" + level[x][y - 1:]
            counter += 1
    for i in range(len(level)):
        level[i] = level[i][:l - 1] + "-"
    for i in range(len(level)):
        if level[-2][i] != "-" and i != 1 and i != 2:
            if not random.randint(0, 2):
                level[-2] = level[-2][:i] + "/" + level[-2][i-1:]


if __name__ == "__main__":
    main()
