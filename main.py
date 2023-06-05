import argparse

from file_loader import FileLoader
from value_iteration import ValueIteration


def run():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-a",
        "--algorithm",
        choices=["VI", "PI", "LAO"],
        default="VI",
        help="Algoritmo a utilizar. VI: iteración de valor. PI: iteración de política. LAO: algoritmo LAO.",
    )

    parser.add_argument(
        "-f",
        "--file_path",
        required=True,
        type=str,
        help="Ruta del archivo que contiene la instancia del problema grid.",
    )

    parser.add_argument(
        "-e",
        "--epsilon",
        type=float,
        default=0.1,
        help="Valor del parámetro epsilon usado como condición de parada del algoritmo.",
    )

    print("UTEC - Incertidumbre en IA - Proyecto 1")

    args = parser.parse_args()
    file_loader = FileLoader(args.file_path)
    states, initial_state, goal_state = file_loader.load()

    value_iteration = ValueIteration(states, initial_state, goal_state, args.epsilon)
    value_iteration.run()


if __name__ == "__main__":
    run()
