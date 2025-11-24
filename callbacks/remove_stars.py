# MIT License
# Copyright (c) 2025 Stefano Pantaleoni
#
# This file is part of the Astrotracker project.
# See the LICENSE.txt file in the project root for full license information.

import sqlite3
from PyQt6.QtWidgets import (
    QVBoxLayout, QPushButton, QSizePolicy,
    QHBoxLayout, QDialog, QCheckBox,
    QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt


# --- REMOVE STARS FROM DB ---
def remove_stars(self):

    col_widths = [80, 160, 120, 80, 80, 80, 80]
    tot_width = sum(col_widths)

    dialog = QDialog(self)
    dialog.setWindowTitle('Remove Stars')
    dialog.resize(300, 600)
    layout = QVBoxLayout(dialog)

    # Table with checkboxes
    table = QTableWidget()
    table.setRowCount(len(self.df_stars))
    table.setColumnCount(8)
    table.setHorizontalHeaderLabels(
        ['Remove', 'Star', 'Vizier Name', 'RA', 'Dec', 'PM_RA', 'PM_DEC']
    )
    for i, star in self.df_stars.iterrows():
        # Checkbox
        checkbox = QCheckBox()
        table.setCellWidget(i, 0, checkbox)

        # Star info
        ni = 1
        for col in ['star', 'vizier_name', 'ra0', 'dec0', 'pm_ra', 'pm_dec']:
            if type(star[col]) == str:
                item = QTableWidgetItem(star[col])
            else:
                item = QTableWidgetItem(str(star[col]))
            item.setFlags(Qt.ItemFlag.ItemIsEnabled)  # Not editable
            table.setItem(i, ni, item)
            ni += 1

    table.setFixedWidth(tot_width + 40)
    for n, w in enumerate(col_widths):
        table.setColumnWidth(n, w)

    layout.addWidget(table)

    # --- Buttons ---
    button_layout = QHBoxLayout()
    cancel_btn = QPushButton('Cancel')
    cancel_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    remove_btn = QPushButton('Remove Selected')
    remove_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    button_layout.addWidget(cancel_btn)
    button_layout.addWidget(remove_btn)
    layout.addLayout(button_layout)

    def remove_selected():

        # Ask for confirmation before deleting stars
        reply = QMessageBox.question(
            None,
            'Confirm Deletion',
            'Selected stars will be deleted. Are you sure?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.No:
            return

        rows_to_remove = []
        for row in range(table.rowCount()):
            chk = table.cellWidget(row, 0)
            if chk.isChecked():
                star_name = table.item(row, 1).text()
                rows_to_remove.append(star_name)

        # Remove from DataFrame
        self.df_stars = self.df_stars[~self.df_stars['star'].isin(rows_to_remove)].reset_index(drop=True)

        # Update GUI
        self.select_object.clear()
        self.select_object.addItems(self.ssobj + self.df_stars.star.tolist())
        if self.select_object.count() > 0:
            self.select_object.setCurrentIndex(0)

        # Update DB
        with sqlite3.connect(self.db_path) as conn:
            self.df_stars.to_sql('STARS', conn, if_exists='replace', index=False)

        dialog.accept()  # Close dialog

    def cancel():
        dialog.reject()

    remove_btn.clicked.connect(remove_selected)
    cancel_btn.clicked.connect(cancel)
    dialog.exec()

