import pygame
import random
import sys
 

 
pygame.init()
 
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pong")
 
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
GRAY   = (50, 50, 50)
 
clock = pygame.time.Clock()
FPS = 60
 
font_big   = pygame.font.SysFont("monospace", 64, bold=True)
font_small = pygame.font.SysFont("monospace", 22)
 
PADDLE_W = 12
PADDLE_H = 80
PADDLE_SPEED = 6
 
BALL_SIZE = 12
BALL_START_SPEED = 5
 
WIN_SCORE = 7
 
 
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_W, PADDLE_H)
        self.speed = PADDLE_SPEED
 
    def move_up(self):
        if self.rect.top > 0:
            self.rect.y -= self.speed
 
    def move_down(self):
        if self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
 
    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect, border_radius=4)
 
 
class Ball:
    def __init__(self):
        self.reset()
 
    def reset(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2,
                                HEIGHT // 2 - BALL_SIZE // 2,
                                BALL_SIZE, BALL_SIZE)
        self.dx = BALL_START_SPEED * random.choice([-1, 1])
        self.dy = BALL_START_SPEED * random.choice([-1, 1])
 
    def update(self, p1, p2):
        self.rect.x += self.dx
        self.rect.y += self.dy
 
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.dy *= -1
 
        if self.rect.colliderect(p1.rect) and self.dx < 0:
            self.dx *= -1
            self.dy += random.uniform(-1, 1)   # tiny angle variation each hit
        if self.rect.colliderect(p2.rect) and self.dx > 0:
            self.dx *= -1
            self.dy += random.uniform(-1, 1)
 
        self.dy = max(-10, min(10, self.dy))
 
        if self.rect.left <= 0:
            return "p2"   
        if self.rect.right >= WIDTH:
            return "p1"   
 
        return None
 
    def draw(self):
        pygame.draw.ellipse(screen, WHITE, self.rect)
 
 
def draw_divider():
    
    dash_height = 15
    gap = 10
    x = WIDTH // 2 - 1
    y = 0
    while y < HEIGHT:
        pygame.draw.rect(screen, GRAY, (x, y, 2, dash_height))
        y += dash_height + gap
 
 
def draw_scores(s1, s2):
    t1 = font_big.render(str(s1), True, WHITE)
    t2 = font_big.render(str(s2), True, WHITE)
    screen.blit(t1, (WIDTH // 4 - t1.get_width() // 2, 20))
    screen.blit(t2, (3 * WIDTH // 4 - t2.get_width() // 2, 20))
 
 
def show_message(line1, line2=None):
    screen.fill(BLACK)
    t1 = font_big.render(line1, True, WHITE)
    screen.blit(t1, (WIDTH // 2 - t1.get_width() // 2, HEIGHT // 2 - 60))
    if line2:
        t2 = font_small.render(line2, True, GRAY)
        screen.blit(t2, (WIDTH // 2 - t2.get_width() // 2, HEIGHT // 2 + 20))
    pygame.display.flip()
 
 
def wait_for_keypress():
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                return
 
 
def main():
    p1 = Paddle(30, HEIGHT // 2 - PADDLE_H // 2)
    p2 = Paddle(WIDTH - 30 - PADDLE_W, HEIGHT // 2 - PADDLE_H // 2)
    ball = Ball()
 
    score1 = 0
    score2 = 0
 
    
    show_message("PONG", "press any key to start")
    wait_for_keypress()
 
    while True:
        clock.tick(FPS)
 
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
 
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            p1.move_up()
        if keys[pygame.K_s]:
            p1.move_down()
        if keys[pygame.K_UP]:
            p2.move_up()
        if keys[pygame.K_DOWN]:
            p2.move_down()
 
        # update ball
        result = ball.update(p1, p2)
 
        if result == "p1":
            score1 += 1
            ball.reset()
        elif result == "p2":
            score2 += 1
            ball.reset()
 
        
        if score1 >= WIN_SCORE:
            show_message("player 1 wins!", "press any key to play again")
            wait_for_keypress()
            score1, score2 = 0, 0
            ball.reset()
        elif score2 >= WIN_SCORE:
            show_message("player 2 wins!", "press any key to play again")
            wait_for_keypress()
            score1, score2 = 0, 0
            ball.reset()
 
        
        screen.fill(BLACK)
        draw_divider()
        draw_scores(score1, score2)
        p1.draw()
        p2.draw()
        ball.draw()
 
        hint = font_small.render("p1: W/S     p2: UP/DOWN     ESC: quit", True, GRAY)
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 30))
 
        pygame.display.flip()
 
 
# kick things off
main()
