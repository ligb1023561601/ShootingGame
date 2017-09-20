# _*_ coding: utf-8 _*_
# @Time     : 2017/9/20 9:34
# @Author    : Ligb
# @File     : score_board.py

import pygame.font
from pygame.sprite import Group

from ship import Ship


class Scoreboard(object):
    """显示得分信息"""

    def __init__(self, ai_settings, screen, status):
        """初始化显示得分"""
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.game_status = status

        # 字体属性
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # 初始得分图像，包括最高得分,游戏等级,剩余飞船
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """将得分渲染为图像，使其定位在右上角,并进行圆整"""
        rounded_score = round(self.game_status.score, -1)
        score = "Score " + "{:,}".format(rounded_score)
        self.score_image = self.font.render(score, True, self.text_color)
        self.score_image_rect = self.score_image.get_rect()
        self.score_image_rect.right = self.screen_rect.right - 20
        self.score_image_rect.top = 20

    def prep_high_score(self):
        """将最高分渲染为图像，使其定位在顶部中央,并进行圆整"""
        rounded_high_score = round(self.game_status.high_score, -1)
        score = "HighScore " + "{:,}".format(rounded_high_score)
        self.high_score_image = self.font.render(score, True, self.text_color)
        self.high_score_image_rect = self.high_score_image.get_rect()
        self.high_score_image_rect.centerx = self.screen_rect.centerx
        self.high_score_image_rect.top = 20

    def prep_level(self):
        """将游戏等级渲染为图像，使其定位在右上角"""
        level = "Level " + str(self.game_status.game_level)
        self.level_image = self.font.render(level, True, self.text_color)
        self.level_image_rect = self.level_image.get_rect()
        self.level_image_rect.right = self.screen_rect.right - 20
        self.level_image_rect.top = self.score_image_rect.bottom + 20

    def prep_ships(self):
        """显示剩余飞船数"""
        self.ships = Group()
        for ship_number in range(self.game_status.ship_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def draw_score_board(self):
        """显示得分"""
        self.screen.blit(self.score_image, self.score_image_rect)
        self.screen.blit(self.high_score_image, self.high_score_image_rect)
        self.screen.blit(self.level_image, self.level_image_rect)
        self.ships.draw(self.screen)