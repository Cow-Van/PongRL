# Imports all necessary libraries
import sys
import pygame
import random
from eval import Eval
from env import Env

# initializes pygame, must run this before everything else
# the clock keeps track of the time, and limits the framerate
pygame.init()
clock = pygame.time.Clock()

# Sets up the display
# original width 1280, original height 960
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong Game")

basic_font = pygame.font.Font("Pixeltype.ttf", 32)

# starts the game loop, its an infinite loop
class Pong:
    def __init__(self, clock=False) -> None:
        self.ball_speed_x = 7 * random.choice((-1, 1))
        self.ball_speed_y = 7 * random.choice((-1, 1))
        self.game_active = True
        self.player_score = 0
        self.opponent_score = 0
        self.player_speed = 0
        self.opponent_speed = 7
        self.ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
        self.player = pygame.Rect(10, screen_height / 2 - 70, 10, 140)
        self.opponent = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
        self.bg_color = pygame.Color("grey12")
        self.light_grey = (200, 200, 200)
        self.game_end = False
        self.clock = clock

        # Get the game environment
        self.env = Env()

        # Evaluate how well the "player"/AI is doing per round
        self.eval = Eval()

    def tick(self, input=None):
        if input == None:
            # checks for any event that happens
            for event in pygame.event.get():
                # if the event quits the game, then it force quits the application
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # if the event is a key press, then it checks what key was pressed
                if event.type == pygame.KEYDOWN:
                    # if the key pressed was the w key, then the player speed goes up
                    if event.key == pygame.K_w:
                        self.player_speed -= 7
                    # if the key pressed was the s key, then player speed goes down
                    if event.key == pygame.K_s:
                        self.player_speed += 7

                # if the event is a key release, then it checks what key was released
                if event.type == pygame.KEYUP:
                    # if the key released was the w key, then the player speed goes down
                    if event.key == pygame.K_w:
                        self.player_speed += 7
                    # if the key released was the s key, then player speed goes up
                    if event.key == pygame.K_s:
                        self.player_speed -= 7
        elif input == 0:
            pass # 0 = do nothing
        elif input == 1:
            self.player_speed = -7 # Up
        elif input == 2:
            self.player_speed = 7 # Down

        if self.game_active == True:
            # updates all game object's position
            self.player_animation()
            self.ball_animation()
            self.opponent_animation()

            # color the screen
            screen.fill(self.bg_color)

            # draws all game objects to the screen
            if self.clock:
                pygame.draw.rect(screen, self.light_grey, self.player)
                pygame.draw.rect(screen, self.light_grey, self.opponent)
                pygame.draw.ellipse(screen, self.light_grey, self.ball)
                pygame.draw.aaline(
                    screen, self.light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height)
                )

                # draws the scores to the screen
                player_text = basic_font.render("Player Score : " + str(self.player_score), True, self.light_grey)
                screen.blit(player_text, (900, 100))

                opponent_text = basic_font.render("Opponent Score: " + str(self.opponent_score), True, self.light_grey)
                screen.blit(opponent_text, (250, 100))

        if self.clock:
            pygame.display.flip()
            clock.tick(75)
        
        self.env.update(self.ball.x, self.ball.y, self.ball_speed_x, self.ball_speed_y, self.player.centery, self.opponent.centery)
        self.eval.tick()
        return self.eval.get_eval(), self.env.get_all(), self.game_end

    def ball_animation(self):
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y

        # checks if the ball collides with the top or bottom of screen, then changes its y direction
        if self.ball.top <= 0 or self.ball.bottom >= screen_height:
            self.ball_speed_y *= -1

        # checks if ball reached the left side of the screen
        if self.ball.left <= 0:
            self.game_end = True
            self.eval.lose()
            self.ball_restart()
            self.opponent_score += 1
            self.player.centery = screen_height / 2
            self.opponent.centery = screen_height / 2

        # checks if ball reached right side of screen
        if self.ball.right >= screen_width:
            self.eval.win()
            self.ball_restart()
            self.player_score += 1
            self.player.centery = screen_height / 2
            self.opponent.centery = screen_height / 2

        # checks if the ball collides with the player or the opponent, then changes the balls direction
        if self.ball.colliderect(self.player):
            self.eval.bounce()
            self.ball_speed_x *= -1

        if self.ball.colliderect(self.opponent):
            self.ball_speed_x *= -1


    def player_animation(self):
        self.player.y += self.player_speed
        if self.player.top <= 0:
            self.player.top = 0
        if self.player.bottom >= screen_height:
            self.player.bottom = screen_height


    def opponent_animation(self):
        # basic AI for the opponent
        # opponent basically follows the ball movement
        if self.opponent.top < self.ball.y:
            self.opponent.y += self.opponent_speed
        if self.opponent.bottom > self.ball.y:
            self.opponent.y -= self.opponent_speed

        if self.opponent.top <= 0:
            self.opponent.top = 0
        if self.opponent.bottom >= screen_height:
            self.opponent.bottom = screen_height


    def ball_restart(self):
        # resets the ball at the center with random directions
        self.ball.center = (screen_width / 2, screen_height / 2)

        self.ball_speed_y *= random.choice((-1, 1))
        self.ball_speed_x *= random.choice((-1, 1))