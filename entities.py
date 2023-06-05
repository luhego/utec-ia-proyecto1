class State:
    """
    Una clase que representa un estado del problema.

    Attributes
    ----------
    name: str
        Nombre del estado. Ejemplo: robot-at-x1y1
    actions: List[Action]
        Lista de acciones disponibles para el estado actual.
    value: float
        Valor del estado que se actualizará usando el algoritmo Bellman backup.
    selected_action: str
        Accion escogida luega de evaluar todas las acciones disponibles del estado actual.
    """

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
    """
    Una clase que representa un una acción.

    Attributes
    ----------
    name: str
        Nombre de la acción. Por ejemplo: move-south, move-north, move-east, move-west.

    cost: float
        Costo de la acción.

    transitions: List[Transition]
        Lista de transiciones disponibles para una acción.

        Por ejemplo, para el estado robot-at-x5-y2, la misma accion move-south puede ir a
        dos estados distintos con probabilidad 0.5.
        action move-south
            robot-at-x5y2 robot-at-x5y1 0.500000
            robot-at-x5y2 robot-at-x5y2 0.500000
    """

    def __init__(self, name, cost=1):
        self.name = name
        self.cost = cost
        self.transitions = []

    def add_transition(self, transition):
        self.transitions.append(transition)

    def __repr__(self) -> str:
        return f"Action[{self.name}, {self.cost}]"


class Transition:
    """
    Una clase que representa una transición.

    Attributes
    ----------
    next_state: State
        Estado siguiente o destino.

    probability: float
        Probabilidad de la transición.
    """

    def __init__(self, next_state, probability) -> None:
        self.next_state = next_state
        self.probability = probability

    def __repr__(self):
        return f"Transition[{self.next_state}, {self.probability}]"
