# _*_ coding: utf-8 _*_
# @Time     : 2017/9/14 12:16
# @Author    : Ligb
# @File     : alien_invasion.py

import sys
import pygame
from pygame.sprite import Group

import settings
from ship import Ship
from alien import Alien
from game_stats import GameStatus
from button import Button
from score_board import Scoreboard
import game_functions


def run_game():
    """初始化游戏并创建屏幕对象"""
    pygame.init()
    ai_setting = settings.Settings()
    screen = pygame.display.set_mode((ai_setting.screen_width, ai_setting.screen_height))
    pygame.display.set_caption("Alien Invasion")
    play_button = Button(ai_setting, screen, "Play")

    # 创建一艘飞船
    ship = Ship(ai_setting, screen)

    # 创建一个用于存储子弹的编组
    bullets = Group()

    # 创建外星人编组
    aliens = Group()
    game_functions.create_fleet(ai_setting, screen, aliens, ship)

    # 创建游戏数据
    game_status = GameStatus(ai_setting)
    scoreboard = Scoreboard(ai_setting, screen, game_status)

    # 游戏主循环
    while True:
        game_functions.check_events(ai_setting, screen, aliens, ship, bullets, game_status, play_button, scoreboard)

        if game_status.game_active:
            ship.update()
            game_functions.update_bullet(aliens, bullets, ai_setting, screen, ship, game_status, scoreboard)
            game_functions.update_aliens(aliens, ai_setting, ship, game_status, screen, bullets, scoreboard)

        game_functions.update_screen(ai_setting, screen, ship, aliens, bullets, game_status, play_button, scoreboard)

run_game()
