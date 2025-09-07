import os
import pygame, sys, random

def ball_movement():
    """
    Handles the movement of the ball and collision detection with the player and screen boundaries.
    """
    global ball_speed_x, ball_speed_y, score, start, ball_color, highscore

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Start the ball movement when the game begins
    # TODO Task 5 Create a Merge Conflict
    speed = 8
    if start:
        ball_speed_x = speed * random.choice((1, -1))  # Randomize initial horizontal direction
        ball_speed_y = speed * random.choice((1, -1))  # Randomize initial vertical direction
        start = False

    # Ball collision with the player paddle
    if ball.colliderect(player):
        if abs(ball.bottom - player.top) < 10:  # Check if ball hits the top of the paddle
            score += 1  # Increase player score
            if score > highscore:  # <-- aquí se actualiza el récord
                highscore = score
                save_highscore(highscore)
            ball_speed_y *= -1  # Reverse ball's vertical direction
            ball_color = rand_color()

            # TODO Task 6: Add sound effects HERE
            pygame.mixer.init()
            hit_sound = pygame.mixer.Sound("ping.wav")
            hit_sound.play()


    # Ball collision with top boundary
    if ball.top <= 0:
        ball_speed_y *= -1  # Reverse ball's vertical direction
        ball_color = rand_color()

    # Ball collision with left and right boundaries
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1
        ball_color = rand_color()

    # Ball goes below the bottom boundary (missed by player)
    if ball.bottom > screen_height:
        # Handle ball loss: reduce lives, reset ball, and restart game
        global high_score, lives
        lives -= 1
        ball.center = (screen_width / 2, screen_height / 2) #Reset the ball to the center of the screen and stop its movement
        ball_speed_x, ball_speed_y = 0, 0
        start = False

        if lives <= 0:
            # Ensure highscore saved
            if score > highscore:
                highscore = score
                save_highscore(highscore)
            restart()
            lives = 3

def player_movement():
    """
    Handles the movement of the player paddle, keeping it within the screen boundaries.
    """
    player.x += player_speed  # Move the player paddle horizontally

    # Prevent the paddle from moving out of the screen boundaries
    if player.left <= 0:
        player.left = 0
    if player.right >= screen_width:
        player.right = screen_width

def restart():
    """
    Resets the ball and player scores to the initial state.
    """
    global ball_speed_x, ball_speed_y, score
    ball.center = (screen_width / 2, screen_height / 2)  # Reset ball position to center
    ball_speed_y, ball_speed_x = 0, 0  # Stop ball movement
    score = 0  # Reset player score

# General setup
pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()
clock = pygame.time.Clock()

pygame.mixer.music.load("music.wav")
pygame.mixer.music.play(-1)

# Main Window setup
screen_width = 500  # Screen width (can be adjusted)
screen_height = 500  # Screen height (can be adjusted)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')  # Set window title

# Colors
bg_color = pygame.Color('grey12')

# Game Rectangles (ball and player paddle)
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)  # Ball (centered)
# TODO Task 1 Make the paddle bigger
player_height = 15
player_width = 200
player = pygame.Rect(screen_width/2 - 45, screen_height - 20, player_width, player_height)  # Player paddle

# Game Variables
ball_speed_x = 0
ball_speed_y = 0
player_speed = 0

# Ball color setup
ball_color = (255, 255, 255)  # bola empieza blanca

def rand_color():
    return (
        random.randint(50, 255),
        random.randint(50, 255),
        random.randint(50, 255)
    )
# Score Text setup
score = 0
high_score = 0 #add new scores
lives = 3 #add lives to game
# High Score setup
HIGHSCORE_FILE = "highscore.txt"

def load_highscore():
    if not os.path.exists(HIGHSCORE_FILE):
        return 0
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read().strip() or 0)
    except:
        return 0

def save_highscore(value):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(value))

highscore = load_highscore()

basic_font = pygame.font.Font('freesansbold.ttf', 24)  # Font for displaying score

#Load the heart image and scale it to 25x25 pixels
heart_img = pygame.image.load("Red heart illustration.png.jpeg.png")
heart_img = pygame.transform.scale(heart_img, (25, 25))

start = False  # Indicates if the game has started

# Main game loop
while True:
    # Event handling
    # TODO Task 4: Add your name
    name = "Paulo Rentas and Mia Muñoz"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit the game
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_speed -= 6  # Move paddle left
            if event.key == pygame.K_RIGHT:
                player_speed += 6  # Move paddle right
            if event.key == pygame.K_SPACE:
                start = True  # Start the ball movement
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_speed += 6  # Stop moving left
            if event.key == pygame.K_RIGHT:
                player_speed -= 6  # Stop moving right

    # Game Logic
    ball_movement()
    player_movement()

    # Visuals
    white = pygame.Color('white')
    red = pygame.Color('red')
    screen.fill(bg_color)  # Clear screen with background color
    pygame.draw.rect(screen, white, player)  # Draw player paddle
    # TODO Task 3: Change the Ball Color
    pygame.draw.ellipse(screen, ball_color, ball)  # Draw ball
    player_text = basic_font.render(f'{score}', False, white )  # Render player score
    screen.blit(player_text, (screen_width/2 - 15, 10))  # Display score on screen

    hs_text = basic_font.render(f'HIGHSCORE: {highscore}', False, white) # add player HS
    screen.blit(hs_text, (screen_width - 200, 10)) #Display the HS

    # Draw the heart icons on the screen based on the number of lives left
    if lives >= 1:
        screen.blit(heart_img, (10, 10))
    if lives >= 2:
        screen.blit(heart_img, (40, 10))
    if lives >= 3:
        screen.blit(heart_img, (70, 10))

    # Update display
    pygame.display.flip()
    clock.tick(60)  # Maintain 60 frames per second