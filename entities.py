class State:
    def __init__(self, name):
        self.name = name
        self.actions = []
        self.value = 0
        self.selected_action = None

    def add_action(self, action):
        self.actions.append(action)

    def __repr__(self) -> str:
        return self.name


class Action:
    def __init__(self, name, cost=1):
        self.name = name
        self.cost = cost
        self.branches = []

    def add_branch(self, branch):
        self.branches.append(branch)

    def __repr__(self) -> str:
        return f"Action[{self.name}, {self.cost}]"


class ActionBranch:
    def __init__(self, next_state, probability) -> None:
        self.next_state = next_state
        self.probability = probability

    def __repr__(self):
        return f"ActionBranch[{self.next_state}, {self.probability}]"
