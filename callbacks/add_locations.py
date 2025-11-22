# MIT License
# Copyright (c) 2025 Stefano Pantaleoni
#
# This file is part of the Astrotracker project.
# See the LICENSE.txt file in the project root for full license information.

# --- ADD LOCATIONS UI ---

from PyQt6.QtWidgets import (
    QVBoxLayout, QLabel, QLineEdit, QPushButton, QDialog, QGridLayout
)
import importlib
import myastrolib as myal
import myastroplot as myap
from callbacks import add_locations_callbacks as alcb

importlib.reload(myal)
importlib.reload(myap)
importlib.reload(alcb)

# --- ADD LOCATIONS ---
class AddLocationDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main = parent

        self.setWindowTitle('Add Location')
        self.setFixedWidth(500)

        layout = QVBoxLayout(self)

        # Init values
        self.locationname = ''
        self.lat = ''
        self.lon = ''
        self.time_zone = ''
        self.civil_utc = ''
        self.local_utc = ''

        # --- Create Grid ---
        grid = QGridLayout()
        grid.setColumnStretch(0, 2)
        grid.setColumnStretch(1, 2)
        grid.setColumnStretch(2, 2)
        grid.setColumnStretch(3, 1)
        grid.setColumnStretch(4, 2)
        grid.setColumnStretch(5, 2)
        grid.setColumnStretch(6, 2)
        layout.addLayout(grid)

        # --- Row 0: Label
        descr_label = 'Search for a location (e.g. <b>Vancouver, Canada</b>), or lat/lon (e.g. <b>29.9792, 31.1343</b>)'
        grid.addWidget(QLabel(descr_label), 0, 0, 1, 7)

        # --- Row 1: Location Name + Check
        grid.addWidget(QLabel('Location Name'), 1, 0, 1, 1)
        self.location_name_field = QLineEdit()
        grid.addWidget(self.location_name_field, 1, 1, 1, 4)

        self.check_btn = QPushButton('Check')
        self.check_btn.clicked.connect(lambda: alcb.check_location(self))
        grid.addWidget(self.check_btn, 1, 5, 1, 1)

        self.check_result_field = QLineEdit()
        self.check_result_field.setReadOnly(True)
        self.check_result_field.setStyleSheet('background-color: #e8e8e8; border: 1px solid #cccccc')
        grid.addWidget(self.check_result_field, 1, 6, 1, 1)

        # --- Row 2: Lat / Lon ---
        grid.addWidget(QLabel('Latitude'), 2, 0, 1, 1)
        self.lat_field = QLineEdit()
        self.lat_field.setReadOnly(True)
        self.lat_field.setStyleSheet('background-color: #e8e8e8; border: 1px solid #cccccc')
        grid.addWidget(self.lat_field, 2, 1, 1, 2)

        grid.addWidget(QLabel('Longitude'), 2, 4, 1, 1)
        self.lon_field = QLineEdit()
        self.lon_field.setReadOnly(True)
        self.lon_field.setStyleSheet('background-color: #e8e8e8; border: 1px solid #cccccc')
        grid.addWidget(self.lon_field, 2, 5, 1, 2)

        # --- Row 3: UTC ---
        grid.addWidget(QLabel('Civil UTC'), 3, 0, 1, 1)
        self.civilutc_field = QLineEdit()
        self.civilutc_field.setReadOnly(True)
        self.civilutc_field.setStyleSheet('background-color: #e8e8e8; border: 1px solid #cccccc')
        grid.addWidget(self.civilutc_field, 3, 1, 1, 2)

        grid.addWidget(QLabel('Local UTC'), 3, 4, 1, 1)
        self.localutc_field = QLineEdit()
        self.localutc_field.setReadOnly(True)
        self.localutc_field.setStyleSheet('background-color: #e8e8e8; border: 1px solid #cccccc')
        grid.addWidget(self.localutc_field, 3, 5, 1, 2)

        # --- Row 4: Time Zone name and buttons ---
        grid.addWidget(QLabel('Time Zone'), 4, 0)
        self.timezone_field = QLineEdit()
        self.timezone_field.setReadOnly(True)
        self.timezone_field.setStyleSheet('background-color: #e8e8e8; border: 1px solid #cccccc')
        grid.addWidget(self.timezone_field, 4, 1, 1, 2)

        self.update_btn = QPushButton('Update DB')
        self.update_btn.clicked.connect(lambda: alcb.update_db(self))
        self.update_btn.setEnabled(False)
        grid.addWidget(self.update_btn, 4, 5, 1, 1)
        self.close_btn = QPushButton('Close')
        self.close_btn.clicked.connect(self.close)
        grid.addWidget(self.close_btn, 4, 6, 1, 1)

