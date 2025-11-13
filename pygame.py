import pygame  # YANG INI DIUBAH
import random

# --- KONFIGURASI AWAL ---
pygame.init()  # YANG INI DIUBAH

# Konstanta Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)

# Konstanta Ukuran Layar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Setup Layar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # YANG INI DIUBAH
pygame.display.set_caption("Game Pong Klasik")  # YANG INI DIUBAH

# Setup Clock untuk mengontrol FPS
clock = pygame.time.Clock()  # YANG INI DIUBAH

# --- OBJEK-OBJEK GAME ---


# Paddle (Pemukul)
class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 15
        self.height = 100
        self.vel = 5  # Kecepatan paddle
        self.rect = pygame.Rect(
            self.x, self.y, self.width, self.height
        )  # YANG INI DIUBAH

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)  # YANG INI DIUBAH

    def move_up(self):
        if self.rect.top > 0:
            self.rect.y -= self.vel

    def move_down(self):
        if self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.vel


# Ball (Bola)
class Ball:
    def __init__(self):
        self.radius = 10
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.vel_x = random.choice([-4, 4])  # Kecepatan awal random kiri/kanan
        self.vel_y = random.choice([-4, 4])  # Kecepatan awal random atas/bawah
        self.rect = pygame.Rect(  # YANG INI DIUBAH
            self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2
        )

    def draw(self):
        pygame.draw.circle(  # YANG INI DIUBAH
            screen, CYAN, (self.rect.centerx, self.rect.centery), self.radius
        )

    def move(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Pantul dari atas dan bawah layar
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.vel_y *= -1

    def reset(self):
        """Mengembalikan bola ke tengah dengan arah random."""
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.vel_x = random.choice([-4, 4])
        self.vel_y = random.choice([-4, 4])


# --- FUNGSI UTAMA GAME ---
def main():
    run = True
    fps = 60

    # Membuat objek paddle dan bola
    player1 = Paddle(30, SCREEN_HEIGHT // 2 - 50)  # Pemain kiri
    player2 = Paddle(SCREEN_WIDTH - 45, SCREEN_HEIGHT // 2 - 50)  # Pemain kanan
    ball = Ball()

    # Skor
    player1_score = 0
    player2_score = 0
    font = pygame.font.SysFont("comicsansms", 50)  # YANG INI DIUBAH

    while run:
        clock.tick(fps)

        # --- EVENT HANDLING (INPUT PEMAIN) ---
        for event in pygame.event.get():  # YANG INI DIUBAH
            if event.type == pygame.QUIT:  # YANG INI DIUBAH
                run = False

        # Gerakan Pemain 1 (kiri) dengan tombol W dan S
        keys = pygame.key.get_pressed()  # YANG INI DIUBAH
        if keys[pygame.K_w]:  # YANG INI DIUBAH
            player1.move_up()
        if keys[pygame.K_s]:  # YANG INI DIUBAH
            player1.move_down()

        # Gerakan Pemain 2 (kanan) dengan tombol Panah Atas dan Bawah
        if keys[pygame.K_UP]:  # YANG INI DIUBAH
            player2.move_up()
        if keys[pygame.K_DOWN]:  # YANG INI DIUBAH
            player2.move_down()

        # --- LOGIKA PERMAINAN ---
        ball.move()

        # Cek tabrakan bola dengan paddle
        if ball.rect.colliderect(player1.rect) or ball.rect.colliderect(player2.rect):
            ball.vel_x *= -1  # Balik arah horizontal

        # Cek jika bola keluar dari kiri/kanan layar (gol)
        if ball.rect.left <= 0:
            player2_score += 1
            ball.reset()
        if ball.rect.right >= SCREEN_WIDTH:
            player1_score += 1
            ball.reset()

        # --- GAMBAR SEMUA OBJEK KE LAYAR ---
        screen.fill(BLACK)

        # Gambar garis tengah
        pygame.draw.rect(
            screen, WHITE, (SCREEN_WIDTH // 2 - 2, 0, 4, SCREEN_HEIGHT)
        )  # YANG INI DIUBAH

        # Gambar objek
        player1.draw()
        player2.draw()
        ball.draw()

        # Gambar skor
        score_text = font.render(f"{player1_score} : {player2_score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 30))

        # Update tampilan
        pygame.display.update()  # YANG INI DIUBAH

    pygame.quit()  # YANG INI DIUBAH


# --- MENJALANKAN GAME ---
if __name__ == "__main__":
    main()
