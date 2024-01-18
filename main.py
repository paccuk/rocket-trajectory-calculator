from Missile import Missile
from Animation import Animation

missile_config = {
    "name": "Missile",
    "mass": 100,  # mass             (kg)
    "gravity": 9.81,  # gravity constant (m/s^2)
    "drag_coefficient": 2,  # drag coefficient (unitless)
    "launch_angle": 70,  # launch angle     (radians)
    "initial_thrust": 5000,  # initial thrust   (N)
    "thrust_duration": 2,  # thrust duration  (s)
    "max_simulation_time": 100,  # max simulation time (s)
    "num_time_steps": 5000,  # number of time steps
}


if __name__ == "__main__":
    missile = Missile(missile_config)
    missile.simulate()
    missile.save_config()

    animation = Animation(missile)
    animation.animate_trajectory()
    animation.save_animation()
