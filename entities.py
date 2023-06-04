class State:
    def __init__(self, name):
        self.name = name

    def __repr__(self) -> str:
        return self.name


class Action:
    def __init__(self, name, current_state, next_state, probability, cost=1):
        self.name = name
        self.current_state = current_state
        self.next_state = next_state
        self.probability = probability
        self.cost = cost

    def __repr__(self) -> str:
        return f"Action[{self.name}, {self.current_state}, {self.next_state}, {self.probability}, {self.cost}]"
