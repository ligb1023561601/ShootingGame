# _*_ coding: utf-8 _*_
# @Time     : 2017/9/14 15:04
# @Author    : Ligb
# @File     : settings.py


class Settings(object):
    """存储所有的设置"""

    def __init__(self):
        """初始化游戏设置"""
        self.screen_width = 1200
        self.self_height = 800

        # 由RGB值组合表示颜色
        self.bg_color = (230, 230, 230)

        # 飞船的设置
        self.ship_speed_factor = 2

        # 子弹的设置
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 16
        self.bullet_color = 60, 60, 60
        self.bullet_allowed = 10
