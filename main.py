# 游戏主入口
import pygame
from source import tools, setup
from source.setup import GRAPHICS
from source.states import main_menu, load_screen, level


def main():

    states = {'main_menu': main_menu.MainMenu(), 'load_screen': load_screen.LoadScreen(), 'level': level.Level()}
    game = tools.Game(states, 'main_menu')
    game.run()

if __name__ == '__main__':
    main()