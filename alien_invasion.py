# _*_ coding: utf-8 _*_
# @Time     : 2017/9/14 12:16
# @Author    : Ligb
# @File     : alien_invasion.py

import sys
import pygame
from pygame.sprite import Group

import settings
from ship import Ship
import game_functions


def run_game():
    """初始化游戏并创建屏幕对象"""
    pygame.init()
    ai_setting = settings.Settings()
    screen = pygame.display.set_mode((ai_setting.screen_width, ai_setting.self_height))
    pygame.display.set_caption("Alien Invasion")

    # 创建一艘飞船
    ship = Ship(ai_setting, screen)

    # 创建一个用于存储子弹的编组
    bullets = Group()

    # 游戏主循环
    while True:
        game_functions.check_events(ai_setting, screen, ship, bullets)
        ship.update()
        game_functions.update_bullet(bullets)
        game_functions.update_screen(ai_setting, screen, ship, bullets)


run_game()
