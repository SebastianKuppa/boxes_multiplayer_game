from boxes import BoxesGame
# test

if __name__ == '__main__':
    bg = BoxesGame()

    while True:
        if bg.update() == 1:
            break

    bg.finished()
