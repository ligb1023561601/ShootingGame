# _*_ coding: utf-8 _*_
# @Time     : 2017/9/14 16:50
# @Author    : Ligb
# @File     : game_functions.py

import sys

import pygame

import bullet


def check_events(ai_setting, screen, ship, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, ai_setting, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)


def update_screen(ai_setting, screen, ship, bullets):
    """更新屏幕图像，并切换到新屏幕"""

    # 每次循环时都重绘屏幕
    screen.fill(ai_setting.bg_color)

    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()

    # 让最近绘制的屏幕可见,营造平滑移动的效果
    pygame.display.flip()


def check_keydown_event(event, ai_settings, screen, ship, bullets):
    """检测按键按下"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_event(event, ship):
    """检测按键弹起"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_bullet(bullets):
    """删除已经消失的子弹"""
    # 当对编组调用update（）时，会自动对编组中的每个精灵中的update（）方法调用，刷新子弹坐标
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def fire_bullet(ai_settings, screen, ship, bullets):
    """如果未达到子弹数量上限，创建一颗子弹并加入到编组中"""
    if len(bullets) <= ai_settings.bullet_allowed:
        new_bullet = bullet.Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
