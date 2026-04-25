import pygame
import sys
from racer import GameSession
from ui import (main_menu, settings_screen, username_screen,
                game_over_screen, leaderboard_screen, draw_hud,
                draw_background, DARK, PINK, WHITE)
from persistence import load_settings, save_settings, load_leaderboard, save_score
 
W, H = 480, 720
FPS = 60
 
STATE_MENU = "menu"
STATE_USERNAME = "username"
STATE_GAME = "game"
STATE_GAMEOVER = "gameover"
STATE_LEADERBOARD = "leaderboard"
STATE_SETTINGS = "settings"
 
 
def apply_music(sound_on):
    if sound_on:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()
 
 
def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Racer ♥")
    clock = pygame.time.Clock()
 
    settings = load_settings()
    leaderboard = load_leaderboard()
 
    try:
        pygame.mixer.music.load("assets/music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        if not settings["sound"]:
            pygame.mixer.music.pause()
    except Exception:
        pass
 
    state = STATE_MENU
    username = ""
    username_buf = ""
    session = None
    menu_scroll = 0
    final_score = final_dist = final_coins = 0
 
    while True:
        dt = clock.tick(FPS) / 1000.0
        mouse_pos = pygame.mouse.get_pos()
        menu_scroll = (menu_scroll + 1) % 10000
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_settings(settings)
                pygame.quit()
                sys.exit()
 
            if state == STATE_MENU:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    btns = main_menu(screen, W, H, mouse_pos, menu_scroll)
                    for i, r in enumerate(btns):
                        if r.collidepoint(mouse_pos):
                            if i == 0:
                                state = STATE_USERNAME
                                username_buf = ""
                            elif i == 1:
                                leaderboard = load_leaderboard()
                                state = STATE_LEADERBOARD
                            elif i == 2:
                                state = STATE_SETTINGS
                            elif i == 3:
                                save_settings(settings)
                                pygame.quit()
                                sys.exit()
 
            elif state == STATE_USERNAME:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and username_buf.strip():
                        username = username_buf.strip()
                        session = GameSession(W, H, settings["car_color"], settings["difficulty"])
                        state = STATE_GAME
                    elif event.key == pygame.K_BACKSPACE:
                        username_buf = username_buf[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        state = STATE_MENU
                    else:
                        if len(username_buf) < 16 and event.unicode.isprintable():
                            username_buf += event.unicode
 
            elif state == STATE_GAME:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = STATE_MENU
                    else:
                        session.on_key_down(event.key)
 
            elif state == STATE_GAMEOVER:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    btns = game_over_screen(screen, W, H, mouse_pos,
                                            final_score, final_dist, final_coins, menu_scroll)
                    for i, r in enumerate(btns):
                        if r.collidepoint(mouse_pos):
                            if i == 0:
                                session = GameSession(W, H, settings["car_color"], settings["difficulty"])
                                state = STATE_GAME
                            elif i == 1:
                                state = STATE_MENU
 
            elif state == STATE_LEADERBOARD:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    btns = leaderboard_screen(screen, W, H, mouse_pos, leaderboard, menu_scroll)
                    if btns[0].collidepoint(mouse_pos):
                        state = STATE_MENU
 
            elif state == STATE_SETTINGS:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    items = settings_screen(screen, W, H, mouse_pos, settings, menu_scroll)
                    for tag, item in items:
                        if tag == "sound" and item.collidepoint(mouse_pos):
                            settings["sound"] = not settings["sound"]
                            save_settings(settings)
                            apply_music(settings["sound"])
                        elif tag == "color_row":
                            for name, cr in item.items():
                                if cr.collidepoint(mouse_pos):
                                    settings["car_color"] = name
                                    save_settings(settings)
                        elif tag == "diff_row":
                            for d, dr in item.items():
                                if dr.collidepoint(mouse_pos):
                                    settings["difficulty"] = d
                                    save_settings(settings)
                        elif tag == "back" and item.collidepoint(mouse_pos):
                            state = STATE_MENU
 
        if state == STATE_GAME and session:
            session.update(dt)
            if not session.alive:
                final_score = session.score
                final_dist = session.distance
                final_coins = session.coins
                leaderboard = save_score(username, final_score, final_dist, final_coins)
                state = STATE_GAMEOVER
 
        screen.fill(DARK)
 
        if state == STATE_MENU:
            main_menu(screen, W, H, mouse_pos, menu_scroll)
 
        elif state == STATE_USERNAME:
            username_screen(screen, W, H, username_buf, menu_scroll)
 
        elif state == STATE_GAME and session:
            session.draw(screen)
            draw_hud(screen, W, session.score, session.distance, session.coins,
                     session.active_powerup, session.powerup_timer,
                     session.shield_active, 0)
 
        elif state == STATE_GAMEOVER:
            game_over_screen(screen, W, H, mouse_pos, final_score, final_dist, final_coins, menu_scroll)
 
        elif state == STATE_LEADERBOARD:
            leaderboard_screen(screen, W, H, mouse_pos, leaderboard, menu_scroll)
 
        elif state == STATE_SETTINGS:
            settings_screen(screen, W, H, mouse_pos, settings, menu_scroll)
 
        pygame.display.flip()
 
 
if __name__ == "__main__":
    main()