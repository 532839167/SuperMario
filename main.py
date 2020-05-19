# 游戏主入口
import pygame

from source import tools, setup
from source.setup import GRAPHICS


def main():
    game = tools.Game()
    game.run(setup, GRAPHICS)

if __name__ == '__main__':
    main()