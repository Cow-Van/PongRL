from pong import Pong, screen
import numpy as np
from rl import Agent
import matplotlib.pyplot as plt
import tensorflow as tf
import psutil

ACTIONS = 3
STATE_COUNT = 6
TOTAL_GAMETIME = 100_000

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


def PlayExperiment(starting_model=0):
    GameTime = starting_model

    GameHistory = []

    # Create our PongGame instance
    TheGame = Pong()

    #  Create our Agent (including DQN based Brain)
    TheAgent = Agent(STATE_COUNT, ACTIONS)

    # Load existing model
    if starting_model > 0:
        model = tf.keras.models.load_model(f"models/{starting_model}.keras")
        TheAgent.setModel(model)

    # Initialise NextAction  Assume Action is scalar:  0:stay, 1:Up, 2:Down
    BestAction = 0

    # Default game state (doesn't really matter)
    GameState = CaptureNormalizedState(0, 0, 0, 0, 0, 0)

    # =================================================================
    try:
        # Main Experiment Loop
        for gtime in range(TOTAL_GAMETIME):
            GameEnd = False
            
            GameTicks = 0
            for i in range(5000):
                # Determine Next Action From the Agent
                BestAction = TheAgent.Act(GameState)

                #  Now Apply the Recommended Action into the Game
                ReturnScore, [ BallX, BallY, BallSpeedX, BallSpeedY, PlayerCenterY, OpponentCenterY ], GameEnd = TheGame.tick(BestAction)

                GameState = CaptureNormalizedState(BallX, BallY, BallSpeedX, BallSpeedY, PlayerCenterY, OpponentCenterY)

                if GameEnd:
                    GameTicks = i
                    break
            else:
                GameTicks = i
            
            TheGame = Pong()
            
            NextState = CaptureNormalizedState(BallX, BallY, BallSpeedX, BallSpeedY, PlayerCenterY, OpponentCenterY)

            # Capture the Sample [S, A, R, S"] in Agent Experience Replay Memory
            TheAgent.CaptureSample((GameState, BestAction, ReturnScore, NextState))

            #  Now Request Agent to DQN Train process  Against Experience
            TheAgent.Process()

            # Move State On
            GameState = NextState

            # Move GameTime Click
            GameTime = GameTime + 1

            # print our where we are after saving where we are
            if GameTime % 1000 == 0:
                # Save the Keras Model
                TheAgent.saveModel(GameTime)

            print(
                "Game Time: ",
                GameTime,
                "   Game Score: ",
                "{0:.4f}".format(ReturnScore),
                "   EPSILON: ",
                "{0:.4f}".format(TheAgent.epsilon),
                "   Ticks: ",
                "{0}".format(GameTicks),
            )

            process = psutil.Process()

            print(
                "Memory Usage: ",
                "{0}".format(process.memory_info().rss / 1024 ** 2),
                " MiB"
            )

            if GameTime % 50 == 0:
                GameHistory.append((GameTime, ReturnScore, TheAgent.epsilon))
    except KeyboardInterrupt:
        TheAgent.saveModel(GameTime)

    # ===============================================
    # End of Game Loop  so Plot the Score vs Game Time profile
    x_val = [x[0] for x in GameHistory]
    y_val = [x[1] for x in GameHistory]

    plt.plot(x_val, y_val)
    plt.xlabel("Game Time")
    plt.ylabel("Score")
    plt.show()
    # =======================================================================


def main():
    # Main Method Just Play our Experiment
    PlayExperiment(49150)

    # =======================================================================


if __name__ == "__main__":
    main()
