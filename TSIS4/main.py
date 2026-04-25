import sys
import pygame
from config import *
from game import Game

try:
    import db
    db.init_db()
    DB_AVAILABLE = True
    print("DB connected OK")
except Exception as e:
    DB_AVAILABLE = False
    print(f"DB not available: {e}")


def draw_background(surface):
    surface.fill(BG_COLOR)


def draw_text(surface, text, font, color, x, y, center=True):
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.centerx = x
        rect.y = y
    else:
        rect.x = x
        rect.y = y
    surface.blit(surf, rect)
    return rect


def draw_button(surface, text, font, rect, hover=False):
    color = LIGHT_GRAY if hover else GRAY
    pygame.draw.rect(surface, color, rect, border_radius=8)
    pygame.draw.rect(surface, WHITE, rect, 2, border_radius=8)
    txt_surf = font.render(text, True, WHITE)
    txt_rect = txt_surf.get_rect(center=rect.center)
    surface.blit(txt_surf, txt_rect)


def make_button(text, font, cx, y, w=220, h=48):
    rect = pygame.Rect(0, y, w, h)
    rect.centerx = cx
    return rect


class MainMenu:
    def __init__(self, surface, clock, settings):
        self.surface = surface
        self.clock = clock
        self.settings = settings
        self.font_title = pygame.font.SysFont("consolas", 52, bold=True)
        self.font_btn = pygame.font.SysFont("consolas", 26)
        self.font_sm = pygame.font.SysFont("consolas", 20)
        self.username = ""
        self.typing = True
        cx = WINDOW_WIDTH // 2
        self.btn_play = make_button("PLAY", self.font_btn, cx, 330)
        self.btn_lb = make_button("LEADERBOARD", self.font_btn, cx, 395)
        self.btn_settings = make_button("SETTINGS", self.font_btn, cx, 460)
        self.btn_quit = make_button("QUIT", self.font_btn, cx, 525)

    def run(self):
        while True:
            dt = self.clock.tick(FPS)
            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and self.typing:
                    if event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    elif event.key == pygame.K_RETURN:
                        if self.username.strip():
                            self.typing = False
                    elif len(self.username) < 20 and event.unicode.isprintable():
                        self.username += event.unicode
                if event.type == pygame.MOUSEBUTTONDOWN and not self.typing:
                    if self.btn_play.collidepoint(mouse):
                        return "play", self.username.strip()
                    if self.btn_lb.collidepoint(mouse):
                        return "leaderboard", self.username.strip()
                    if self.btn_settings.collidepoint(mouse):
                        return "settings", self.username.strip()
                    if self.btn_quit.collidepoint(mouse):
                        pygame.quit()
                        sys.exit()

            draw_background(self.surface)
            draw_text(self.surface, "SNAKE", self.font_title, GREEN,
                      WINDOW_WIDTH // 2, 60)

            prompt = "Enter username:" if self.typing else f"Player: {self.username}"
            color = YELLOW if self.typing else WHITE
            draw_text(self.surface, prompt, self.font_sm, color, WINDOW_WIDTH // 2, 180)

            if self.typing:
                input_rect = pygame.Rect(WINDOW_WIDTH // 2 - 140, 210, 280, 40)
                pygame.draw.rect(self.surface, GRAY, input_rect, border_radius=6)
                pygame.draw.rect(self.surface, WHITE, input_rect, 2, border_radius=6)
                name_surf = self.font_sm.render(self.username + "|", True, WHITE)
                self.surface.blit(name_surf, (input_rect.x + 8, input_rect.y + 8))
                hint = self.font_sm.render("Press Enter to confirm", True, LIGHT_GRAY)
                self.surface.blit(hint, hint.get_rect(centerx=WINDOW_WIDTH // 2, y=260))
            else:
                for btn, label in [
                    (self.btn_play, "PLAY"),
                    (self.btn_lb, "LEADERBOARD"),
                    (self.btn_settings, "SETTINGS"),
                    (self.btn_quit, "QUIT"),
                ]:
                    draw_button(self.surface, label, self.font_btn, btn,
                                hover=btn.collidepoint(mouse))

            pygame.display.flip()


class GameOverScreen:
    def __init__(self, surface, clock, score, level, personal_best):
        self.surface = surface
        self.clock = clock
        self.score = score
        self.level = level
        self.personal_best = personal_best
        self.font_title = pygame.font.SysFont("consolas", 48, bold=True)
        self.font_md = pygame.font.SysFont("consolas", 26)
        self.font_btn = pygame.font.SysFont("consolas", 24)
        cx = WINDOW_WIDTH // 2
        self.btn_retry = make_button("RETRY", self.font_btn, cx, 380)
        self.btn_menu = make_button("MAIN MENU", self.font_btn, cx, 445)

    def run(self):
        while True:
            self.clock.tick(FPS)
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.btn_retry.collidepoint(mouse):
                        return "retry"
                    if self.btn_menu.collidepoint(mouse):
                        return "menu"

            draw_background(self.surface)
            draw_text(self.surface, "GAME OVER", self.font_title, RED,
                      WINDOW_WIDTH // 2, 80)
            draw_text(self.surface, f"Score: {self.score}", self.font_md, WHITE,
                      WINDOW_WIDTH // 2, 200)
            draw_text(self.surface, f"Level reached: {self.level}", self.font_md, WHITE,
                      WINDOW_WIDTH // 2, 240)
            best_color = YELLOW if self.score >= self.personal_best else LIGHT_GRAY
            draw_text(self.surface, f"Personal best: {self.personal_best}", self.font_md,
                      best_color, WINDOW_WIDTH // 2, 280)
            if self.score >= self.personal_best:
                draw_text(self.surface, "NEW RECORD!", self.font_md, YELLOW,
                          WINDOW_WIDTH // 2, 320)

            for btn, label in [(self.btn_retry, "RETRY"), (self.btn_menu, "MAIN MENU")]:
                draw_button(self.surface, label, self.font_btn, btn,
                            hover=btn.collidepoint(mouse))
            pygame.display.flip()


class LeaderboardScreen:
    def __init__(self, surface, clock):
        self.surface = surface
        self.clock = clock
        self.font_title = pygame.font.SysFont("consolas", 40, bold=True)
        self.font_hdr = pygame.font.SysFont("consolas", 20, bold=True)
        self.font_row = pygame.font.SysFont("consolas", 18)
        self.font_btn = pygame.font.SysFont("consolas", 24)
        self.btn_back = make_button("BACK", self.font_btn, WINDOW_WIDTH // 2, 540)
        self.rows = []
        if DB_AVAILABLE:
            try:
                self.rows = db.get_top10()
            except Exception:
                pass

    def run(self):
        while True:
            self.clock.tick(FPS)
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.btn_back.collidepoint(mouse):
                        return

            draw_background(self.surface)
            draw_text(self.surface, "LEADERBOARD", self.font_title, YELLOW,
                      WINDOW_WIDTH // 2, 30)

            headers = ["#", "Username", "Score", "Level", "Date"]
            col_x = [30, 80, 320, 430, 530]
            y = 100
            for i, h in enumerate(headers):
                surf = self.font_hdr.render(h, True, CYAN)
                self.surface.blit(surf, (col_x[i], y))
            pygame.draw.line(self.surface, LIGHT_GRAY, (20, y + 24), (WINDOW_WIDTH - 20, y + 24), 1)

            for rank, row in enumerate(self.rows, 1):
                y2 = 130 + (rank - 1) * 34
                color = YELLOW if rank == 1 else WHITE
                vals = [
                    str(rank),
                    row["username"][:16],
                    str(row["score"]),
                    str(row["level_reached"]),
                    row["date"],
                ]
                for i, v in enumerate(vals):
                    surf = self.font_row.render(v, True, color)
                    self.surface.blit(surf, (col_x[i], y2))

            if not self.rows:
                draw_text(self.surface, "No records yet", self.font_hdr, LIGHT_GRAY,
                          WINDOW_WIDTH // 2, 200)

            draw_button(self.surface, "BACK", self.font_btn, self.btn_back,
                        hover=self.btn_back.collidepoint(mouse))
            pygame.display.flip()


class SettingsScreen:
    def __init__(self, surface, clock, settings):
        self.surface = surface
        self.clock = clock
        self.settings = dict(settings)
        self.font_title = pygame.font.SysFont("consolas", 40, bold=True)
        self.font_md = pygame.font.SysFont("consolas", 24)
        self.font_btn = pygame.font.SysFont("consolas", 22)
        cx = WINDOW_WIDTH // 2
        self.btn_grid = make_button("", self.font_btn, cx + 120, 200, 100, 40)
        self.btn_sound = make_button("", self.font_btn, cx + 120, 260, 100, 40)
        self.btn_color_r = make_button("Red+", self.font_btn, 160, 340, 90, 36)
        self.btn_color_g = make_button("Grn+", self.font_btn, 270, 340, 90, 36)
        self.btn_color_b = make_button("Blu+", self.font_btn, 380, 340, 90, 36)
        self.btn_color_rm = make_button("Red-", self.font_btn, 160, 384, 90, 36)
        self.btn_color_gm = make_button("Grn-", self.font_btn, 270, 384, 90, 36)
        self.btn_color_bm = make_button("Blu-", self.font_btn, 380, 384, 90, 36)
        self.btn_save = make_button("SAVE & BACK", self.font_btn, cx, 490, 240, 48)

    def _toggle(self, key):
        self.settings[key] = not self.settings[key]

    def _clamp_color(self, idx, delta):
        c = list(self.settings["snake_color"])
        c[idx] = max(0, min(255, c[idx] + delta))
        self.settings["snake_color"] = c

    def run(self):
        while True:
            self.clock.tick(FPS)
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.btn_grid.collidepoint(mouse):
                        self._toggle("grid_overlay")
                    elif self.btn_sound.collidepoint(mouse):
                        self._toggle("sound")
                    elif self.btn_color_r.collidepoint(mouse):
                        self._clamp_color(0, 20)
                    elif self.btn_color_g.collidepoint(mouse):
                        self._clamp_color(1, 20)
                    elif self.btn_color_b.collidepoint(mouse):
                        self._clamp_color(2, 20)
                    elif self.btn_color_rm.collidepoint(mouse):
                        self._clamp_color(0, -20)
                    elif self.btn_color_gm.collidepoint(mouse):
                        self._clamp_color(1, -20)
                    elif self.btn_color_bm.collidepoint(mouse):
                        self._clamp_color(2, -20)
                    elif self.btn_save.collidepoint(mouse):
                        save_settings(self.settings)
                        return self.settings

            draw_background(self.surface)
            draw_text(self.surface, "SETTINGS", self.font_title, CYAN,
                      WINDOW_WIDTH // 2, 40)

            draw_text(self.surface, "Grid overlay:", self.font_md, WHITE,
                      200, 210, center=False)
            grid_label = "ON" if self.settings["grid_overlay"] else "OFF"
            grid_col = GREEN if self.settings["grid_overlay"] else RED
            draw_button(self.surface, grid_label, self.font_btn, self.btn_grid,
                        hover=self.btn_grid.collidepoint(mouse))

            draw_text(self.surface, "Sound:", self.font_md, WHITE, 200, 270, center=False)
            snd_label = "ON" if self.settings["sound"] else "OFF"
            draw_button(self.surface, snd_label, self.font_btn, self.btn_sound,
                        hover=self.btn_sound.collidepoint(mouse))
            _ = grid_col
            _ = snd_label

            draw_text(self.surface, "Snake color:", self.font_md, WHITE, 30, 315, center=False)
            preview_rect = pygame.Rect(490, 350, 60, 60)
            pygame.draw.rect(self.surface, tuple(self.settings["snake_color"]), preview_rect,
                             border_radius=6)
            pygame.draw.rect(self.surface, WHITE, preview_rect, 2, border_radius=6)

            for btn, label in [
                (self.btn_color_r, "R+"), (self.btn_color_g, "G+"), (self.btn_color_b, "B+"),
                (self.btn_color_rm, "R-"), (self.btn_color_gm, "G-"), (self.btn_color_bm, "B-"),
            ]:
                draw_button(self.surface, label, self.font_btn, btn,
                            hover=btn.collidepoint(mouse))

            draw_button(self.surface, "SAVE & BACK", self.font_btn, self.btn_save,
                        hover=self.btn_save.collidepoint(mouse))
            pygame.display.flip()


def main():
    pygame.init()
    surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    settings = load_settings()
    username = ""
    player_id = None
    personal_best = 0

    while True:
        menu = MainMenu(surface, clock, settings)
        action, username = menu.run()

        if DB_AVAILABLE and username:
            try:
                player_id = db.get_or_create_player(username)
                personal_best = db.get_personal_best(player_id)
            except Exception:
                player_id = None
                personal_best = 0

        if action == "leaderboard":
            LeaderboardScreen(surface, clock).run()
            continue

        if action == "settings":
            settings = SettingsScreen(surface, clock, settings).run()
            continue

        while True:
            game = Game(settings, player_id, personal_best)
            running = True
            while running:
                dt = clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        running = False
                    game.handle_event(event)

                game.update(dt)
                game.draw(surface)
                pygame.display.flip()

                if game.over:
                    if DB_AVAILABLE and player_id is not None:
                        try:
                            db.save_session(player_id, game.score, game.level)
                            personal_best = db.get_personal_best(player_id)
                            print(f"Saved: score={game.score} level={game.level}")
                        except Exception as e:
                            print(f"Save error: {e}")
                    else:
                        print(f"Not saved: DB_AVAILABLE={DB_AVAILABLE}, player_id={player_id}")
                    screen = GameOverScreen(surface, clock, game.score,
                                            game.level, personal_best)
                    result = screen.run()
                    if result == "retry":
                        break
                    else:
                        running = False
                        break

            if not game.over or result == "menu":
                break


if __name__ == "__main__":
    main()