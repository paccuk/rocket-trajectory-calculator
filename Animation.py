from PyQt5.QtWidgets import QSizePolicy, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import animation
import matplotlib.pyplot as plt
import numpy as np


class Animation:
    def __init__(self) -> None:
        self.is_active = False

    def animate_trajectory(self, ax, fig, missiles, show_legend=False):
        "Animate the trajectory of a missile instance."

        self.missiles = missiles
        self.colors = [f"C{i}" for i in range(len(self.missiles))]
        self.names = [missile.name for missile in self.missiles]

        ballistic_phase = [
            ax.plot(
                [],
                [],
                lw=1,
                alpha=0.6,
                ls="--",
                label=f"Ballistic phase: {name}",
                color=color,
            )[0]
            for name, color in zip(self.names, self.colors)
        ]

        boost_phase = [
            ax.plot([], [], lw=1, label=f"Boost phase: {name}", color=color)[0]
            for name, color in zip(self.names, self.colors)
        ]

        timestamps = [
            ax.scatter(
                [],
                [],
                alpha=0.9,
                marker=".",
                label=f"Seconds passed: {name}",
                color=color,
            )
            for name, color in zip(self.names, self.colors)
        ]

        max_X = max(m.pos_array[:, 0].max() for m in self.missiles)
        max_Y = max(m.pos_array[:, 1].max() for m in self.missiles)

        ax.set(
            xlim=[-25, max_X + 250],
            ylim=[-25, max_Y + 250],
            xlabel="X (m)",
            ylabel="Y (m)",
            title="Missile Trajectories",
        )
        if show_legend:
            ax.legend(loc="upper right", fontsize="small")
        ax.grid(True)

        def init():
            for trajectory, boost, timestamp in zip(
                ballistic_phase, boost_phase, timestamps
            ):
                trajectory.set_data([], [])
                boost.set_data([], [])
                timestamp.set_offsets(np.array([]).reshape(0, 2))

            return ballistic_phase + boost_phase + timestamps

        def update(frame):
            for _, (missile, trajectory, boost, timestamp) in enumerate(
                zip(self.missiles, ballistic_phase, boost_phase, timestamps)
            ):
                trajectory.set_data(
                    missile.pos_array[:frame, 0], missile.pos_array[:frame, 1]
                )

                if frame < missile.boost_end_index:
                    boost.set_data(
                        missile.pos_array[:frame, 0], missile.pos_array[:frame, 1]
                    )

                if frame in missile.indices_for_every_second:
                    timestamp.set_offsets(
                        missile.timestamps_array[
                            : np.where(missile.indices_for_every_second == frame)[0][0]
                            + 1,
                            :,
                        ]
                    )

            return ballistic_phase + boost_phase + timestamps

        self.ani = animation.FuncAnimation(
            fig=fig,
            func=update,
            init_func=init,
            blit=True,
            frames=max(m.pos_array.shape[0] for m in self.missiles),
            interval=20,
        )

    def save_animation(self):
        self.ani.save(filename="missiles_animation.gif", writer="pillow")


class MissileAnimationWidget(QWidget):
    def __init__(self, parent):
        super(MissileAnimationWidget, self).__init__(parent)
        self.animation = Animation()

        self.figure, self.ax = plt.subplots()

        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QVBoxLayout()
        layout.addWidget(NavigationToolbar2QT(self.canvas, self))
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def start_animation(self, missiles, show_legend):
        self.animation.is_active = True
        self.animation.animate_trajectory(self.ax, self.figure, missiles, show_legend)
        self.canvas.draw()
