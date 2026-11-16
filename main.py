"""종스크롤 슈팅 게임. 실행: python main.py"""
import sys

import pygame

from settings import (
    WIDTH, HEIGHT, FPS, TITLE, HIGHSCORE_FILE,
    ENEMY_SPAWN_MS, START_LIVES, SCORE_PER_ENEMY,
    WHITE, YELLOW, RED, HUD_SHADE, GAME_OVER_SHADE,
)
from entities import Background, Player, Enemy

SPAWN_ENEMY = pygame.USEREVENT + 1


def load_high_score():
    """HIGHSCORE_FILE 에서 최고 점수를 읽어 돌려준다."""
    # TODO(F5): 최고 점수 파일 읽기
    return 0


def save_high_score(score):
    """최고 점수를 HIGHSCORE_FILE 에 저장한다."""
    # TODO(F5): 최고 점수 파일 저장
    pass


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.big_font = pygame.font.Font(None, 72)
        pygame.time.set_timer(SPAWN_ENEMY, ENEMY_SPAWN_MS)
        self.background = Background()
        self.hud_shade = pygame.Surface((WIDTH, 44), pygame.SRCALPHA)
        self.hud_shade.fill(HUD_SHADE)
        self.dark_shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.dark_shade.fill(GAME_OVER_SHADE)
        self.high_score = load_high_score()
        self.running = True
        self.on_title = True
        self.reset()

    def reset(self):
        """새 판을 시작하고 스프라이트·점수·생명을 초기화한다."""
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        self.score = 0
        self.lives = START_LIVES
        self.game_over = False

    # ---------------- 입력 ----------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.on_title:
                self.handle_title_event(event)
            elif event.type == SPAWN_ENEMY and not self.game_over:
                enemy = Enemy()
                self.enemies.add(enemy)
                self.all_sprites.add(enemy)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE and not self.game_over:
                    bullet = self.player.shoot()
                    self.bullets.add(bullet)
                    self.all_sprites.add(bullet)
                # TODO(F5): 게임 오버 상태에서 R 키로 재시작

    def handle_title_event(self, event):
        """시작 화면에서는 SPACE로 시작하고 ESC로 종료한다."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.on_title = False
                self.reset()
            elif event.key == pygame.K_ESCAPE:
                self.running = False

    # ---------------- 갱신 ----------------
    def update(self):
        if self.game_over:
            return

        self.background.update()
        if self.on_title:
            return

        self.player.update(pygame.key.get_pressed())
        self.bullets.update()
        self.enemies.update()

        # 총알과 적이 충돌하면 둘 다 제거하고, 제거된 적 수만큼 점수를 올린다.
        hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        hit_enemy_count = sum(len(hit_enemies) for hit_enemies in hits.values())
        self.score += hit_enemy_count * SCORE_PER_ENEMY

        # TODO(F4): 플레이어 충돌, 화면 이탈 및 생명 처리

        for enemy in list(self.enemies):
            if enemy.rect.top > HEIGHT:
                enemy.kill()
                # TODO(F4): 화면 아래로 지나간 적만큼 생명 감소

        # TODO(F4): 생명이 0 이하이면 게임 오버

    def end_game(self):
        """게임 오버 처리."""
        self.game_over = True
        # TODO(F5): 최고 점수 갱신 및 저장

    # ---------------- 그리기 ----------------
    def draw_text(self, text, font, color, **position):
        surface = font.render(text, True, color)
        self.screen.blit(surface, surface.get_rect(**position))

    def draw(self):
        self.background.draw(self.screen)
        if self.on_title:
            self.draw_title()
            pygame.display.flip()
            return

        self.all_sprites.draw(self.screen)
        if self.game_over:
            self.screen.blit(self.dark_shade, (0, 0))
        self.screen.blit(self.hud_shade, (0, 0))
        self.draw_text(f"SCORE: {self.score}", self.font, WHITE, topleft=(10, 10))
        self.draw_text(f"LIVES: {self.lives}", self.font, WHITE, topright=(WIDTH - 10, 10))
        if self.game_over:
            self.draw_game_over()
        pygame.display.flip()

    def draw_title(self):
        cx = WIDTH // 2
        self.screen.blit(self.dark_shade, (0, 0))
        self.draw_text(TITLE, self.big_font, YELLOW, center=(cx, 150))
        self.screen.blit(self.player.image, self.player.image.get_rect(center=(cx, 270)))
        controls = ("LEFT / RIGHT : Move", "SPACE : Shoot", "R : Restart", "ESC : Quit")
        for i, line in enumerate(controls):
            self.draw_text(line, self.font, WHITE, center=(cx, 370 + i * 34))
        if pygame.time.get_ticks() // 500 % 2 == 0:
            self.draw_text("Press SPACE to start", self.font, YELLOW, center=(cx, 540))

    def draw_game_over(self):
        # TODO(F4): GAME OVER 와 이번 판 점수 표시
        # TODO(F5): 최고 점수와 재시작 안내 표시
        pass

    # ---------------- 게임 루프 ----------------
    def step(self):
        self.handle_events()
        self.update()
        self.draw()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.step()
        pygame.quit()


if __name__ == "__main__":
    Game().run()
    sys.exit()
