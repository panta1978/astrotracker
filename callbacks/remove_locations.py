# REMOVE LOCATIONS UI
import sqlite3
from PyQt6.QtWidgets import (
    QVBoxLayout, QPushButton, QSizePolicy,
    QHBoxLayout, QDialog, QCheckBox,
    QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt



def remove_locations(self):

    dialog = QDialog(self)
    dialog.setWindowTitle('Remove Locations')
    dialog.resize(400, 600)
    layout = QVBoxLayout(dialog)

    # Table with checkboxes
    table = QTableWidget()
    table.setRowCount(len(self.df_loc))
    table.setColumnCount(2)
    table.setHorizontalHeaderLabels(['Remove', 'Location'])
    for i, location in enumerate(self.df_loc['location']):
        # Checkbox
        checkbox = QCheckBox()
        table.setCellWidget(i, 0, checkbox)
        # Location name
        item = QTableWidgetItem(location)
        item.setFlags(Qt.ItemFlag.ItemIsEnabled)  # Not editable
        table.setItem(i, 1, item)
    table.setFixedWidth(370)
    table.setColumnWidth(0, 80)
    table.setColumnWidth(1, 280)

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
                location_name = table.item(row, 1).text()
                rows_to_remove.append(location_name)

        # Remove from DataFrame
        self.df_loc = self.df_loc[~self.df_loc['location'].isin(rows_to_remove)].reset_index(drop=True)

        # Update GUI
        self.select_location.clear()
        self.select_location.addItems(self.df_loc.location)
        if self.select_location.count() > 0:
            self.select_location.setCurrentIndex(0)

        # Update DB
        with sqlite3.connect(self.db_path) as conn:
            self.df_loc.to_sql('LOCATIONS', conn, if_exists='replace', index=False)

        dialog.accept()  # Close dialog

    def cancel():
        dialog.reject()

    remove_btn.clicked.connect(remove_selected)
    cancel_btn.clicked.connect(cancel)
    dialog.exec()
