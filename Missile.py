import numpy as np
import os.path
import csv


class Missile:
    def __init__(self, config: dict) -> None:
        self.__cfg = config

        for key, value in self.__cfg.items():
            setattr(self, key, value)

        self.launch_angle = np.radians(self.launch_angle)

        self.dt = self.max_simulation_time / self.num_time_steps

        self.pos_array = np.zeros((self.num_time_steps, 2))
        self.vel_array = np.zeros((self.num_time_steps, 2))
        self.initialize()

    def initialize(self):
        self.pos_array[0, :] = 0
        self.vel_array[0, :] = 0

    def simulate(self):
        "Simulate the trajectory of a missile instance using Euler's method."
        frames = np.linspace(0, self.max_simulation_time, self.num_time_steps)

        for step in range(1, self.num_time_steps):
            thrust = self.initial_thrust if frames[step] < self.thrust_duration else 0
            drag_force = -self.drag_coefficient * self.vel_array[step - 1, :]
            gravitational_force = np.array([0, -self.gravity * self.mass])
            thrust_force = thrust * np.array(
                [np.cos(self.launch_angle), np.sin(self.launch_angle)]
            )

            net_force = drag_force + gravitational_force + thrust_force
            acc = net_force / self.mass

            self.vel_array[step, :] = self.vel_array[step - 1, :] + acc * self.dt
            self.pos_array[step, :] = (
                self.pos_array[step - 1, :] + self.vel_array[step, :] * self.dt
            )

            if self.pos_array[step, 1] < 0:
                self.pos_array = self.pos_array[:step, :]
                break

    def save_config(self):
        def write_file(mode: str, writeheader: bool):
            with open(filename, mode, newline="") as csvfile:
                fieldnames = list(self.__cfg.keys())
                writer = csv.DictWriter(csvfile, fieldnames)

                if writeheader:
                    writer.writeheader()

                writer.writerow(self.__cfg)

        filename = "configs.csv"

        if os.path.isfile(filename):
            write_file("a", writeheader=False)

        else:
            write_file("w", writeheader=True)
