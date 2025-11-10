# MIT License
# Copyright (c) 2025 Stefano Pantaleoni
#
# This file is part of the Astrotracker project.
# See the LICENSE.txt file in the project root for full license information.

# --- CALLBACKS USED BY MAIN FILE ---

import os
import pandas as pd
import sqlite3
from PyQt6.QtWidgets import (
    QFileDialog, QMessageBox, QComboBox, QDateEdit
)
from PyQt6.QtCore import QDate
import importlib
import myastrolib as myal
import myastroplot as myap
import myastroplot_multi as myapm
from callbacks import add_stars
from callbacks import add_locations
from callbacks import remove_stars
from callbacks import remove_locations

importlib.reload(myal)
importlib.reload(myap)
importlib.reload(add_stars)
importlib.reload(add_locations)
importlib.reload(remove_stars)
importlib.reload(remove_locations)



# --- INIT ---
def init_data(self):

    # Recreate DB if it does not exist
    self.db_path = 'astrodb.db'
    if not(os.path.exists(self.db_path)):
        sql_file = 'db_backup.sql'
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            with open(sql_file, 'r', encoding='utf-8') as f:
                sql_script = f.read()
            cursor.executescript(sql_script)
            conn.commit()

    # Init Data
    with sqlite3.connect(self.db_path) as conn:
        self.df_loc = pd.read_sql_query('SELECT * FROM LOCATIONS ORDER BY location', conn)
        self.df_stars = pd.read_sql_query('SELECT * FROM STARS ORDER BY star', conn)
    self.ssobj = ['SUN', 'MOON', 'MERCURY', 'VENUS', 'MARS', 'JUPITER', 'SATURN']
    self.df_out = []
    self.sel_time = 'Civil'



# --- TIME TYPE (CIVIL, LOCAL, GREENWICH) ---
def set_time_type(self, curr_label):
    # Make selected one checked, others unchecked
    for label, act in self.actions.items():
        act.setChecked(label == curr_label)
        self.sel_time = curr_label
    self.recalc = True



# --- UPDATE PLOT ---
def update_plot(self):

    # Mode Type
    multi_mode = self.selmultidata.currentText()

    # Get parameters (single mode)
    curr_obj = self.select_object.currentText()
    curr_location = self.select_location.currentText()
    curr_day = self.select_day.date().toString('yyyy-MM-dd')

    # Get parameters (multiple mode)
    multi_values = []
    for row in range(self.multitable.rowCount()):
        combo = self.multitable.cellWidget(row, 0)  # get the QComboBox
        if combo is not None:
            if multi_mode == 'Multi Days':
                multi_values.append(combo.date().toString('yyyy-MM-dd'))
            else:
                multi_values.append(combo.currentText())  # get the selected text

    # Objects to be checked
    if multi_mode == 'Multi Objects':
        sel_ssbodies = [m for m in multi_values if m in self.ssobj]
        sel_stars = [m for m in multi_values if m not in self.ssobj]
    else:
        if curr_obj in self.ssobj:
            if curr_obj == 'SUN':
                sel_ssbodies = ['SUN']
            else:
                sel_ssbodies = ['SUN', curr_obj]
            sel_stars = []
        else:
            sel_ssbodies = ['SUN']
            sel_stars = [curr_obj]

    sel_stars_ra0 = [] ; sel_stars_dec0 = []
    sel_stars_pm_ra = [] ; sel_stars_pm_dec = []
    for sel_star in sel_stars:
        curr_rec = self.df_stars.loc[self.df_stars['star'] == sel_star].iloc[0]
        sel_stars_ra0.append(curr_rec['ra0'])
        sel_stars_dec0.append(curr_rec['dec0'])
        sel_stars_pm_ra.append(curr_rec['pm_ra'])
        sel_stars_pm_dec.append(curr_rec['pm_dec'])

    # Current position info
    if multi_mode == 'Multi Locations':
        sel_locations = multi_values
    else:
        sel_locations = [curr_location]
    lats = [] ; lons = [] ; tz_names = []
    for sel_location in sel_locations:
        row = self.df_loc.loc[self.df_loc['location'] == sel_location].iloc[0]
        lats.append(row['latitude'])
        lons.append(row['longitude'])
        tz_names.append(row['time_zone'])

    # Time info
    if multi_mode == 'Multi Days':
        sel_days = multi_values
    else:
        sel_days = [curr_day]

    # Get Data
    if self.recalc:
        self.df_out = myal.get_coords(
            sel_ssbodies = sel_ssbodies,
            sel_stars = sel_stars,
            stars_ra0 = sel_stars_ra0,
            stars_dec0 = sel_stars_dec0,
            stars_pm_ra = sel_stars_pm_ra,
            stars_pm_dec = sel_stars_pm_dec,
            loc_names= sel_locations,
            lats = lats,
            lons = lons,
            tz_names = tz_names,
            sel_time = self.sel_time,
            sel_days = sel_days,
            t_min = self.tmin.time().toString('HH:mm') if self.tminmaxsel.isChecked() else '00:00',
            t_max = self.tmax.time().toString('HH:mm') if self.tminmaxsel.isChecked() else '00:00',
            t_delta = self.tdelta.value()
    )

    # Create Graph
    plot_type = self.select_graph.currentText()
    if multi_mode == 'Single Data':
        myap.makeplot_single(self.df_out, curr_obj, curr_location, curr_day, plot_type, self)
    else:
        myapm.makeplot_multi(self.df_out, curr_obj, curr_location, curr_day, plot_type, multi_mode, multi_values, self)
    self.export_button.setEnabled(True)
    self.recalc = False # If no input parameter changes, do not recalculate objects' positions



