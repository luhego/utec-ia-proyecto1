class State:
    def __init__(self, name):
        self.name = name

    def __repr__(self) -> str:
        return self.name


class Action:
    def __init__(self, name):
        self.name = name
        self.transitions = []

    def add_transition(self, transition):
        self.transitions.append(transition)


class Transition:
    def __init__(self, current_state, next_state, probability):
        self.current_state = current_state
        self.next_state = next_state
        self.probability = probability

    def __repr__(self) -> str:
        return f"Transition[current_state={self.current_state}, next_state={self.next_state}, probability={self.probability}]"
