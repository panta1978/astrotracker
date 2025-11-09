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
    QFileDialog, QMessageBox, QApplication
)
from PyQt6.QtCore import Qt
import importlib
import myastrolib as myal
import myastroplot as myap
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



# --- UPDATE PLOT ---
def update_plot(self):

    # Get parameters
    curr_obj = self.select_object.currentText()
    curr_location = self.select_location.currentText()
    curr_day = self.select_day.date().toString('yyyy-MM-dd')

    # Objects to be checked
    if curr_obj in self.ssobj:
        if curr_obj == 'SUN':
            sel_ssbodies = ['SUN']
        else:
            sel_ssbodies = ['SUN', curr_obj]
        sel_stars = []
        sel_stars_ra0 = []
        sel_stars_dec0 = []
        sel_stars_pm_ra = []
        sel_stars_pm_dec = []
    else:
        sel_ssbodies = ['SUN']
        sel_stars = [curr_obj]
        sel_star_ra0 = self.df_stars.loc[self.df_stars['star'] == curr_obj].iloc[0]['ra0']
        sel_stars_ra0 = [sel_star_ra0]
        sel_star_dec0 = self.df_stars.loc[self.df_stars['star'] == curr_obj].iloc[0]['dec0']
        sel_stars_dec0 = [sel_star_dec0]
        sel_star_pm_ra = self.df_stars.loc[self.df_stars['star'] == curr_obj].iloc[0]['pm_ra']
        sel_stars_pm_ra = [sel_star_pm_ra]
        sel_star_pm_dec = self.df_stars.loc[self.df_stars['star'] == curr_obj].iloc[0]['pm_dec']
        sel_stars_pm_dec = [sel_star_pm_dec]

    # Current position info
    row = self.df_loc.loc[self.df_loc['location'] == curr_location].iloc[0]
    lats = [row['latitude']]
    lons = [row['longitude']]
    tz_names = [row['time_zone']]

    # Time info
    sel_days = [curr_day]

    # Get Data
    self.df_out = myal.get_coords(
        sel_ssbodies = sel_ssbodies,
        sel_stars = sel_stars,
        stars_ra0 = sel_stars_ra0,
        stars_dec0 = sel_stars_dec0,
        stars_pm_ra = sel_stars_pm_ra,
        stars_pm_dec = sel_stars_pm_dec,
        loc_name= curr_location,
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
    myap.makeplot(self.df_out, curr_obj, curr_location, curr_day, plot_type, self)
    self.export_button.setEnabled(True)



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