# --- TIME STEP CHANGED
def change_objparam(self):
    self.recalc = True



# --- MULTI DATA SELECTION
def selmultidata(self):

    # Mode Type
    multi_mode = self.selmultidata.currentText()

    # Enable multitable and upper buttons
    enabs = [True, True, True, True]
    if multi_mode == 'Single Data':
        enabs[0] = False
        multi_options = []
    if multi_mode == 'Multi Objects':
        enabs[1] = False
        multi_options = self.ssobj + self.df_stars.star.tolist()
    if multi_mode == 'Multi Locations':
        enabs[2] = False
        multi_options = self.df_loc.location.tolist()
    if multi_mode == 'Multi Days':
        enabs[3] = False
        multi_options = []
    self.multitable.setEnabled(enabs[0])
    self.select_object.setEnabled(enabs[1])
    self.select_location.setEnabled(enabs[2])
    self.select_day.setEnabled(enabs[3])

    # Adjust number of rows
    self.multitable.clearContents()
    self.multitable.setRowCount(self.nrows.value())

    # Set Table options (cases: Objects / Locations)
    if multi_mode in ['Multi Objects', 'Multi Locations']:
        ni = 0
        for row in range(self.nrows.value()):
            combo = QComboBox()
            combo.addItems(multi_options)
            combo.setCurrentIndex(ni)  # default to empty
            combo.currentIndexChanged.connect(lambda index, r=row: change_objparam(self))
            combo.setMinimumHeight(24)  # makes it look better
            self.multitable.setCellWidget(row, 0, combo)
            ni += 1

    # Set Table options (cases: Objects / Locations)
    if multi_mode == 'Multi Days':
        ni = 0
        for row in range(self.nrows.value()):
            dateedit = QDateEdit()
            dateedit.setDisplayFormat('dd/MM/yyyy')
            dateedit.setDate(QDate.currentDate().addDays(ni))
            dateedit.setCalendarPopup(True)
            dateedit.dateChanged.connect(lambda index, r=row: change_objparam(self))
            dateedit.setMinimumHeight(24)
            self.multitable.setCellWidget(row, 0, dateedit)
            ni += 1

    self.recalc = True



# ---  EXPORT DATA ---
def export_data(self):

    file_path, _ = QFileDialog.getSaveFileName(
        self, 'Save CSV File', '', 'CSV Files (*.csv);;All Files (*)'
    )
    if not file_path:
        return

    try:
        # Ensure it ends with .csv
        if not file_path.lower().endswith('.csv'):
            file_path += '.csv'

        # Save the DataFrame
        self.df_out.to_csv(file_path, sep=';', index=False)
        QMessageBox.information(self, 'Success', f'File saved as:\n{file_path}')

    except Exception as e:
        QMessageBox.critical(self, 'Error', f'Could not save file:\n{str(e)}')



# --- SELECT / UNSELECT MIN/MAX TIME
def tminmaxsel(self):
    is_chk = self.tminmaxsel.isChecked()
    self.tmin.setEnabled(is_chk)
    self.tmax.setEnabled(is_chk)
    self.recalc = True



# --- ADD STARS ---
def call_add_stars(window):
    dlg = add_stars.AddStarDialog(window)
    dlg.exec()



# --- REMOVE STARS ---
def call_remove_stars(self):
    remove_stars.remove_stars(self)



# --- ADD LOCATIONS ---
def call_add_locations(window):
    dlg = add_locations.AddLocationDialog(window)
    dlg.exec()



# --- REMOVE LOCATIONS ---
def call_remove_locations(self):
    remove_locations.remove_locations(self)



# --- ABOUT DIALOG ---
def show_about_dialog(self):
    text = (
            '<b>Astrotracker</b><br>'
            f'Version {self.ver}<br><br>'
            'A Python-based tool for astronomical event tracking and visualisation.<br><br>'
            '<b>License:</b><br>'
            'MIT License<br>'
            'Copyright (c) 2025 Stefano Pantaleoni<br><br>'
            'See LICENSE.txt for full details.'
        )
    QMessageBox.about(self, 'About Astrotracker', text)
    