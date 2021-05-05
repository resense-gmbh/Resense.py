import matplotlib.pyplot as plt
from .recording import *


def _show_generic_xyz_plot(time_points, x, y, z, y_label, legend, name):
    plt.plot(time_points, x, label="x")
    plt.plot(time_points, y, label="y")
    plt.plot(time_points, z, label="z")
    plt.title(name)
    plt.xlabel("Zeit (s)")
    plt.ylabel(y_label)
    plt.legend(loc=legend)
    plt.grid()
    plt.show()


def display_force_plot(recording: BufferedRecording, legend: str = "upper left", name: str = None):
    time_points = recording.get_array_of_timestamps()
    x_points = recording.get_array_of_values(Variable.FORCE, Direction.X)
    y_points = recording.get_array_of_values(Variable.FORCE, Direction.Y)
    z_points = recording.get_array_of_values(Variable.FORCE, Direction.Z)

    _show_generic_xyz_plot(time_points, x_points, y_points, z_points, "Force (N)", legend, name)


def display_torque_plot(recording: BufferedRecording, legend: str = "upper left", name: str = None):
    time_points = recording.get_array_of_timestamps()
    x_points = recording.get_array_of_values(Variable.TORQUE, Direction.X)
    y_points = recording.get_array_of_values(Variable.TORQUE, Direction.Y)
    z_points = recording.get_array_of_values(Variable.TORQUE, Direction.Z)

    _show_generic_xyz_plot(time_points, x_points, y_points, z_points, "Torque (mNm)", legend, name)
