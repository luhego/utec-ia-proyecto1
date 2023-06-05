from collections import defaultdict

from entities import State, Action, Transition


class FileLoader:
    """
    Una clase que representa un file loader. El file loader se utiliza para leer los archivos
    de entrada e instancias del problema y extraer la información necesario como los estados,
    acciones, costos, estado inicial y final.
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        with open(self.file_path, "r") as file:
            rows = file.readlines()

        states = self.__get_states(rows)
        actions = self.__get_actions(rows)
        _ = self.__get_costs(rows, actions)
        initial_state = self.__get_initial_state(rows, states)
        goal_state = self.__get_goal_state(rows, states)

        self.__enrich_states(states, actions, goal_state)

        return states, initial_state, goal_state

    """
    Extraemos los estados del archivo de entrada en un diccionario con el siguiente formato:
    states = {"robot-at-x1y1": State("robot-at-x1y1"), ...}
    """

    def __get_states(self, rows):
        states = {}
        state_index = rows.index("states\n") + 1
        state_names = rows[state_index].strip().split(", ")
        for state_name in state_names:
            state = State(state_name.strip())
            states[state_name] = state
        return states

    """
    Extraemos las acciones del archivo de entrada en un diccionario con el siguiente formato:
        actions = {
            ("robot-at-x1y1", "move_south"): {"next_state": "robot-at-x1y1", "probability": 1},
            ...
        }
    """

    def __get_actions(self, rows):
        actions = defaultdict(list)

        def helper(action_name):
            action_index = rows.index(f"action {action_name}\n") + 1
            while rows[action_index].strip() != "endaction":
                action_data = rows[action_index].strip().split()
                current_state_name = action_data[0]
                next_state_name = action_data[1]
                probability = float(action_data[2])

                actions[(current_state_name, action_name)].append(
                    {"next_state_name": next_state_name, "probability": probability}
                )
                action_index += 1

        helper("move-south")
        helper("move-north")
        helper("move-west")
        helper("move-east")

        return actions

    """
    Extraemos los costos del archivo de entrada y actualizamos el diccionario de acciones:
    actions = {
        ("robot-at-x1y1", "move_south"): {
            "cost": 1,
            "transitions": [
                {"next_state": "robot-at-x1y1", "probability": 1}
            ]
        },
        ...
    }
    """

    def __get_costs(self, rows, actions):
        costs = {}

        cost_index = rows.index(f"cost\n") + 1
        while rows[cost_index].strip() != "endcost":
            cost_data = rows[cost_index].strip().split()
            state_name = cost_data[0]
            action_name = cost_data[1]
            cost = float(cost_data[2])

            key = (state_name, action_name)
            costs[key] = cost

            action_transitions = actions[key]
            actions[key] = {"cost": cost, "transitions": action_transitions}

            cost_index += 1

        return costs

    """
    Extraemos el estado inicial.
    """

    def __get_initial_state(self, rows, states):
        initial_state_index = rows.index(f"initialstate\n") + 1
        state_name = rows[initial_state_index].strip()
        return states[state_name]

    """
    Extraemos el estado objetivo.
    """

    def __get_goal_state(self, rows, states):
        goal_state_index = rows.index(f"goalstate\n") + 1
        state_name = rows[goal_state_index].strip()
        return states[state_name]

    """
    Actualizamos los estados con las acciones disponibles para el estado actual.
    """

    def __enrich_states(self, states, actions, goal_state):
        for state_name, action_name in actions.keys():
            # Ignoramos el estado objetivo
            if states[state_name] == goal_state:
                continue

            action = Action(name=action_name, cost=actions[(state_name, action_name)]["cost"])
            for branch in actions[(state_name, action_name)]["transitions"]:
                action.add_transition(
                    Transition(
                        next_state=states[branch["next_state_name"]],
                        probability=branch["probability"],
                    )
                )
            states[state_name].add_action(action)
