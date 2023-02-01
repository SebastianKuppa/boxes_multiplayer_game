import pygame

from boxes import BoxesGame


if __name__ == '__main__':
    bg = BoxesGame()

    while True:
        bg.update()
