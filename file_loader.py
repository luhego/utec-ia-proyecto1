from entities import State, Action, Transition


class FileLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        with open(self.file_path, "r") as file:
            rows = file.readlines()

        states_map = self.__get_states(rows)
        actions_map = self.__get_actions(rows, states_map)
        costs_map = self.__get_costs(rows)
        initial_state = self.__get_initial_state(rows, states_map)
        goal_state = self.__get_goal_state(rows, states_map)

        return states_map, actions_map, costs_map, initial_state, goal_state

    def __get_states(self, rows):
        states_map = {}
        state_index = rows.index("states\n") + 1
        state_names = rows[state_index].strip().split(", ")
        for state_name in state_names:
            state = State(state_name.strip())
            states_map[state_name] = state
        return states_map

    def __get_actions(self, rows, states_map):
        actions_map = {}

        def helper(action_name):
            action_index = rows.index(f"action {action_name}\n") + 1
            action = Action(action_name)
            while rows[action_index].strip() != "endaction":
                action_data = rows[action_index].strip().split()
                current_state_name = action_data[0]
                next_state_name = action_data[1]
                probability = float(action_data[2])
                action.add_transition(
                    Transition(
                        states_map[current_state_name],
                        states_map[next_state_name],
                        probability,
                    )
                )
                action_index += 1

            actions_map[action_name] = action

        helper("move-south")
        helper("move-north")
        helper("move-west")
        helper("move-east")

        return actions_map

    def __get_costs(self, rows):
        costs_map = {}

        cost_index = rows.index(f"cost\n") + 1
        while rows[cost_index].strip() != "endcost":
            cost_data = rows[cost_index].strip().split()
            state_name = cost_data[0]
            action_name = cost_data[1]
            cost = cost_data[2]

            costs_map[f"{state_name}|{action_name}"] = cost
            cost_index += 1

        return costs_map

    def __get_initial_state(self, rows, states_map):
        initial_state_index = rows.index(f"initialstate\n") + 1
        state_name = rows[initial_state_index].strip()
        return states_map[state_name]

    def __get_goal_state(self, rows, states_map):
        goal_state_index = rows.index(f"goalstate\n") + 1
        state_name = rows[goal_state_index].strip()
        return states_map[state_name]
