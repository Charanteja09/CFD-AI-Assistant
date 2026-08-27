import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def create_graphs(file_path):

    # Read CFD data
    data = pd.read_csv(file_path)

    # Find the main project folder
    project_folder = Path(__file__).resolve().parent.parent

    # Create generated folder automatically
    generated_folder = project_folder / "generated"

    generated_folder.mkdir(
        exist_ok=True
    )

    # -------------------------
    # VELOCITY GRAPH
    # -------------------------

    plt.figure(figsize=(8, 5))

    plt.plot(
        data["position"],
        data["velocity"],
        marker="o"
    )

    plt.xlabel("Position (m)")
    plt.ylabel("Velocity (m/s)")
    plt.title("Velocity vs Position")

    plt.grid(True)

    velocity_path = (
        generated_folder / "velocity.png"
    )

    plt.savefig(velocity_path)

    plt.close()


    # -------------------------
    # PRESSURE GRAPH
    # -------------------------

    plt.figure(figsize=(8, 5))

    plt.plot(
        data["position"],
        data["pressure"],
        marker="o"
    )

    plt.xlabel("Position (m)")
    plt.ylabel("Pressure (Pa)")
    plt.title("Pressure vs Position")

    plt.grid(True)

    pressure_path = (
        generated_folder / "pressure.png"
    )

    plt.savefig(pressure_path)

    plt.close()


    print("Graphs created successfully!")

    print(
        "Velocity graph:",
        velocity_path
    )

    print(
        "Pressure graph:",
        pressure_path
    )