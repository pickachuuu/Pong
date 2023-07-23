import pygame
from pygame.locals import *
from random import randint
from pygame import mixer
pygame.init()
mixer.init()


# PROPERTIES
SIZE = 800, 600
width, height = SIZE
pygame.display.set_caption("First game")
screen = pygame.display.set_mode(SIZE)
bg_color = 'black'
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)
pygame_icon = pygame.image.load('icon.png')
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption('Pong')
custom_font = pygame.font.SysFont('Public Pixel', 16)


# SOUNDFX_PROPERTIES
hit = pygame.mixer.Sound('paddle_hit.wav')
score_sound = pygame.mixer.Sound('score.wav')
end_music = pygame.mixer.Sound('game_over.wav')
mixer.music.load('bg_music.wav')
mixer.music.set_volume(0.2)
mixer.music.play(-1)

# TIMER_PROPERTIES
timer_duration = 3000
goal_scored = False

# PADDLE_PROPERTIES
p_height = 100
p_width = 10
p1_color = 'white'
paddle1_dy = 300
paddle1_dx = 0
paddle1_image = pygame.Surface((p_width, p_height))
paddle1_image.fill(p1_color)
p2_color = 'white'
paddle2_dy = 300
paddle2_dx = 790
paddle2_image = pygame.Surface((p_width, p_height))
paddle2_image.fill(p2_color)

# PLAYER_SCORE_PROPERTIES
font = pygame.font.Font(None, 36)
player1 = 0
player2 = 0
p1_game_point = 0
p2_game_point = 0
game_over = False
game_start = False

# GAME_BOARD_PROPERTIES
board_line_width = 5
board_line_height = 500
board_line_dx = width // 2
board_line_dy = 100
board_image = pygame.Surface((board_line_width, board_line_height))
board_image.fill("white")
board_horizontal_width = 800
board_horizontal_height = 5
board_horizontal_x = 0
board_horizontal_y = 100
board_horizontal_image = pygame.Surface((board_horizontal_width, board_horizontal_height))
board_horizontal_image.fill("white")

# PLAYER_INPUT_PROPERTIES
player1_up_pressed = False
player1_down_pressed = False
player2_up_pressed = False
player2_down_pressed = False

# BALL_PROPERTIES
ball_color = "white"
ball_x = 402
ball_y = 350
ball_rad = 10
ball_speed = 7
ball_dx = ball_speed
ball_dy = ball_speed
ball_buffer = 4

# Ball delay properties
ball_delay_duration = 2000  # 2000 milliseconds = 2 seconds
ball_delay_timer = pygame.time.get_ticks()
ball_delay_complete = False
first_time = True  # Flag to check if it's the first time the game is loaded

# GAME_OVER_PROPERTIES
game_over_timer = 0
reset_delay = 5000  # 5000 milliseconds = 5 seconds

def game_start():
    global game_start
    game_start = False

def game_point_check():
    global p1_game_point, p2_game_point, game_over
    if p1_game_point == 3 or p2_game_point == 3:
        game_over = True
        return game_over
    else:
        game_over = False
        return game_over

def collision_check(paddle_dx, paddle_dy, p_width, p_height, ball_x, ball_y, ball_rad):
    paddle_rect = pygame.Rect(paddle_dx, paddle_dy, p_width, p_height)
    ball_rect = pygame.Rect(ball_x - ball_rad, ball_y - ball_rad, ball_rad * 2, ball_rad * 2)
    return paddle_rect.colliderect(ball_rect)

def reset_board():
    global player1, player2, paddle1_dx, paddle1_dy, paddle2_dx, paddle2_dy, ball_x, ball_y, player1, player2
    paddle1_dx = 0
    paddle1_dy = 300
    paddle2_dx = 790
    paddle2_dy = 300
    ball_x = 402
    ball_y = 330
    player1 = 0
    player2 = 0
    pygame.time.wait(1000)

def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy, ball_speed, traj
    ball_x = 402
    ball_y = 350
    ball_speed = 7
    ball_dx = ball_speed
    ball_dy = ball_speed
    traj = randint (1, 2)


def ball_freeze():
    global ball_x, ball_y, ball_dx, ball_dy, ball_speed
    ball_x = 402
    ball_y = 350
    ball_speed = 0
    ball_dx = ball_speed
    ball_dy = ball_speed

