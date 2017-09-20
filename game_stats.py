# _*_ coding: utf-8 _*_
# @Time     : 2017/9/19 14:37
# @Author    : Ligb
# @File     : game_stats.py

import json


class GameStatus(object):
    """游戏数据统计的类"""
    def __init__(self, ai_settings):
        """初始化,启动时游戏非活跃需要按钮启动"""
        self.ai_setting = ai_settings
        self.game_active = False

        # 读取历史最高分
        file_path = "high_score.json"
        with open(file_path) as high_score:
            self.high_score = json.load(high_score)
        self.reset_status()

    def reset_status(self):
        """初始化游戏起始时的信息"""
        self.ship_left = self.ai_setting.ship_limit
        self.score = 0

        # 游戏等级
        self.game_level = 1
