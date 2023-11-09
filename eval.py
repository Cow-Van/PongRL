class Eval():
    def __init__(self) -> None:
        self.eval = 0

    def tick(self):
        self.eval += 0.0001

    def bounce(self):
        print("Bounce")
        self.eval += 0.01

    def win(self):
        print("Win")
        self.eval += 0.2

    def lose(self):
        print("Lose")
        # self.eval -= 0.1
        pass

    def get_eval(self):
        return self.eval

    def reset(self):
        self.eval = 0