# MAIN_LOOP
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_w:
                player1_up_pressed = True
            elif event.key == K_s:
                player1_down_pressed = True
            elif event.key == K_UP:
                player2_up_pressed = True
            elif event.key == K_DOWN:
                player2_down_pressed = True

        if event.type == KEYUP:
            if event.key == K_w:
                player1_up_pressed = False
            elif event.key == K_s:
                player1_down_pressed = False
            elif event.key == K_UP:
                player2_up_pressed = False
            elif event.key == K_DOWN:
                player2_down_pressed = False

    if player1_up_pressed:
        paddle1_dy -= 10
        if paddle1_dy < 100:
            player1_up_pressed = False
            paddle1_dy = 100
    if player1_down_pressed:
        paddle1_dy += 10
        if paddle1_dy >= height - 100:
            player1_down_pressed = False
            paddle1_dy = (height - 100)
    if player2_up_pressed:
        paddle2_dy -= 10
        if paddle2_dy < 100:
            player2_up_pressed = False
            paddle2_dy = 100
    if player2_down_pressed:
        paddle2_dy += 10
        if paddle2_dy >= height - 100:
            player2_down_pressed = False
            paddle2_dy = (height - 100)

    if first_time and not ball_delay_complete:
        current_time = pygame.time.get_ticks()
        traj = randint(1, 2)
        if current_time - ball_delay_timer >= ball_delay_duration:
            ball_delay_complete = True
            ball_dx = ball_speed
            ball_dy = ball_speed

    if ball_delay_complete:
        first_time = False

        if traj == 1:
            ball_x += ball_dx
            ball_y += ball_dy
        elif traj == 2:
            ball_x -= ball_dx
            ball_y -= ball_dy

        if ball_x + ball_rad >= width + 30:
            ball_dx = -ball_dx
            player1 += 1
            goal_scored = True
            ball_freeze()
            score_sound.play(maxtime=int(score_sound.get_length() * 1000))
            goal_time = pygame.time.get_ticks()
        if ball_x - ball_rad < -30:
            ball_dx = -ball_dx
            player2 += 1
            goal_scored = True
            ball_freeze()
            score_sound.play(maxtime=int(score_sound.get_length() * 1000))
            goal_time = pygame.time.get_ticks()

        if goal_scored:
            time_since_goal = pygame.time.get_ticks() - goal_time
            if time_since_goal >= timer_duration:
                goal_scored = False
                reset_ball()

        if player1 == 5:
            p1_game_point += 1
            reset_board()
        if player2 == 5:
            p2_game_point += 1
            reset_board()

        if ball_y - ball_rad < 100 or ball_y + ball_rad > height:
            ball_dy = -ball_dy
        if collision_check(paddle1_dx, paddle1_dy, p_width, p_height, ball_x, ball_y, ball_rad):
            ball_dx = -ball_dx
            hit.play(maxtime=int(hit.get_length() * 1000))
        if collision_check(paddle2_dx, paddle2_dy, p_width, p_height, ball_x, ball_y, ball_rad):
            ball_dx = -ball_dx
            hit.play(maxtime=int(hit.get_length() * 1000))

    game_point_check()
    score_display_1 = custom_font.render(f"Score: {player1}", True, "white")
    score_display_2 = custom_font.render(f"Score: {player2}", True, "white")
    game_point_display_1 = custom_font.render(f"Streak: {p1_game_point}", True, "white")
    game_point_display_2 = custom_font.render(f"Streak: {p2_game_point}", True, "white")
    game_over_display = custom_font.render(f"GAME OVER", True, "white")
    p1_wins = custom_font.render(f"Player 1 wins", True, "white")
    p2_wins = custom_font.render(f"Player 2 wins", True, "white")
    screen.fill(bg_color)

    if game_over == False:
        screen.fill(bg_color)
        screen.blit(score_display_1, (20, 20))
        screen.blit(score_display_2, (630, 20))
        screen.blit(game_point_display_1, (20, 45))
        screen.blit(game_point_display_2, (630, 45))
        screen.blit(board_horizontal_image, (board_horizontal_x, board_horizontal_y))
        screen.blit(board_image, (board_line_dx, board_line_dy))
        screen.blit(paddle1_image, (paddle1_dx, paddle1_dy))
        screen.blit(paddle2_image, (paddle2_dx, paddle2_dy))
        pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_rad)

    if game_over == True:
        pygame.mixer.music.stop()
        end_music.play(maxtime=int(end_music.get_length() * 1000))
        ball_freeze()
        screen.blit(game_over_display, (330, 280))
        if p1_game_point == 3:
            screen.blit(p1_wins, (300, 330))
        elif p2_game_point == 3:
            screen.blit(p2_wins, (300, 330))

    if game_over_timer == 0 and game_over:
        game_over_timer = pygame.time.get_ticks()

    # Check if enough time has passed to reset the game
    if game_over_timer != 0 and pygame.time.get_ticks() - game_over_timer >= reset_delay:
        # Reset the game
        p1_game_point = 0
        p2_game_point = 0
        reset_board()
        reset_ball()
        game_over = False
        game_over_timer = 0

    pygame.display.update()
    clock.tick(60)
pygame.quit()