import pandas as pd
import math


def analyze_cfd_file(file_path):

    data = pd.read_csv(file_path)

    # -------------------------
    # VELOCITY
    # -------------------------

    velocities = data["velocity"]

    maximum_velocity = velocities.max()
    minimum_velocity = velocities.min()
    average_velocity = velocities.mean()


    # -------------------------
    # PRESSURE
    # -------------------------

    pressures = data["pressure"]

    maximum_pressure = pressures.max()
    minimum_pressure = pressures.min()

    pressure_drop = (
        maximum_pressure - minimum_pressure
    )


    # -------------------------
    # PIPE
    # -------------------------

    diameter = 0.05  # 50 mm


    # -------------------------
    # AREA
    # -------------------------

    area = math.pi * diameter**2 / 4


    # -------------------------
    # FLOW RATE
    # -------------------------

    flow_rate = area * average_velocity


    # -------------------------
    # REYNOLDS NUMBER
    # -------------------------

    density = 998.2
    viscosity = 0.001003

    reynolds_number = (
        density
        * average_velocity
        * diameter
    ) / viscosity


    # -------------------------
    # FLOW REGIME
    # -------------------------

    if reynolds_number < 2300:

        flow_regime = "Laminar"

    elif reynolds_number < 4000:

        flow_regime = "Transitional"

    else:

        flow_regime = "Turbulent"


    # -------------------------
    # DISPLAY RESULTS
    # -------------------------

    print("----- VELOCITY -----")

    print(
        "Maximum:",
        maximum_velocity,
        "m/s"
    )

    print(
        "Minimum:",
        minimum_velocity,
        "m/s"
    )

    print(
        "Average:",
        average_velocity,
        "m/s"
    )


    print("\n----- PRESSURE -----")

    print(
        "Maximum:",
        maximum_pressure,
        "Pa"
    )

    print(
        "Minimum:",
        minimum_pressure,
        "Pa"
    )

    print(
        "Pressure Drop:",
        pressure_drop,
        "Pa"
    )


    print("\n----- FLOW -----")

    print(
        "Flow Rate:",
        flow_rate,
        "m³/s"
    )


    print("\n----- FLOW TYPE -----")

    print(
        "Reynolds Number:",
        reynolds_number
    )

    print(
        "Flow Regime:",
        flow_regime
    )


    return {
    "maximum_velocity": float(maximum_velocity),
    "minimum_velocity": float(minimum_velocity),
    "average_velocity": float(average_velocity),

    "maximum_pressure": float(maximum_pressure),
    "minimum_pressure": float(minimum_pressure),
    "pressure_drop": float(pressure_drop),

    "flow_rate": float(flow_rate),

    "reynolds_number": float(reynolds_number),
    "flow_regime": flow_regime
}