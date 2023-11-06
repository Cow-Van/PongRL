import keras
import numpy as np
from pong import Pong, screen
from rl import Agent

ACTIONS = 3
STATE_COUNT = 6

def CaptureNormalizedState(
    ball_x, ball_y, ball_speed_x, ball_speed_y, player_center_y, opponent_center_y
):
    gstate = np.zeros([STATE_COUNT])
    gstate[0] = ball_x / screen.get_width()
    gstate[1] = ball_y / screen.get_height()
    gstate[2] = ball_speed_x / 7
    gstate[3] = ball_speed_y / 7
    gstate[4] = player_center_y / screen.get_height()
    gstate[5] = opponent_center_y / screen.get_height()

    return gstate


model = keras.models.load_model("models/9000.keras")

# Create our PongGame instance
TheGame = Pong(True)

while True:
    TheGame.tick()

    #  Create our Agent (including DQN based Brain)
    TheAgent = Agent(STATE_COUNT, ACTIONS)
    TheAgent.setModel(model)

    # # Initialise NextAction  Assume Action is scalar:  0:stay, 1:Up, 2:Down
    BestAction = 0

    GameState = CaptureNormalizedState(0, 0, 0, 0, 0, 0)

    BestAction = TheAgent.Act(GameState)

    # #  Now Apply the Recommended Action into the Game
    ReturnScore, [ BallX, BallY, BallSpeedX, BallSpeedY, PlayerCenterY, OpponentCenterY ], GameEnd = TheGame.tick(BestAction)

    GameState = CaptureNormalizedState(BallX, BallY, BallSpeedX, BallSpeedY, PlayerCenterY, OpponentCenterY)