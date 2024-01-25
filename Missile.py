import numpy as np
import os.path
import csv


class Missile:
    def __init__(self, config: dict) -> None:
        self.cfg = config
        self.gravity = 9.81
        self.num_time_steps = 2000

        for key, value in self.cfg.items():
            setattr(self, key, value)

        self.launch_angle_rads = np.radians(self.launch_angle)

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
                [np.cos(self.launch_angle_rads), np.sin(self.launch_angle_rads)]
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

        self.boost_end_index = int(self.thrust_duration / self.dt)
        self.indices_for_every_second = np.arange(
            0, self.pos_array.shape[0], int(1 / self.dt)
        )
        self.timestamps_array = self.pos_array[self.indices_for_every_second, :]

    def save_config(self):
        filename = "configs.csv"

        if os.path.isfile(filename):
            if not self.config_exists():
                self.write_file(filename, "a", self.cfg, False)
        else:
            self.write_file(filename, "w", self.cfg, True)

    def config_exists(self):
        configs = []

        with open("configs.csv", "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                configs.append(row)

        for config in configs:
            if config["name"] == self.cfg["name"]:
                configs.remove(config)
                configs.append(self.cfg)
                self.write_file("configs.csv", "w", configs, True)
                return True

    def write_file(self, filename: str, mode: str, data, writeheader: bool):
        with open(filename, mode, newline="") as csvfile:
            fieldnames = list(self.cfg.keys())
            writer = csv.DictWriter(csvfile, fieldnames)

            if writeheader:
                writer.writeheader()
            
            if isinstance(data, list):
                writer.writerows(data)
            else:
                writer.writerow(data)
