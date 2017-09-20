# _*_ coding: utf-8 _*_
# @Time     : 2017/9/14 15:22
# @Author    : Ligb
# @File     : ship.py

import pygame

from pygame.sprite import Sprite


class Ship(Sprite):
    """飞船相关"""

    def __init__(self, ai_settings, screen):
        """初始化飞船并设置其初始位置"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()

        # 获取屏幕的矩形
        self.screen_rect = screen.get_rect()

        # 将每艘飞船放在屏幕底中央,为了存小数点定义了center
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)

        # 持续移动的标志
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """根据持续移动标志调整飞船位置,用if能同时按两个键然后保持不动，elif则不能
        并限制其活动范围在屏幕内"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        self.rect.centerx = self.center

    def center_ship(self):
        """飞船居中"""
        self.rect.centerx = self.screen_rect.centerx
