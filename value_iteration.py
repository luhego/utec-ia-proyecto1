class ValueIteration:
    def __init__(
        self,
        states,
        initial_state,
        goal_state,
        epsilon=0.01,
    ):
        self.states = states
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.epsilon = epsilon

        self.num_states = len(self.states.keys())

    """
    Ejecutamos el algoritmo de iteración de valor mientras el residual calculado sea menor al epsilon.
    """

    def run(self):
        iteration = 1
        max_residual = self.__run_one_step()
        while max_residual > self.epsilon:
            iteration += 1
            max_residual = self.__run_one_step()

        self.__calculate_policy()

    """
    Corremos una iteración del algoritmo de iteración de valor de la siguiente manera:

    1. Recorremos todos los estados.
    2. Para cada estado:
     2.1. Corremos el algoritmo Bellman backup para calcular la función de valor del estado y la acción escogida.
     2.2. Actualizamos la función de valor para el estado.
     2.3. Calculamos el residual calculando el valor absoluto de la diferencia del valor actual del estado y el valor previo.
    4. Calculamos el residual maximo de todos los residuales calculados.
    """

    def __run_one_step(self):
        max_residual = 0

        residuals = []

        # 1. Iteramos sobre todos los estados
        for state in self.states.values():
            previous_value = state.value

            # Calculamos la función de valor usando la ecuación de Bellman para el estado state_name
            selected_action, new_value = self.__run_bellman_backup(state)

            # Actualizamos la función de valor para el estado s
            state.value = new_value
            state.selected_action = selected_action

            # Calculamos el residual
            residual = abs(new_value - previous_value)

            residuals.append(residual)

        max_residual = max(residuals)
        return max_residual

    """
    Corremos el algoritmo Bellman backup para un estado de la siguiente manera:
    1. Iteramos todas las acciones disponibles para el estado:
    2. Para cada accion, calculamos el valor.
    3. Escogemos la acción con el menor valor.
    """

    def __run_bellman_backup(self, state):
        if state == self.goal_state:
            state.value = 0
            return None, state.value

        # Por cada estados, iteramos sobre todas las acciones
        actions_values = []
        for action in state.actions:
            value = 0
            for transition in action.transitions:
                value += transition.probability * (action.cost + transition.next_state.value)
            actions_values.append((action, value))

        # Escogemos la accion con el menor valor
        min_action = min(actions_values, key=lambda action_value: action_value[1])

        selected_action = min_action[0]
        new_value = min_action[1]

        return selected_action, new_value

    def __calculate_policy(self):
        for state in self.states.values():
            if state == self.goal_state:
                print(state.name + " goal state 0")
            else:
                print(state.name + " " + state.selected_action.name + " " + str(state.value))
