# MIT License
# Copyright (c) 2025 Stefano Pantaleoni
#
# This file is part of the Astrotracker project.
# See the LICENSE.txt file in the project root for full license information.

import sys
from functools import partial
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox,
    QPushButton, QSpacerItem, QSizePolicy, QHBoxLayout, QDateEdit, QCheckBox, QTimeEdit, QSpinBox
)
from PyQt6.QtGui import QAction
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt, QDate, QTimer, QTime
import importlib
import myastrolib as myal
import myastroplot as myap
from callbacks import callbacks as cb

importlib.reload(myal)
importlib.reload(myap)
importlib.reload(cb)


class MainWindow(QMainWindow):


    # --- MAIN WINDOW ---
    def __init__(self):
        ssobj: list[str]
        df_stars: pd.DataFrame
        df_loc: pd.DataFrame
        df_out: pd.DataFrame
        sel_time: str

        # Window Setup
        super().__init__()
        self.setWindowTitle('Astrotracker')
        cb.init_data(self)
        QTimer.singleShot(0, self.showMaximized)

        # Central Widget / Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)


        # --- TOP ROW ---
        top_row = QHBoxLayout()

        # Object Selection
        label_object = QLabel('Object:')
        label_object.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        top_row.addWidget(label_object)

        self.select_object = QComboBox()
        self.select_object.addItems(self.ssobj + self.df_stars.star.tolist())
        self.select_object.setFixedWidth(150)
        top_row.addWidget(self.select_object)
        top_row.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum))

        # Location Selection
        label_location = QLabel('Location:')
        label_location.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        top_row.addWidget(label_location)

        self.select_location = QComboBox()
        self.select_location.addItems(self.df_loc.location)
        self.select_location.setFixedWidth(250)
        top_row.addWidget(self.select_location)
        top_row.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum))

        # Day Selection
        label_day = QLabel('Day:')
        label_day.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        top_row.addWidget(label_day)

        self.select_day = QDateEdit()
        self.select_day.setDate(QDate.currentDate())
        self.select_day.setMinimumDate(QDate(1900, 1, 1))
        self.select_day.setMaximumDate(QDate(2100, 12, 31))
        self.select_day.setCalendarPopup(True)
        top_row.addWidget(self.select_day)
        top_row.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum))

        # Graph Selection
        label_graph = QLabel('Graph Type:')
        label_graph.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        top_row.addWidget(label_graph)

        self.select_graph = QComboBox()
        self.select_graph.addItems([
            'Azimuth/Altidude',
            'Azimuth/Altidude (Polar)',
            'Equatorial',
            'Equatorial (Polar, North)',
            'Equatorial (Polar, South)'
        ])
        self.select_graph.setFixedWidth(200)
        top_row.addWidget(self.select_graph)
        top_row.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding))


        # Top Row Container
        container_top_row = QWidget()
        container_top_row.setLayout(top_row)
        container_top_row.setFixedHeight(40)
        container_top_row.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container_top_row)


        # --- MAIN ROW ---
        main_row = QHBoxLayout()

        # Plotly Graph View
        self.webview = QWebEngineView()
        main_row.addWidget(self.webview)

        # Side Menu
        sidemenu = QVBoxLayout()
        sidemenu.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Graph Options Label
        label_graphopts = QLabel('Graph Options:')
        label_graphopts.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        sidemenu.addWidget(label_graphopts)

        # Day/Night Filter
        self.daynight = QComboBox()
        self.daynight.addItems(['Day and Night', 'Night Only', 'Day Only'])
        self.daynight.setFixedWidth(150)
        sidemenu.addWidget(self.daynight)

        # Horizon Filter
        self.horizonview = QComboBox()
        self.horizonview.addItems(['All positions', 'Above Horizon'])
        self.horizonview.setFixedWidth(150)
        sidemenu.addWidget(self.horizonview)
        sidemenu.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum))

        # Graph Options Label
        label_eqpolar = QLabel('Equatorial Polar Graphs:')
        label_eqpolar.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        sidemenu.addWidget(label_eqpolar)

        # Halph hemisphere for polar equatorial graphs
        self.halfhemisphere = QCheckBox('Half Hemisphere')
        self.halfhemisphere.setFixedWidth(150)
        sidemenu.addWidget(self.halfhemisphere)
        sidemenu.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum))

        # Time MIN / MAX selection
        self.tminmaxsel = QCheckBox('Set Time min / max')
        self.tminmaxsel.setFixedWidth(150)
        self.tminmaxsel.clicked.connect(lambda: cb.tminmaxsel(self))
        sidemenu.addWidget(self.tminmaxsel)

        # Time MIN / MAX Layout
        tminmax = QHBoxLayout()
        tminmax.setContentsMargins(0, 0, 0, 0)
        self.tmin = QTimeEdit()
        self.tmin.setDisplayFormat('HH:mm')
        self.tmin.setEnabled(False)
        self.tmin.setFixedWidth(80)
        self.tmin.setTime(QTime(0, 0))
        tminmax.addWidget(self.tmin)
        label_tminmax = QLabel('-')
        tminmax.addWidget(label_tminmax)
        self.tmax = QTimeEdit()
        self.tmax.setDisplayFormat('HH:mm')
        self.tmax.setEnabled(False)
        self.tmax.setFixedWidth(80)
        self.tmax.setTime(QTime(0, 0))
        tminmax.addWidget(self.tmax)
        tminmax.addSpacerItem(QSpacerItem(5, 5, QSizePolicy.Policy.Expanding))
        tminmax_widget = QWidget()
        tminmax_widget.setLayout(tminmax)
        sidemenu.addWidget(tminmax_widget)

        # Time Step Layout
        tdelta = QHBoxLayout()
        tdelta.setContentsMargins(0, 0, 0, 0)
        label_tdelta = QLabel('Time step [min]')
        tdelta.addWidget(label_tdelta)
        self.tdelta = QSpinBox()
        self.tdelta.setRange(1, 15)
        self.tdelta.setSingleStep(1)  # increment/decrement by 5
        self.tdelta.setValue(5)
        tdelta.addWidget(self.tdelta)
        tdelta.addSpacerItem(QSpacerItem(5, 5, QSizePolicy.Policy.Expanding))
        tdelta_widget = QWidget()
        tdelta_widget.setLayout(tdelta)
        sidemenu.addWidget(tdelta_widget)
        sidemenu.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum))

        # Button Styles
        style_button = """
            QPushButton {
                color: darkred;
                font-size: 10pt;
                font-weight: bold;
            }
        """

        # Run Button
        self.run_button = QPushButton('RUN')
        self.run_button.clicked.connect(lambda: cb.update_plot(self))
        self.run_button.setFixedWidth(120)
        self.run_button.setStyleSheet(style_button)
        sidemenu.addWidget(self.run_button)

        # Export Button
        self.export_button = QPushButton('EXPORT')
        self.export_button.setEnabled(False)
        self.export_button.clicked.connect(lambda: cb.export_data(self))
        self.export_button.setFixedWidth(120)
        self.export_button.setStyleSheet(style_button)
        sidemenu.addWidget(self.export_button)
        sidemenu.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum))

        # Side Menu Container
        sidemenu_widget = QWidget()
        sidemenu_widget.setFixedWidth(200)
        sidemenu_widget.setLayout(sidemenu)
        main_row.addWidget(sidemenu_widget)

        # Main Row Container
        container_main_row = QWidget()
        container_main_row.setLayout(main_row)
        main_layout.addWidget(container_main_row)


        # --- MENUS ---
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {spacing: 4px;}
            QMenuBar::item {padding: 2px 6px; margin: 0px;}
        """)

        # Time Type Menu
        time_menu = menubar.addMenu('Time Type')
        self.actions = {}
        for label in ['Civil', 'Local', 'Greenwich']:
            action = QAction(label, self, checkable=True)
            action.triggered.connect(partial(cb.set_time_type, self, label))
            time_menu.addAction(action)
            self.actions[label] = action
        self.actions['Civil'].setChecked(True)

        # Stars Menu
        star_menu = menubar.addMenu('Stars')
        star_add = QAction('Add Stars', self)
        star_add.triggered.connect(lambda: cb.call_add_stars(self))
        star_menu.addAction(star_add)
        star_remove = QAction('Remove Stars', self)
        star_remove.triggered.connect(lambda: cb.call_remove_stars(self))
        star_menu.addAction(star_remove)

        # Locations Menu
        loc_menu = menubar.addMenu('Locations')
        loc_add = QAction('Add Locations', self)
        loc_add.triggered.connect(lambda: cb.call_add_locations(self))
        loc_menu.addAction(loc_add)
        loc_remove = QAction('Remove Locations', self)
        loc_remove.triggered.connect(lambda: cb.call_remove_locations(self))
        loc_menu.addAction(loc_remove)

        # Initial Plot
        cb.update_plot(self)


# --- MAIN APP EXECUTION ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
