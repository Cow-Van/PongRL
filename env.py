## Inputs ##
# Ball X #
# Ball Y #
# Ball Speed X #
# Ball Speed Y #
# Player Center Y #
# Opponent Center Y #

class Env:
    def update(self, ball_x, ball_y, ball_speed_x, ball_speed_y, player_center_y, opponent_center_y) -> None:
        self.ball_x = ball_x
        self.ball_y = ball_y
        self.ball_speed_x = ball_speed_x
        self.ball_speed_y = ball_speed_y
        self.player_center_y = player_center_y
        self.opponent_center_y = opponent_center_y
    
    def get_all(self):
        return [self.ball_x, self.ball_y, self.ball_speed_x, self.ball_speed_y, self.player_center_y, self.opponent_center_y]

## Outputs ##
# Up? #
# Down? #
# None? #