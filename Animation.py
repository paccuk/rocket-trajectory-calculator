import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


class Animation:
    def __init__(self, missile) -> None:
        self.missile = missile

    def animate_trajectory(self):
        "Animate the trajectory of a missile instance."

        color = "#636EFA"
        indices_for_every_second = np.arange(
            0, self.missile.pos_array.shape[0], int(1 / self.missile.dt)
        )
        timestamps_array = self.missile.pos_array[indices_for_every_second, :]
        boost_end_index = int(self.missile.thrust_duration / self.missile.dt)

        fig, ax = plt.subplots()

        (ballistic_phase,) = ax.plot(
            [], [], c=color, lw=2, alpha=0.6, ls="--", label="Ballistic phase"
        )

        (boost_phase,) = ax.plot([], [], c=color, lw=2, label="Boost phase")

        timestamps = ax.scatter(
            [], [], c=color, alpha=0.9, marker="o", label="Seccond passed"
        )

        ax.set(
            xlim=[-25, 500],
            ylim=[-25, 400],
            xlabel="X (m)",
            ylabel="Y (m)",
            title="Missile Trajectory",
        )
        ax.legend(fontsize="small")
        ax.grid(True)

        def init():
            ballistic_phase.set_data([], [])
            boost_phase.set_data([], [])
            timestamps.set_offsets(np.array([]).reshape(0, 2))

            return ballistic_phase, boost_phase, timestamps

        def update(frame):
            ballistic_phase.set_data(
                self.missile.pos_array[:frame, 0], self.missile.pos_array[:frame, 1]
            )

            if frame < boost_end_index:
                boost_phase.set_data(
                    self.missile.pos_array[:frame, 0], self.missile.pos_array[:frame, 1]
                )

            if frame in indices_for_every_second:
                timestamps.set_offsets(
                    timestamps_array[
                        : np.where(indices_for_every_second == frame)[0][0] + 1, :
                    ]
                )

            return (ballistic_phase, boost_phase, timestamps)

        self.ani = animation.FuncAnimation(
            fig=fig,
            func=update,
            init_func=init,
            blit=True,
            frames=self.missile.pos_array.shape[0],
            interval=20,
        )

        plt.show()

    def save_animation(self):
        self.ani.save(f"{self.missile.name}.mp4")
