# _*_ coding: utf-8 _*_
# @Time     : 2017/9/14 15:04
# @Author    : Ligb
# @File     : settings.py


class Settings(object):
    """存储所有的设置"""

    def __init__(self):
        """初始化游戏设置"""
        self.screen_width = 1200
        self.screen_height = 800

        # 由RGB值组合表示颜色
        self.bg_color = (230, 230, 230)

        # 飞船的设置
        self.ship_limit = 1

        # 子弹的设置
        self.bullet_width = 3
        self.bullet_height = 16
        self.bullet_color = 60, 60, 60
        self.bullet_allowed = 4

        # 外星人设置
        self.alien_drop_speed_factor = 40

        # 加快游戏节奏
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        # 计分
        self.alien_points = 50

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """将所有静态初始化设置归在一起"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3

        # 外星人设置,方向1为向右，-1为向左
        self.alien_speed_factor = 0.5
        self.fleet_direction = 1

    def increase_speed(self):
        """提高速度设置,提高得分"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.score_scale * self.alien_points)

