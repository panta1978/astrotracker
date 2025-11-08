# --- ADD STARS UI ---

from PyQt6.QtWidgets import (
    QVBoxLayout, QLabel, QLineEdit, QPushButton, QDialog, QGridLayout
)
import importlib
import myastrolib as myal
import myastroplot as myap
from callbacks import add_stars_callbacks as ascb

importlib.reload(myal)
importlib.reload(myap)
importlib.reload(ascb)

# --- ADD STARS ---
class AddStarDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main = parent

        self.setWindowTitle('Add Star')
        self.setFixedWidth(500)

        layout = QVBoxLayout(self)

        # Init values
        self.starname = ''
        self.ra0 = ''
        self.dec0 = ''
        self.pm_ra = ''
        self.pm_dec = ''
        self.vizier_name = ''

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

        # --- Row 1: Star Name + Check
        grid.addWidget(QLabel('Star Name'), 0, 0, 1, 1)
        self.star_name_field = QLineEdit()
        grid.addWidget(self.star_name_field, 0, 1, 1, 4)

        self.check_btn = QPushButton('Check')
        self.check_btn.clicked.connect(lambda: ascb.check_star(self))
        grid.addWidget(self.check_btn, 0, 5, 1, 1)

        self.check_result_field = QLineEdit()
        self.check_result_field.setReadOnly(True)
        self.check_result_field.setStyleSheet('background-color: #e8e8e8; border: 1px solid #cccccc')
        grid.addWidget(self.check_result_field, 0, 6, 1, 1)

        # --- Row 2: RA / Dec ---
        grid.addWidget(QLabel('RA2000'), 1, 0, 1, 1)
        self.ra_field = QLineEdit()
        self.ra_field.setReadOnly(True)
        self.ra_field.setStyleSheet('background-color: #e8e8e8; border: 1px solid #cccccc')
        grid.addWidget(self.ra_field, 1, 1, 1, 2)

        grid.addWidget(QLabel('Dec2000'), 1, 4, 1, 1)
        self.dec_field = QLineEdit()
        self.dec_field.setReadOnly(True)
        self.dec_field.setStyleSheet('background-color: #e8e8e8; border: 1px solid #cccccc')
        grid.addWidget(self.dec_field, 1, 5, 1, 2)

        # --- Row 3: pm_ra / pm_dec ---
        grid.addWidget(QLabel('pm_ra'), 2, 0, 1, 1)
        self.pm_ra_field = QLineEdit()
        self.pm_ra_field.setReadOnly(True)
        self.pm_ra_field.setStyleSheet('background-color: #e8e8e8; border: 1px solid #cccccc')
        grid.addWidget(self.pm_ra_field, 2, 1, 1, 2)

        grid.addWidget(QLabel('pm_dec'), 2, 4, 1, 1)
        self.pm_dec_field = QLineEdit()
        self.pm_dec_field.setReadOnly(True)
        self.pm_dec_field.setStyleSheet('background-color: #e8e8e8; border: 1px solid #cccccc')
        grid.addWidget(self.pm_dec_field, 2, 5, 1, 2)

        # --- Row 4: Vizier Name and buttons ---
        grid.addWidget(QLabel('Vizier Name'), 3, 0)
        self.vizier_field = QLineEdit()
        self.vizier_field.setReadOnly(True)
        self.vizier_field.setStyleSheet('background-color: #e8e8e8; border: 1px solid #cccccc')
        grid.addWidget(self.vizier_field, 3, 1, 1, 2)

        self.update_btn = QPushButton('Update DB')
        self.update_btn.clicked.connect(lambda: ascb.update_db(self))
        self.update_btn.setEnabled(False)
        grid.addWidget(self.update_btn, 3, 5, 1, 1)
        self.close_btn = QPushButton('Close')
        self.close_btn.clicked.connect(self.close)
        grid.addWidget(self.close_btn, 3, 6, 1, 1)

