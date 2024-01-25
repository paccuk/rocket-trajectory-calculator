import csv
from PyQt5 import QtCore, QtGui, QtWidgets
from random import randint
import sys, os

from Animation import MissileAnimationWidget
from Missile import Missile


class MissileAnimationApp(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MissileAnimationApp, self).__init__(parent)
        self.setup_ui()
        self.missiles_inst_dict = {}

    def setup_ui(self):
        self.setObjectName("Missile Animation")
        self.setWindowTitle("Missile Animation")
        self.resize(1024, 768)
        self.setMinimumSize(QtCore.QSize(1024, 768))
        self.setInputMethodHints(QtCore.Qt.ImhNone)
        self.main_widget = QtWidgets.QWidget(self)
        self.main_widget.setObjectName("main_widget")
        self.gridLayout = QtWidgets.QGridLayout(self.main_widget)
        self.gridLayout.setObjectName("gridLayout")

        self.init_animation_frame()
        self.init_simulation_result_frame()
        self.init_missile_params_frame()

        self.init_missile_params_box()
        self.init_config_box()

        self.init_spacer()

        self.init_animation_box()
        self.init_single_missile_anim_checkbox()
        self.init_simulate_btn()

        self.init_widgets()

        self.init_menubar()
        self.init_save_cfg_act()
        self.init_load_cfg_act()
        self.init_save_anim_act()

        self.add_menubar_actions()

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "Missile Simulation"))
        self.result_table_widget.headerItem().setText(0, _translate("self", "Name"))
        self.result_table_widget.headerItem().setText(
            1, _translate("self", "Flight distance")
        )
        self.result_table_widget.headerItem().setText(
            2, _translate("self", "Max speed")
        )
        self.result_table_widget.headerItem().setText(
            3, _translate("self", "Highest point")
        )
        self.result_table_widget.headerItem().setText(
            4, _translate("self", "Boost duration")
        )
        self.result_table_widget.headerItem().setText(
            5, _translate("self", "Ballistic duration")
        )
        self.result_table_widget.headerItem().setText(
            6, _translate("self", "Sum duration")
        )
        self.mis_params_box.setTitle(_translate("self", "Missile parameters"))
        self.name_label.setText(_translate("self", "Name"))
        self.mass_label.setText(_translate("self", "Mass"))
        self.mass_input.setSuffix(_translate("self", " kg", "gg"))
        self.drag_coeff_label.setText(_translate("self", "Drag coefficient"))
        self.launch_angle_label.setText(_translate("self", "Launch angle"))
        self.launch_angle_input.setSuffix(_translate("self", " rad"))
        self.init_thrust_label.setText(_translate("self", "Itinital thrust"))
        self.init_thrust_input.setSuffix(_translate("self", " N"))
        self.thrust_dut_label.setText(_translate("self", "Thrust duration"))
        self.thrust_dur_input.setSuffix(_translate("self", " s"))
        self.simult_time_label.setText(_translate("self", "Simulation time"))
        self.simul_time_input.setSuffix(_translate("self", " s"))
        self.add_missile_btn.setText(_translate("self", "Add to animation"))
        self.random_btn.setText(_translate("self", "Randomize params"))
        self.defaults_btn.setText(_translate("self", "Set defaults"))
        self.configs_box.setTitle(_translate("self", "Missiles to animate"))
        self.remove_missile_btn.setText(_translate("self", "Remove from animation"))
        self.animation_box.setTitle(_translate("self", "Animation"))
        self.show_legend_checkbox.setText(_translate("self", "Show legend"))
        self.animate_single_missile_checkbox.setText(
            _translate("self", "Animate single missile")
        )
        self.simulate_btn.setText(_translate("self", "Animate"))
        self.config_menu.setTitle(_translate("self", "Config"))
        self.anim_menu.setTitle(_translate("self", "Animation"))
        self.save_cfg_act.setText(_translate("self", "Save"))
        self.load_cfg_act.setText(_translate("self", "Load"))
        self.save_anim_act.setText(_translate("self", "Save"))

    def init_animation_frame(self):
        self.animation_frame = QtWidgets.QFrame(self.main_widget)
        self.animation_frame.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.animation_frame.sizePolicy().hasHeightForWidth()
        )
        self.animation_frame.setSizePolicy(sizePolicy)
        self.animation_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.animation_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.animation_frame.setObjectName("animation_frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.animation_frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.animation_widget = MissileAnimationWidget(self.animation_frame)
        self.animation_widget.setMinimumSize(QtCore.QSize(600, 450))
        self.animation_widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.animation_widget.setObjectName("animation_widget")
        self.verticalLayout_2.addWidget(self.animation_widget)
        self.gridLayout.addWidget(self.animation_frame, 0, 0, 1, 1)

    def init_simulation_result_frame(self):
        self.simulation_result_frame = QtWidgets.QFrame(self.main_widget)
        self.simulation_result_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.simulation_result_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.simulation_result_frame.setObjectName("simulation_result_frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.simulation_result_frame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.result_table_widget = QtWidgets.QTreeWidget(self.simulation_result_frame)
        self.result_table_widget.setMinimumSize(QtCore.QSize(600, 0))
        self.result_table_widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.result_table_widget.setObjectName("result_table_widget")
        self.verticalLayout_3.addWidget(self.result_table_widget)
        self.gridLayout.addWidget(self.simulation_result_frame, 1, 0, 1, 1)

    def init_missile_params_frame(self):
        self.missile_params_frame = QtWidgets.QFrame(self.main_widget)
        self.missile_params_frame.setMinimumSize(QtCore.QSize(150, 0))
        self.missile_params_frame.setMaximumSize(QtCore.QSize(250, 16777215))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(9)
        self.missile_params_frame.setFont(font)
        self.missile_params_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.missile_params_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.missile_params_frame.setObjectName("missile_params_frame")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.missile_params_frame)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.mis_params_box = QtWidgets.QGroupBox(self.missile_params_frame)

    def init_missile_params_box(self):
        font = QtGui.QFont()
        font.setPointSize(10)
        self.mis_params_box.setFont(font)
        self.mis_params_box.setObjectName("mis_params_box")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.mis_params_box)
        self.verticalLayout.setObjectName("verticalLayout")
        self.name_layout = QtWidgets.QVBoxLayout()
        self.name_layout.setContentsMargins(-1, -1, -1, 5)
        self.name_layout.setObjectName("name_layout")
        self.name_label = QtWidgets.QLabel(self.mis_params_box)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.name_label.setFont(font)
        self.name_label.setObjectName("name_label")
        self.name_layout.addWidget(self.name_label)
        self.name_input = QtWidgets.QLineEdit(self.mis_params_box)
        self.name_input.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.name_input.setFont(font)
        self.name_input.setObjectName("name_input")
        self.name_layout.addWidget(self.name_input)
        self.verticalLayout.addLayout(self.name_layout)
        self.mass_layout = QtWidgets.QVBoxLayout()
        self.mass_layout.setContentsMargins(-1, 0, -1, 5)
        self.mass_layout.setObjectName("mass_layout")
        self.mass_label = QtWidgets.QLabel(self.mis_params_box)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.mass_label.setFont(font)
        self.mass_label.setObjectName("mass_label")
        self.mass_layout.addWidget(self.mass_label)
        self.mass_input = QtWidgets.QDoubleSpinBox(self.mis_params_box)
        self.mass_input.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.mass_input.setFont(font)
        self.mass_input.setDecimals(1)
        self.mass_input.setMinimum(80.0)
        self.mass_input.setMaximum(750.0)
        self.mass_input.setSingleStep(10.0)
        self.mass_input.setProperty("value", 100.0)
        self.mass_input.setObjectName("mass_input")
        self.mass_layout.addWidget(self.mass_input)
        self.verticalLayout.addLayout(self.mass_layout)
        self.drag_coeff_layout = QtWidgets.QVBoxLayout()
        self.drag_coeff_layout.setContentsMargins(-1, -1, -1, 5)
        self.drag_coeff_layout.setObjectName("drag_coeff_layout")
        self.drag_coeff_label = QtWidgets.QLabel(self.mis_params_box)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.drag_coeff_label.setFont(font)
        self.drag_coeff_label.setObjectName("drag_coeff_label")
        self.drag_coeff_layout.addWidget(self.drag_coeff_label)
        self.drag_coeff_input = QtWidgets.QDoubleSpinBox(self.mis_params_box)
        self.drag_coeff_input.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.drag_coeff_input.setFont(font)
        self.drag_coeff_input.setDecimals(1)
        self.drag_coeff_input.setMaximum(10.0)
        self.drag_coeff_input.setProperty("value", 2.0)
        self.drag_coeff_input.setObjectName("drag_coeff_input")
        self.drag_coeff_layout.addWidget(self.drag_coeff_input)
        self.verticalLayout.addLayout(self.drag_coeff_layout)
        self.launch_angle_layout = QtWidgets.QVBoxLayout()
        self.launch_angle_layout.setContentsMargins(-1, -1, -1, 5)
        self.launch_angle_layout.setObjectName("launch_angle_layout")
        self.launch_angle_label = QtWidgets.QLabel(self.mis_params_box)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.launch_angle_label.setFont(font)
        self.launch_angle_label.setObjectName("launch_angle_label")
        self.launch_angle_layout.addWidget(self.launch_angle_label)
        self.launch_angle_input = QtWidgets.QDoubleSpinBox(self.mis_params_box)
        self.launch_angle_input.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.launch_angle_input.setFont(font)
        self.launch_angle_input.setDecimals(1)
        self.launch_angle_input.setMinimum(50.0)
        self.launch_angle_input.setMaximum(80.0)
        self.launch_angle_input.setProperty("value", 70.0)
        self.launch_angle_input.setObjectName("launch_angle_input")
        self.launch_angle_layout.addWidget(self.launch_angle_input)
        self.verticalLayout.addLayout(self.launch_angle_layout)
        self.init_thrust_layout = QtWidgets.QVBoxLayout()
        self.init_thrust_layout.setContentsMargins(-1, -1, -1, 5)
        self.init_thrust_layout.setObjectName("init_thrust_layout")
        self.init_thrust_label = QtWidgets.QLabel(self.mis_params_box)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.init_thrust_label.setFont(font)
        self.init_thrust_label.setObjectName("init_thrust_label")
        self.init_thrust_layout.addWidget(self.init_thrust_label)
        self.init_thrust_input = QtWidgets.QDoubleSpinBox(self.mis_params_box)
        self.init_thrust_input.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.init_thrust_input.setFont(font)
        self.init_thrust_input.setDecimals(0)
        self.init_thrust_input.setMinimum(4500.0)
        self.init_thrust_input.setMaximum(10000.0)
        self.init_thrust_input.setSingleStep(100.0)
        self.init_thrust_input.setProperty("value", 5000.0)
        self.init_thrust_input.setObjectName("init_thrust_input")
        self.init_thrust_layout.addWidget(self.init_thrust_input)
        self.verticalLayout.addLayout(self.init_thrust_layout)
        self.thrust_dur_layout = QtWidgets.QVBoxLayout()
        self.thrust_dur_layout.setContentsMargins(-1, -1, -1, 5)
        self.thrust_dur_layout.setObjectName("thrust_dur_layout")
        self.thrust_dut_label = QtWidgets.QLabel(self.mis_params_box)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.thrust_dut_label.setFont(font)
        self.thrust_dut_label.setObjectName("thrust_dut_label")
        self.thrust_dur_layout.addWidget(self.thrust_dut_label)
        self.thrust_dur_input = QtWidgets.QDoubleSpinBox(self.mis_params_box)
        self.thrust_dur_input.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.thrust_dur_input.setFont(font)
        self.thrust_dur_input.setDecimals(0)
        self.thrust_dur_input.setMinimum(1.0)
        self.thrust_dur_input.setMaximum(8.0)
        self.thrust_dur_input.setProperty("value", 2.0)
        self.thrust_dur_input.setObjectName("thrust_dur_input")
        self.thrust_dur_layout.addWidget(self.thrust_dur_input)
        self.verticalLayout.addLayout(self.thrust_dur_layout)
        self.simul_time_layout = QtWidgets.QVBoxLayout()
        self.simul_time_layout.setContentsMargins(-1, -1, -1, 5)
        self.simul_time_layout.setObjectName("simul_time_layout")
        self.simult_time_label = QtWidgets.QLabel(self.mis_params_box)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.simult_time_label.setFont(font)
        self.simult_time_label.setObjectName("simult_time_label")
        self.simul_time_layout.addWidget(self.simult_time_label)
        self.simul_time_input = QtWidgets.QDoubleSpinBox(self.mis_params_box)
        self.simul_time_input.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.simul_time_input.setFont(font)
        self.simul_time_input.setDecimals(0)
        self.simul_time_input.setMinimum(50.0)
        self.simul_time_input.setMaximum(200.0)
        self.simul_time_input.setSingleStep(5.0)
        self.simul_time_input.setProperty("value", 100.0)
        self.simul_time_input.setObjectName("simul_time_input")
        self.simul_time_layout.addWidget(self.simul_time_input)
        self.verticalLayout.addLayout(self.simul_time_layout)
        self.add_missile_btn = QtWidgets.QPushButton(self.mis_params_box)
        self.add_missile_btn.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.add_missile_btn.setFont(font)
        self.add_missile_btn.setObjectName("add_missile_btn")
        self.add_missile_btn.clicked.connect(self.add_missile)
        self.verticalLayout.addWidget(self.add_missile_btn)

        self.random_btn = QtWidgets.QPushButton(self.mis_params_box)
        self.random_btn.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.random_btn.setFont(font)
        self.random_btn.setObjectName("random_btn")
        self.random_btn.clicked.connect(self.randomize_missile_params)
        self.verticalLayout.addWidget(self.random_btn)

        self.defaults_btn = QtWidgets.QPushButton(self.mis_params_box)
        self.defaults_btn.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.defaults_btn.setFont(font)
        self.defaults_btn.setObjectName("defaults_btn")
        self.defaults_btn.clicked.connect(self.reset_defaults)
        self.verticalLayout.addWidget(self.defaults_btn)
        self.verticalLayout_5.addWidget(self.mis_params_box)

    def init_config_box(self):
        self.configs_box = QtWidgets.QGroupBox(self.missile_params_frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.configs_box.setFont(font)
        self.configs_box.setObjectName("configs_box")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.configs_box)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.missiles_list = QtWidgets.QComboBox(self.configs_box)
        self.missiles_list.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.missiles_list.setFont(font)
        self.missiles_list.setEditable(False)
        self.missiles_list.setObjectName("missiles_list")
        self.missiles_list.currentIndexChanged.connect(self.change_missile)
        self.gridLayout_2.addWidget(self.missiles_list, 0, 0, 1, 2)
        self.remove_missile_btn = QtWidgets.QPushButton(self.configs_box)
        self.remove_missile_btn.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.remove_missile_btn.setFont(font)
        self.remove_missile_btn.setObjectName("remove_missile_btn")
        self.remove_missile_btn.clicked.connect(self.remove_missile)
        self.gridLayout_2.addWidget(self.remove_missile_btn, 1, 0, 1, 2)
        self.verticalLayout_5.addWidget(self.configs_box)

    def init_spacer(self):
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_5.addItem(spacerItem)

    def init_animation_box(self):
        self.animation_box = QtWidgets.QGroupBox(self.missile_params_frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.animation_box.setFont(font)
        self.animation_box.setObjectName("animation_box")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.animation_box)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.show_legend_checkbox = QtWidgets.QCheckBox(self.animation_box)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.show_legend_checkbox.setFont(font)
        self.show_legend_checkbox.setObjectName("show_legend_checkbox")
        self.verticalLayout_4.addWidget(self.show_legend_checkbox)
        self.animate_single_missile_checkbox = QtWidgets.QCheckBox(self.animation_box)

    def init_single_missile_anim_checkbox(self):
        font = QtGui.QFont()
        font.setPointSize(9)
        self.animate_single_missile_checkbox.setFont(font)
        self.animate_single_missile_checkbox.setObjectName(
            "animate_single_missile_checkbox"
        )
        self.verticalLayout_4.addWidget(self.animate_single_missile_checkbox)

    def init_simulate_btn(self):
        self.simulate_btn = QtWidgets.QPushButton(self.animation_box)
        self.simulate_btn.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.simulate_btn.setFont(font)
        self.simulate_btn.setMouseTracking(False)
        self.simulate_btn.setObjectName("simulate_btn")
        self.simulate_btn.clicked.connect(self.animate_missiles)
        self.verticalLayout_4.addWidget(self.simulate_btn)

    def init_widgets(self):
        self.verticalLayout_5.addWidget(self.animation_box)
        self.gridLayout.addWidget(self.missile_params_frame, 0, 1, 2, 1)
        self.setCentralWidget(self.main_widget)

    def init_menubar(self):
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 26))
        self.menubar.setObjectName("menubar")
        self.config_menu = QtWidgets.QMenu(self.menubar)
        self.config_menu.setObjectName("config_menu")
        self.anim_menu = QtWidgets.QMenu(self.menubar)
        self.anim_menu.setObjectName("anim_menu")
        self.setMenuBar(self.menubar)

    def init_save_cfg_act(self):
        self.save_cfg_act = QtWidgets.QAction(self)
        self.save_cfg_act.setObjectName("save_cfg_act")
        self.save_cfg_act.triggered.connect(self.save_config)

    def init_load_cfg_act(self):
        self.load_cfg_act = QtWidgets.QAction(self)
        self.load_cfg_act.setObjectName("load_cfg_act")
        self.load_cfg_act.triggered.connect(self.load_config)

    def init_save_anim_act(self):
        self.save_anim_act = QtWidgets.QAction(self)
        self.save_anim_act.setObjectName("save_anim_act")
        self.save_anim_act.triggered.connect(self.save_animation)

    def add_menubar_actions(self):
        self.config_menu.addAction(self.save_cfg_act)
        self.config_menu.addAction(self.load_cfg_act)
        self.anim_menu.addAction(self.save_anim_act)
        self.menubar.addAction(self.config_menu.menuAction())
        self.menubar.addAction(self.anim_menu.menuAction())

    def read_inputs(self, name: str):
        return {
            "name": name,
            "mass": self.mass_input.value(),
            "drag_coefficient": self.drag_coeff_input.value(),
            "launch_angle": self.launch_angle_input.value(),
            "initial_thrust": self.init_thrust_input.value(),
            "thrust_duration": self.thrust_dur_input.value(),
            "max_simulation_time": self.simul_time_input.value(),
        }

    def add_missile(self):
        name = self.name_input.text()

        if name and name not in self.missiles_inst_dict.keys():
            config = self.read_inputs(name)
            missile = Missile(config)
            missile.simulate()
            self.missiles_inst_dict.update({name: missile})
            self.missiles_list.addItem(name)
            self.missiles_list.setCurrentText(name)

    def remove_missile(self):
        name = self.missiles_list.currentText()

        if name and name in self.missiles_inst_dict.keys():
            self.missiles_inst_dict.pop(name)
            self.missiles_list.removeItem(self.missiles_list.currentIndex())

    def animate_missiles(self):
        if self.animation_is_active():
            self.clear_animation()

        if self.missiles_count() > 0:
            show_legend = self.get_show_legend_state()

            if self.is_single_missile_animation():
                self.animate_single_missile(show_legend)

            else:
                self.animate_all_missiles(show_legend)

    def animate_all_missiles(self, show_legend):
        self.animation_widget.start_animation(
            self.missiles_inst_dict.values(), show_legend
        )
        self.result_table_widget.clear()
        for missile in self.missiles_inst_dict.values():
            self.add_missile_to_result_table(missile)

    def animate_single_missile(self, show_legend):
        name = self.get_name()
        if name and name in self.missiles_inst_dict.keys():
            self.animation_widget.start_animation(
                [self.missiles_inst_dict[name]], show_legend
            )
            self.result_table_widget.clear()
            self.add_missile_to_result_table(self.missiles_inst_dict[name])

    def save_config(self):
        name = self.get_name()
        if name and name in self.missiles_inst_dict.keys():
            self.missiles_inst_dict[name].save_config()

    def load_config(self):
        self.cfg_loader_widget = config_loader_widget(self)
        self.cfg_loader_widget.show()

    def save_animation(self):
        self.animation_widget.animation.save_animation()

    def randomize_missile_params(self):
        self.mass_input.setValue(randint(80, 750))
        self.drag_coeff_input.setValue(randint(1, 8))
        self.launch_angle_input.setValue(randint(50, 80))
        self.init_thrust_input.setValue(randint(4500, 10000))
        self.thrust_dur_input.setValue(randint(1, 8))
        self.simul_time_input.setValue(randint(50, 200))

    def reset_defaults(self):
        self.mass_input.setValue(100.0)
        self.drag_coeff_input.setValue(2.0)
        self.launch_angle_input.setValue(70.0)
        self.init_thrust_input.setValue(5000.0)
        self.thrust_dur_input.setValue(2.0)
        self.simul_time_input.setValue(100.0)

    def clear_animation(self):
        self.animation_widget.animation.ani.event_source.stop()
        self.animation_widget.ax.cla()
        self.animation_widget.animation.is_active = False

    def get_name(self):
        return self.missiles_list.currentText()

    def change_missile(self):
        name = self.get_name()
        if name and name in self.missiles_inst_dict.keys():
            missile = self.missiles_inst_dict[name]
            self.name_input.setText(name)
            self.mass_input.setValue(missile.mass)
            self.drag_coeff_input.setValue(missile.drag_coefficient)
            self.launch_angle_input.setValue(missile.launch_angle)
            self.init_thrust_input.setValue(missile.initial_thrust)
            self.thrust_dur_input.setValue(missile.thrust_duration)
            self.simul_time_input.setValue(missile.max_simulation_time)

    def is_single_missile_animation(self):
        return self.animate_single_missile_checkbox.isChecked()

    def get_show_legend_state(self):
        return self.show_legend_checkbox.isChecked()

    def missiles_count(self):
        return len(self.missiles_inst_dict.items())

    def animation_is_active(self):
        return self.animation_widget.animation.is_active

    def add_missile_to_result_table(self, missile):
        item = QtWidgets.QTreeWidgetItem()
        item.setText(0, missile.name)
        item.setText(1, str(round(missile.pos_array[-1, 0], 2)))
        item.setText(2, str(round(missile.vel_array[:, 0].max(), 2)))
        item.setText(3, str(round(missile.pos_array[:, 1].max(), 2)))
        item.setText(4, str(round(missile.boost_end_index * missile.dt, 2)))
        item.setText(
            5,
            str(
                round(
                    (missile.pos_array.shape[0] - missile.boost_end_index) * missile.dt,
                    2,
                )
            ),
        )
        item.setText(6, str(round(missile.pos_array.shape[0] * missile.dt, 2)))
        self.result_table_widget.addTopLevelItem(item)


