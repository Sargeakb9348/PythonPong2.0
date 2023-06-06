import pygame
import random
import math
pygame.init()
pygame.display.set_caption("Python Pong")

WIDTH, HEIGHT = 700, 501  # height and width of display window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))


FPS = 60
WHITE = (255, 255, 255)
BLUE = (1, 9, 56)
RED = (255, 0, 0)
YELLOW = (235, 183, 52)
GREEN = (0, 255, 4)
PINK = (250, 5, 221)


PADDLE_WIDTH, PADDLE_HEIGHT = 20, 101
BALL_RADIUS = 7
POWERUP_RADIUS = 18


SCORE_FONT = pygame.font.SysFont("comicsans", 25)

WINNING_SCORE = 10


class Paddle:
    # Class attributes
    COLOR = WHITE
    VELOCITY = 4  # distance/frame

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y,
                         self.width, self.height))  # draw paddle

    def move(self, up=True):  # true is up false is down
        if(up):
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


class Ball:
    MAX_VEL = -5
    color = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        # move ball in x direction on program start (randomized which direction)
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.x_vel = -1 * self.MAX_VEL
        self.y_vel = 0
        self.color = WHITE


class Powerup:

    def __init__(self, active):

        # Randomize position and color of powerup
        xrand = random.randint(60, WIDTH-60)
        yrand = random.randint(20, HEIGHT-20)
        colorrand = random.randint(0, 3)
        if(colorrand == 0):
            pcolor = RED
        elif(colorrand == 1):
            pcolor = YELLOW
        elif(colorrand == 2):
            pcolor = GREEN
        elif(colorrand == 3):
            pcolor = PINK

        self.x = xrand
        self.y = yrand
        self.color = pcolor
        self.active = active

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), POWERUP_RADIUS)

    def reset(self):
        # Randomize position and color of powerup
        xrand = random.randint(40, WIDTH-40)
        yrand = random.randint(20, HEIGHT-20)
        colorrand = random.randint(0, 3)
        if(colorrand == 0):
            pcolor = RED
        elif(colorrand == 1):
            pcolor = YELLOW
        elif(colorrand == 2):
            pcolor = GREEN
        elif(colorrand == 3):
            pcolor = PINK

        self.x = xrand
        self.y = yrand
        self.color = pcolor
        self.active = True


def draw(win, paddles, ball, left_score, right_score, powerup):
    win.fill(BLUE)  # fill with blue

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)

    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH*(3/4) -
             right_score_text.get_width()//2, 20))
    for paddle in paddles:
        paddle.draw(win)  # draw each paddle in the list of paddles

    for i in range(10, HEIGHT, HEIGHT//20):  # draw dotted line
        if i % 2 == 1:
            continue

        # 20 rectangles 10 drawn rectangles with width = 2px
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 1, i, 2, HEIGHT//20))

    ball.draw(win)

    if (powerup.active != False):
        powerup.draw(win)

    pygame.display.update()  # display draw updates


def handle_collision(ball, left_paddle, right_paddle, powerup):
    if ball.y + ball.radius >= HEIGHT:  # if it hits the ceiling
        ball.y_vel *= -1
    elif ball.y-ball.radius <= 0:  # if it hits the ceiling
        ball.y_vel *= -1

    # CHANGE X and Y velocity
    if ball.x_vel < 0:  # hitting the left paddle
        # if the ball is within the y range of the height of the paddle
        if ball.y >= left_paddle.y and ball.y < left_paddle.y + left_paddle.height:
            # if the ball hits the right edge of the paddle
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                # Y velocity equation: half of height/ reduction factor = max velocity => half of height/max velocity =reduction
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = ball.y-middle_y
                reduction_factor = (left_paddle.height/2)/ball.MAX_VEL
                # squeez the velocity in range of -5 and 5
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = y_vel*-1

    else:  # hitting the right paddle
        # if the ball is within the y range of the height of the paddle
        if ball.y >= right_paddle.y and ball.y < right_paddle.y + right_paddle.height:
            if ball.x+ball.radius >= right_paddle.x:  # if the ball hits the left edge of the paddle
                ball.x_vel *= -1

                # Y velocity equation: half of height/ reduction factor = max velocity => half of height/max velocity =reduction
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = ball.y-middle_y
                reduction_factor = (right_paddle.height/2)/ball.MAX_VEL
                # squeez the velocity in range of -5 and 5
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = y_vel*-1

    # collision with powerup
    if powerup.active == True:

        if((BALL_RADIUS+POWERUP_RADIUS) >= math.sqrt(((ball.x - powerup.x)**2)+((ball.y - powerup.y)**2))):
            # if ball.y >= powerup.y-POWERUP_RADIUS and ball.y < powerup.y + POWERUP_RADIUS:
            # if ball.x >= powerup.x-POWERUP_RADIUS and ball.x < powerup.x + POWERUP_RADIUS:
            if powerup.color == RED:  # RED POWERUP
                ball.x_vel = ball.x_vel*1.5
                ball.color = RED
                powerup.active = False
            elif powerup.color == YELLOW:  # YELLOW POWERUP
                ball.color = YELLOW
                powerup.active = False
            elif powerup.color == PINK:  # PINK POWERUP
                ball.color = PINK
                powerup.active = False
            else:  # GREEN POWERUP
                ball.color = GREEN
                powerup.active = False


def handle_paddle_movement(keys, left_paddle, right_paddle):

    if keys[pygame.K_w] and left_paddle.y - left_paddle.VELOCITY >= 0:
        left_paddle.move(up=True)  # move left paddle up
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VELOCITY + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)  # move left paddle down

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VELOCITY >= 0:
        right_paddle.move(up=True)  # move left paddle up
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VELOCITY + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)  # move left paddle down


def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT//2-PADDLE_HEIGHT //
                         2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT //
                          2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)

    powerup = Powerup(True)

    left_score = 0
    right_score = 0

    while run:
        clock.tick(FPS)  # 60 fps cap (regulates speed of while loop)
        draw(WIN, [left_paddle, right_paddle], ball, left_score,
             right_score, powerup)  # constantly draw screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()  # returns a list of keys pressed
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle, powerup)

        if ball.x < 0:
            if ball.color == YELLOW:
                right_score += 2
            else:
                right_score += 1

            powerup.reset()
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
        elif ball.x > WIDTH:
            if ball.color == YELLOW:
                left_score += 2
            else:
                left_score += 1
            powerup.reset()
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()

        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left player won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right player won!"

        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width() //
                     2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            powerup.reset()
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()


if __name__ == '__main__':
    main()
