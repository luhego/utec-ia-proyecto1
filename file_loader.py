from collections import defaultdict

from entities import State, Action, ActionBranch


class FileLoader:
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

    def __get_states(self, rows):
        states = {}
        state_index = rows.index("states\n") + 1
        state_names = rows[state_index].strip().split(", ")
        for state_name in state_names:
            state = State(state_name.strip())
            states[state_name] = state
        return states

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

            action_branches = actions[key]
            actions[key] = {"cost": cost, "branches": action_branches}

            cost_index += 1

        return costs

    def __get_initial_state(self, rows, states):
        initial_state_index = rows.index(f"initialstate\n") + 1
        state_name = rows[initial_state_index].strip()
        return states[state_name]

    def __get_goal_state(self, rows, states):
        goal_state_index = rows.index(f"goalstate\n") + 1
        state_name = rows[goal_state_index].strip()
        return states[state_name]

    def __enrich_states(self, states, actions, goal_state):
        for state_name, action_name in actions.keys():
            # Ignoramos el estado objetivo
            if states[state_name] == goal_state:
                continue

            action = Action(
                name=action_name, cost=actions[(state_name, action_name)]["cost"]
            )
            for branch in actions[(state_name, action_name)]["branches"]:
                action.add_branch(
                    ActionBranch(
                        next_state=states[branch["next_state_name"]],
                        probability=branch["probability"],
                    )
                )
            states[state_name].add_action(action)
