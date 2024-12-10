import pygame
import sys



# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Casse-Briques")

# Couleurs par défaut
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Couleurs configurables
paddle_color = BLUE
ball_color = GREEN
brick_color = RED

# Raquette
paddle_width, paddle_height = 100, 10
paddle_x = (WIDTH - paddle_width) // 2
paddle_y = HEIGHT - 30
paddle_speed = 10

# Balle
ball_radius = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = 5
ball_speed_y = 5

# Briques
brick_width, brick_height = 70, 30
brick_rows, brick_cols = 5, 10
brick_gap = 5
bricks = []

for row in range(brick_rows):
    for col in range(brick_cols):
        brick_x = col * (brick_width + brick_gap) + brick_gap
        brick_y = row * (brick_height + brick_gap) + brick_gap
        bricks.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))

# Vies
lives = 3

# Fonction pour dessiner les briques
def draw_bricks():
    for brick in bricks:
        pygame.draw.rect(screen, brick_color, brick)

# Fonction pour dessiner la raquette
def draw_paddle():
    pygame.draw.rect(screen, paddle_color, (paddle_x, paddle_y, paddle_width, paddle_height))

# Fonction pour dessiner la balle
def draw_ball():
    pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)

# Fonction pour dessiner les vies
def draw_lives():
    font = pygame.font.Font(None, 36)
    text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(text, (10, 10))

# Fonction pour dessiner le menu principal
def draw_menu():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render("Casse-Briques", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4))

    font = pygame.font.Font(None, 36)
    text1 = font.render("1. Play", True, WHITE)
    text2 = font.render("2. Change Colors", True, WHITE)
    text3 = font.render("3. Quit", True, WHITE)
    screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 2))
    screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2 + 50))
    screen.blit(text3, (WIDTH // 2 - text3.get_width() // 2, HEIGHT // 2 + 100))
    pygame.display.flip()

# Fonction pour changer les couleurs
def change_colors():
    global paddle_color, ball_color, brick_color
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    text = font.render("Choose a color scheme:", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4))

    text1 = font.render("1. Default", True, WHITE)
    text2 = font.render("2. Blue Theme", True, WHITE)
    text3 = font.render("3. Green Theme", True, WHITE)
    screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 2))
    screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2 + 50))
    screen.blit(text3, (WIDTH // 2 - text3.get_width() // 2, HEIGHT // 2 + 100))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    paddle_color = BLUE
                    ball_color = GREEN
                    brick_color = RED
                    waiting = False
                elif event.key == pygame.K_2:
                    paddle_color = (0, 0, 255)
                    ball_color = (0, 0, 255)
                    brick_color = (0, 0, 255)
                    waiting = False
                elif event.key == pygame.K_3:
                    paddle_color = (0, 255, 0)
                    ball_color = (0, 255, 0)
                    brick_color = (0, 255, 0)
                    waiting = False

# Boucle principale du jeu
def game_loop():
    global paddle_x, ball_x, ball_y, ball_speed_x, ball_speed_y, lives, bricks
    lives = 3  # Réinitialiser les vies
    bricks = []
    for row in range(brick_rows):
        for col in range(brick_cols):
            brick_x = col * (brick_width + brick_gap) + brick_gap
            brick_y = row * (brick_height + brick_gap) + brick_gap
            bricks.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Mouvement de la raquette avec la souris
        mouse_x, _ = pygame.mouse.get_pos()
        paddle_x = mouse_x - paddle_width // 2
        if paddle_x < 0:
            paddle_x = 0
        elif paddle_x > WIDTH - paddle_width:
            paddle_x = WIDTH - paddle_width

        # Mouvement de la balle
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Rebond sur les bords
        if ball_x <= ball_radius or ball_x >= WIDTH - ball_radius:
            ball_speed_x = -ball_speed_x
        if ball_y <= ball_radius:
            ball_speed_y = -ball_speed_y

        # Rebond sur la raquette
        if (paddle_y - ball_radius <= ball_y <= paddle_y + paddle_height + ball_radius and
            paddle_x <= ball_x <= paddle_x + paddle_width):
            ball_speed_y = -ball_speed_y

        # Rebond sur les briques
        for brick in bricks[:]:
            if brick.colliderect(pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)):
                ball_speed_y = -ball_speed_y
                bricks.remove(brick)

        # Dessin
        screen.fill(BLACK)
        draw_bricks()
        draw_paddle()
        draw_ball()
        draw_lives()
        pygame.display.flip()

        # Vérification de la fin du jeu
        if ball_y >= HEIGHT:
            lives -= 1
            if lives <= 0:
                running = False
            else:
                ball_x, ball_y = WIDTH // 2, HEIGHT // 2
                ball_speed_x, ball_speed_y = 5, 5
                paddle_x = (WIDTH - paddle_width) // 2

        # Limitation de la vitesse de la boucle
        pygame.time.Clock().tick(60)

# Boucle du menu principal
def main_menu():
    while True:
        draw_menu()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        game_loop()
                        waiting = False
                    elif event.key == pygame.K_2:
                        change_colors()
                        waiting = False
                    elif event.key == pygame.K_3:
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    main_menu()
