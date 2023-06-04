import numpy as np


class ValueIteration:
    def __init__(
        self,
        states,
        actions,
        costs,
        initial_state,
        goal_state,
        epsilon=0.01,
    ):
        self.states = states
        self.actions = actions
        self.costs = costs
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.epsilon = epsilon

        self.num_states = len(self.states_map.keys())

        # Inicializamos la función de valor inicial con zeros
        self.value_function = np.zeros(self.num_states)

    def run(self):
        # Ejecutamos el algoritmo de iteración de valor
        iteration = 0
        residual = 0
        while True:
            iteration += 1

            # Iteramos sobre todos los estados
            for state_name in self.states_map.keys():
                # Calculamos la función de valor usando la ecuación de Bellman para el estado state_name

                # Calculamos el residual
                pass

    def __execute_bellman(self, state):
        pass
