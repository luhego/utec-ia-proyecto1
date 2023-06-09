import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arrow


class GridDrawer:
    def __init__(self, grid, states, initial_state, goal_state) -> None:
        self.grid = grid
        self.states = states
        self.initial_state = initial_state
        self.goal_state = goal_state

    def draw(self):
        grid_array = np.array(self.grid)
        num_rows = grid_array.shape[0]
        num_cols = grid_array.shape[1]

        # Definimos los colores a utilizar en el grid
        colors = {
            0: "white",  # Celda normal
            1: "black",  # Pared
            2: "green",  # Estado Inicial
            3: "red",  # Estado Final
            4: "white",  # Marca que indica que hay una pared al lado
        }

        fig_width = num_cols * 0.50
        fig_height = num_rows * 0.50
        _, ax = plt.subplots(figsize=(fig_width, fig_height))
        ax.set_aspect("equal")

        # Dibujamos las lineas horizontales
        for i in range(num_rows + 1):
            ax.plot([0, num_rows], [i, i], color="gray", linestyle="-", linewidth=1)

        # Dibujamos las lineas verticales
        for j in range(num_cols + 1):
            ax.plot([j, j], [0, num_rows], color="gray", linestyle="-", linewidth=1)

        # Iteramos sobre el grid y dibujamos las celdas
        for i in range(num_rows):
            for j in range(num_cols):
                value = grid_array[i, j]
                color = colors.get(value, "white")
                ax.add_patch(plt.Rectangle((j, num_rows - i - 1), 1, 1, color=color))

        # Iteramos sobre los estados para dibujar las flechas
        for _, state in self.states.items():
            i = state.row
            j = state.col

            self.__draw_state(state, ax)

        ax.set_xlim([0, grid_array.shape[1]])
        ax.set_ylim([0, grid_array.shape[0]])

        ax.set_xticks([])
        ax.set_yticks([])

        # Dibujamos el grid
        plt.savefig("grid.png")
        # plt.show()

    # Dibujamos el estado y la acción en el grid
    def __draw_state(self, state, ax):
        if state == self.goal_state:
            return

        arrow = self.__get_arrow(state.selected_action.name, state.x, state.y)
        if not arrow:
            return
        arrow.set_linewidth(1)
        arrow.set_color("red")
        ax.add_patch(arrow)

    # Generamos el objeto Arrow de acuerdo a la acción que luega se usará para visualizar la flecha
    def __get_arrow(self, action_name, x, y):
        arrow = None
        if action_name == "move-south":
            arrow = Arrow(x - 0.5, y, 0, -1, color="white", width=0.2)
        elif action_name == "move-north":
            arrow = Arrow(x - 0.5, y - 1, 0, 1, color="white", width=0.2)
        elif action_name == "move-west":
            arrow = Arrow(x, y - 0.5, -1, 0, color="white", width=0.2)
        elif action_name == "move-east":
            arrow = Arrow(x - 1, y - 0.5, 1, 0, color="white", width=0.2)
        return arrow