class config_loader_widget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(config_loader_widget, self).__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("config_loader_widget")
        self.setMinimumSize(QtCore.QSize(350, 250))
        self.setMaximumSize(QtCore.QSize(500, 500))
        self.setBaseSize(QtCore.QSize(350, 450))
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.config_list_widget = QtWidgets.QListWidget(self)
        self.config_list_widget.setObjectName("config_list_widget")
        self.load_configs()
        self.gridLayout.addWidget(self.config_list_widget, 0, 0, 1, 1)
        self.dialog_btns_box = QtWidgets.QDialogButtonBox(self)
        self.dialog_btns_box.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok
        )
        self.dialog_btns_box.setObjectName("dialog_btns_box")
        self.dialog_btns_box.accepted.connect(self.select_config)
        self.dialog_btns_box.rejected.connect(self.close_window)
        self.gridLayout.addWidget(self.dialog_btns_box, 1, 0, 1, 1)

        self.retranslate_ui(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslate_ui(self, config_loader_widget):
        _translate = QtCore.QCoreApplication.translate
        config_loader_widget.setWindowTitle(
            _translate("config_loader_widget", "Select missile config")
        )

    def read_config_file(self):
        self.configs = []
        filename = "configs.csv"

        if os.path.isfile(filename):
            with open(filename, "r") as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    self.configs.append(row)

            return [row["name"] for row in self.configs]

    def load_configs(self):
        self.config_list_widget.clear()
        names = self.read_config_file()
        if names:
            self.config_list_widget.addItems(names)

    def select_config(self):
        if self.config_list_widget.currentRow() != -1:
            self.load_config()
        self.close_window()
        

    def close_window(self):
        self.close()

    def load_config(self):
        missile_cfg = self.configs[self.config_list_widget.currentRow()]
        self.parent().name_input.setText(missile_cfg["name"])
        self.parent().mass_input.setValue(float(missile_cfg["mass"]))
        self.parent().drag_coeff_input.setValue(float(missile_cfg["drag_coefficient"]))
        self.parent().launch_angle_input.setValue(float(missile_cfg["launch_angle"]))
        self.parent().init_thrust_input.setValue(float(missile_cfg["initial_thrust"]))
        self.parent().thrust_dur_input.setValue(float(missile_cfg["thrust_duration"]))
        self.parent().simul_time_input.setValue(
            float(missile_cfg["max_simulation_time"])
        )

        self.parent().add_missile()


def run_application():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MissileAnimationApp()
    main_window.show()
    sys.exit(app.exec_())
