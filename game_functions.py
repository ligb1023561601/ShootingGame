# _*_ coding: utf-8 _*_
# @Time     : 2017/9/14 16:50
# @Author    : Ligb
# @File     : game_functions.py

import sys
import pygame
import json

import bullet
from time import sleep
from alien import Alien


def check_events(ai_setting, screen, aliens, ship, bullets, game_status, play_button,scoreboard):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, ai_setting, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 返回一个元组
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(mouse_x, mouse_y, play_button, game_status, ai_setting, screen,
                              aliens, bullets, ship, scoreboard)


def update_screen(ai_setting, screen, ship, aliens, bullets, game_status, play_button, scoreboard):
    """更新屏幕图像，并切换到新屏幕"""

    # 每次循环时都重绘屏幕
    screen.fill(ai_setting.bg_color)

    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()

    # 对编组调用draw方法时，pygame自动绘制各个元素
    aliens.draw(screen)

    # 如果游戏未开启，则显示按钮
    if not game_status.game_active:
        play_button.draw_button()

    # 绘制记分牌
    scoreboard.draw_score_board()

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


def update_bullet(aliens, bullets, ai_settings, screen, ship, game_status, scoreboard):
    """删除已经消失的子弹"""
    # 当对编组调用update（）时，会自动对编组中的每个精灵中的update（）方法调用，刷新子弹坐标
    # 检查子弹与外星人是否相撞，groupcollide方法会返回一个字典，键为子弹，值为外星人,两个bool值表示是否删除产生碰撞的两个元素
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    collisiongs = check_bullet_alien_collision(bullets, aliens, ai_settings, screen, ship, game_status, scoreboard)


def fire_bullet(ai_settings, screen, ship, bullets):
    """如果未达到子弹数量上限，创建一颗子弹并加入到编组中"""
    if len(bullets) <= ai_settings.bullet_allowed:
        new_bullet = bullet.Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def create_fleet(ai_setting, screen, aliens, ship):
    """创建外星人群，计算一行可容纳多少个"""
    alien = Alien(ai_setting, screen)
    number_aliens_x = get_number_aliens_x(ai_setting, alien.rect.width)
    number_rows = get_number_rows(ai_setting, ship.rect.height, alien.rect.height)
    create_alien(number_aliens_x, number_rows, ai_setting, screen, alien.rect.width, aliens)


def get_number_aliens_x(ai_setting, alien_width):
    """获取一行能容纳的外星人数目"""
    available_space_x = ai_setting.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """获取屏幕能容纳的外星人行数，要考虑初始时外星人与飞船留有一定间距"""
    available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(number_aliens_x, number_rows, ai_setting, screen, alien_width, aliens):
    """循环创建一群外星人"""
    for number_row in range(number_rows):
        for alien_number in range(number_aliens_x):
            alien = Alien(ai_setting, screen)
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            alien.y = alien.rect.height + 2 * number_row * alien.rect.height
            alien.rect.y = alien.y
            aliens.add(alien)


def update_aliens(aliens, ai_settings, ship, game_status, screen, bullets, scoreboard):
    """更新外星人的坐标,并检测是否碰撞了飞船或者是否有外星人到达底端"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(game_status, aliens, bullets, ai_settings, screen, ship, scoreboard)

    # 触底
    check_aliens_bottom(screen, aliens, game_status, bullets, ai_settings, ship, scoreboard)


def check_fleet_edges(ai_settings, aliens):
    """一旦到达右边缘，即改变方向"""
    for alien in aliens.sprites():
        if alien.check_edge():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """改变方向并向下移动"""
    for alien in aliens.sprites():
        alien.y += ai_settings.alien_drop_speed_factor
        alien.rect.y = alien.y

    ai_settings.fleet_direction *= -1


def check_bullet_alien_collision(bullets, aliens, ai_settings, screen, ship, game_status, scoreboard):
    """检查子弹是否击中外星人,清空一群后加速"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    # 击中后检查得分,并更新得分的图像进行显示，要将每个消灭的外星人都作为得分
    if collisions:
        for aliens in collisions.values():
            game_status.score += ai_settings.alien_points * len(aliens)
            scoreboard.prep_score()
        check_high_score(game_status, scoreboard)

    # 清空完了一群外星人
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, aliens, ship)

        # 提高等级
        game_status.game_level += 1
        scoreboard.prep_level()
    return collisions


def ship_hit(game_status, aliens, bullets, ai_settings, screen, ship, scoreboard):
    """飞船碰撞后清屏并产生一群新的外星人"""
    # 减少一艘飞船数
    game_status.ship_left -= 1

    if game_status.ship_left > 0:
        # 清空子弹与外星人,飞船减一
        aliens.empty()
        bullets.empty()
        scoreboard.prep_ships()

        # 新建一群外星人
        create_fleet(ai_settings, screen, aliens, ship)

        # 飞船居中
        ship.center_ship()
        sleep(1)
    else:
        # 飞船撞完，设为不活跃，显示play与鼠标
        game_status.game_active = False
        pygame.mouse.set_visible(True)
        scoreboard.prep_ships()


def check_aliens_bottom(screen, aliens, game_status, bullets, ai_settings, ship, scoreboard):
    """检查外星人触底"""
    screen_rect = screen.get_rect()

    for alien in aliens.copy():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(game_status, aliens, bullets, ai_settings, screen, ship, scoreboard)
            break


def check_play_button(mouse_x, mouse_y, play_button, game_status, ai_settings, screen, aliens, bullets, ship, scoreboard):
    """单击Play按钮时开始新游戏"""
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not game_status.game_active:

        # 开始后让鼠标光标隐藏,并重置速度设置
        pygame.mouse.set_visible(False)
        ai_settings.initialize_dynamic_settings()

        # 重置游戏统计信息
        game_status.reset_status()
        scoreboard.prep_score()
        scoreboard.prep_level()
        scoreboard.prep_ships()
        game_status.game_active = True

        # 清空外星人列表和子弹
        aliens.empty()
        bullets.empty()

        # 重建外星人并让飞船居中
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()


def check_high_score(game_status, scoreboard):
    """检查是否产生了最高分,并存入json"""
    if game_status.score > game_status.high_score:
        game_status.high_score = game_status.score
        scoreboard.prep_high_score()
        file_path = "high_score.json"
        with open(file_path, "w") as high_score:
            json.dump(game_status.high_score, high_score)