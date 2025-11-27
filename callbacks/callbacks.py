# MIT License
# Copyright (c) 2025 Stefano Pantaleoni
#
# This file is part of the Astrotracker project.
# See the LICENSE.txt file in the project root for full license information.

# --- CALLBACKS USED BY MAIN FILE ---

import os
import sys
import re
import yaml
from datetime import datetime
import shutil
import pandas as pd
import sqlite3
from pathlib import Path
from PyQt6.QtWidgets import (
    QFileDialog, QMessageBox, QComboBox, QDateEdit
)
from PyQt6.QtCore import QDate, QSize
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QPixmap, QPainter, QColor, QIcon
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


# --- DB Path ---
def resource_path(relative_path):
        try: # Compiled Version
            base_path = sys._MEIPASS
        except AttributeError: # Developer mode
            base_path = os.path.abspath('.')
        return os.path.join(base_path, relative_path)


# --- Read DB Routine ---
def read_db(self):
    with sqlite3.connect(self.db_path) as conn:
        self.df_loc = pd.read_sql_query(
            'SELECT * FROM LOCATIONS ORDER BY location', conn
        )
        self.df_stars = pd.read_sql_query(
            'SELECT * FROM STARS ORDER BY star', conn
        )


# --- Restore DB Routine ---
def restore_db(self):
    sql_file = resource_path('db_backup.sql')
    with sqlite3.connect(self.db_path) as conn:
        cursor = conn.cursor()
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        cursor.executescript(sql_script)


# --- INIT ---
def init_data(self):

    # Recreate App path if it does not exist
    if os.name == 'nt':
        app_dir = Path(os.getenv('LOCALAPPDATA')) / 'Astrotracker'
    else:
        app_dir = Path.home() / '.Astrotracker'
    app_dir.mkdir(parents=True, exist_ok=True)

    # Recreate DB if it does not exist or if it is faulty
    self.db_path = app_dir / 'astrodb.db'
    if not(os.path.exists(self.db_path)):
        restore_db(self)
        read_db(self)
    else:
        try:
            read_db(self)
        except:
            if os.path.exists(self.db_path):
                os.remove(self.db_path)
            restore_db(self)
            read_db(self)

    # Other parameters
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


# --- Get Multi Values Routine ---
def get_multi_values(multi_mode, removeduplicates, self):
    multi_values = []
    for row in range(self.multitable.rowCount()):
        combo = self.multitable.cellWidget(row, 0)  # get the QComboBox
        if combo is not None:
            if multi_mode == 'Multi Days':
                multi_values.append(combo.date())
            else:
                multi_values.append(combo.currentText())  # get the selected text
    if removeduplicates:
        multi_values = list(dict.fromkeys(multi_values))
    return multi_values


# --- UPDATE PLOT ---
def update_plot(self):

    # Mode Type
    multi_mode = self.selmultidata.currentText()

    # Get parameters (single mode)
    curr_obj = self.select_object.currentText()
    curr_location = self.select_location.currentText()
    curr_day = self.select_day.date().toString('yyyy-MM-dd')

    # Get parameters (multiple mode)
    multi_values = get_multi_values(multi_mode=multi_mode, removeduplicates=True, self=self)

    # Objects to be checked
    if multi_mode == 'Multi Objects':
        sel_ssbodies = [m for m in multi_values if m in self.ssobj]
        if not 'SUN' in sel_ssbodies:
            sel_ssbodies = ['SUN'] + sel_ssbodies
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
        multi_values = [m.toString('yyyy-MM-dd') for m in multi_values]
        multi_values = list(dict.fromkeys(multi_values))
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
        myap.makeplot_multi(self.df_out, curr_obj, curr_location, curr_day, plot_type, multi_mode, multi_values, self)
    self.recalc = False # If no input parameter changes, do not recalculate objects' positions

    def sanitise_obj_loc(str0):
        str1 = re.sub(r'[^A-Za-z0-9]+', '_', str0)
        str2 = str1.strip('_')
        return str2

    # Save parameters (for default file names)
    self.multi_mode = multi_mode
    self.curr_obj = sanitise_obj_loc(curr_obj)
    self.curr_location = sanitise_obj_loc(curr_location)
    self.curr_day = curr_day.replace('-','_')

    # Adjust for multi mode
    if multi_mode == 'Multi Objects': self.curr_obj = 'MULTI_OBJ'
    if multi_mode == 'Multi Locations': self.curr_location = 'MULTI_LOC'
    if multi_mode == 'Multi Days': curr_day = 'MULTI_DAY'

    match self.select_graph.currentText():
        case 'Azimuth/Altidude':
            self.curr_graph = 'AzAlt'
        case 'Azimuth/Altidude (Polar)':
            self.curr_graph = 'AzAlt_Polar'
        case 'Equatorial':
            self.curr_graph = 'Equatorial'
        case 'Equatorial (Polar, North)':
            self.curr_graph = 'Equatorial_Polar_N'
        case 'Equatorial (Polar, South)':
            self.curr_graph = 'Equatorial_Polar_S'


# --- TIME STEP CHANGED ---
def change_objparam(self):
    self.recalc = True


# --- MULTI DATA SELECTION ---
def selmultidata(self):

    # Mode Type
    multi_mode = self.selmultidata.currentText()
    # Enable / Disable multitable and upper buttons
    enabs = [True, True, True, True, True]
    if multi_mode == 'Single Data':
        enabs[0] = False
        enabs[4] = False
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
    self.multidata_menu.setEnabled(enabs[4])

    # Enable / Disable other controls
    if multi_mode == 'Single Data':
        self.selcolour.setEnabled(False)
        self.nrows.setEnabled(False)
    else:
        self.selcolour.setEnabled(True)
        self.nrows.setEnabled(True)

    # Table Rows
    n_rows = self.multitable.rowCount()
    n_rows_target = self.nrows.value()
    if n_rows_target != n_rows: # Only makes sense if nr of object has changed
        multi_values = get_multi_values(multi_mode=multi_mode, removeduplicates=False, self=self)

    # Manage Table
    if multi_mode in ['Multi Objects', 'Multi Locations']:
        if n_rows_target < n_rows:
            multi_values = multi_values[:n_rows_target]
        elif n_rows_target > n_rows:
            nsel = [min(n, len(multi_options)-1) for n in range(n_rows, n_rows_target)] # Cap nsel to prevent overflows
            multi_values = multi_values + [multi_options[i] for i in nsel]
        else:
            nsel = [min(n, len(multi_options)-1) for n in range(0, n_rows_target)] # Cap nsel to prevent overflows
            multi_values = [multi_options[i] for i in nsel]
    elif multi_mode == 'Multi Days':
        if n_rows_target < n_rows:
            multi_values = multi_values[:n_rows_target]
        elif n_rows_target > n_rows:
            multi_values = (multi_values +
                [myap.capdate(multi_values[-1].addDays(i+1), self.day_min, self.day_max)
                for i in range(n_rows_target-n_rows)])
        else:
            multi_values = [
                myap.capdate(QDate.currentDate().addDays(i), self.day_min, self.day_max)
                for i in range(n_rows_target)
            ]

    # Adjust number of rows
    self.multitable.clearContents()
    self.multitable.setRowCount(self.nrows.value())

    # Set Table options (cases: Objects / Locations)
    if multi_mode in ['Multi Objects', 'Multi Locations']:
        ni = 0
        for row in range(self.nrows.value()):
            combo = QComboBox()
            combo.addItems(multi_options)
            try:
                nj = multi_options.index(multi_values[ni])
            except:
                nj = ni
            combo.setCurrentIndex(nj)
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
            dateedit.setDate(multi_values[ni])
            dateedit.setMinimumDate(self.day_min)
            dateedit.setMaximumDate(self.day_max)
            dateedit.setCalendarPopup(True)
            dateedit.dateChanged.connect(lambda index, r=row: change_objparam(self))
            dateedit.setMinimumHeight(24)
            self.multitable.setCellWidget(row, 0, dateedit)
            ni += 1

    self.recalc = True


# ---  EXPORT DATA ---
def export(self, format):

    # Default file name
    if format == 'csv':
        file_name = f'{self.curr_obj}-{self.curr_location}-{self.curr_day}'
    else:
        file_name = f'{self.curr_obj}-{self.curr_location}-{self.curr_day}-{self.curr_graph}'

    format_up = format.upper()
    file_path, _ = QFileDialog.getSaveFileName(
        self, f'Save {format_up} File', f'{file_name}.{format}', f'{format_up} Files (*.{format})'
    )
    if not file_path:
        return

    try:
        # Ensure it ends with .csv / png
        if not file_path.lower().endswith(f'.{format}'):
            file_path += f'.{format}'

        if format == 'csv': # Save the DataFrame
            self.df_out.to_csv(file_path, sep=';', index=False)
        elif format == 'png': # Export Figure
            self.fig.write_image(file_path)

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
def call_add_stars(self):
    dlg = add_stars.AddStarDialog(self)
    dlg.exec()


# --- REMOVE STARS ---
def call_remove_stars(self):
    remove_stars.remove_stars(self)


# --- ADD LOCATIONS ---
def call_add_locations(self):
    dlg = add_locations.AddLocationDialog(self)
    dlg.exec()


# --- REMOVE LOCATIONS ---
def call_remove_locations(self):
    remove_locations.remove_locations(self)


# --- ABOUT DIALOG ---
def show_errorlog(self, get_base_path):
    base_path = get_base_path()
    log_path = os.path.join(base_path, 'astrotracker_error.log')
    if os.path.exists(log_path):
        try:
            os.startfile(log_path)  # Opens with default app (Notepad, etc.)
        except:
            QMessageBox.critical(
            self,
            'Unable to Open File',
            f'astrotracker_error.log file could not be opened.'
        )
    else:
        QMessageBox.critical(
            self,
            'Unable to Find File',
            f'astrotracker_error.log does not exist.'
        )


# --- ABOUT DIALOG ---
def show_about_dialog(self, get_base_path):
    base_path = get_base_path()
    lic_path = os.path.join(base_path, 'LICENSE.txt')
    text = (
            '<b>Astrotracker</b><br>'
            f'Version {self.ver}<br><br>'
            'A Python-based tool for astronomical event tracking and visualisation.<br><br>'
            '<b>Author:</b><br>'
            'Stefano Pantaleoni (stefano.pantaleoni@gmail.com)<br><br>'
            '<b>License:</b><br>'
            'MIT License<br>'
            'Copyright (c) 2025 Stefano Pantaleoni<br><br>'
            f'See <a href="file:///{lic_path}">LICENSE.txt</a> for full details.'
        )
    QMessageBox.about(self, 'About Astrotracker', text)


# Colour icon
def make_colour_icon(colours, width, height, max_cols=12):
    """Create a horizontal colour bar icon from a list of colour hex strings."""

    def rgb_to_hex(s):
        """Convert 'rgb(r,g,b)' string to '#rrggbb'."""
        if s.startswith('rgb'):
            parts = s[s.find('(')+1 : s.find(')')].split(',')
            r, g, b = [int(p) for p in parts]
            return '#{:02x}{:02x}{:02x}'.format(r, g, b)
        return s  # already hex or name

    # Trim to max_cols for very long palettes
    colours = [rgb_to_hex(c) for c in colours]
    if len(colours) > max_cols:
        step = len(colours) / max_cols
        colours = [colours[int(i * step)] for i in range(max_cols)]

    pix = QPixmap(width, height)
    pix.fill(QColor('transparent'))
    painter = QPainter(pix)
    n = len(colours)
    if n == 0:
        return QIcon(pix)
    block_width = width / n
    for i, col in enumerate(colours):
        painter.fillRect(int(i * block_width), 0, int(block_width), height, QColor(col))
    painter.end()
    return QIcon(pix)


# --- CREATE COLOUR BOX ---
def build_colour_combo(self, width, height):
    combo = QComboBox()
    combo.setIconSize(QSize(width, height))
    model = QStandardItemModel(combo)

    # Merge discrete and continuous colour maps
    schemes = self.discrete_colour_map | self.continuous_colour_map

    for label, colours in schemes.items():
        item = QStandardItem()
        item.setText(label)
        item.setIcon(make_colour_icon(colours, width, height))
        model.appendRow(item)

    combo.setModel(model)
    combo.setMinimumWidth(200)
    return combo


# --- EXPORT DB ---
def call_db_export(self):

    # Export File
    today = datetime.now().strftime('%Y_%m_%d')
    export_path, _ = QFileDialog.getSaveFileName(self,
        'Export Database',
        f'astrotracker-{today}.db',
        'SQLite Database (*.db)'
    )
    if not export_path:
        return

    try:
        shutil.copyfile(self.db_path, export_path)
        QMessageBox.information(self, 'Success', 'Database exported successfully.')
    except Exception as e:
        QMessageBox.critical(self, 'Error', f'Unable to export database:\n{e}')


# --- IMPORT DB ---
def call_db_import(self):

    # Import File
    import_path, _ = QFileDialog.getOpenFileName(
        self,
        'Import Database',
        '',
        'SQLite Database (*.db)'
    )
    if not import_path:
        return

    try:
        shutil.copyfile(import_path, self.db_path)
        init_data(self)
        QMessageBox.information(self,
            'Success',
            'Database imported successfully.\n'
            'Restart the app to make changes effective'
        )
    except Exception as e:
        QMessageBox.critical(self, 'Error', 'Unable to import database')


# --- RESTORE DB ---
def call_db_default(self):

    reply = QMessageBox.question(self,
        'Restore Default Database',
        'This will delete your current data and restore the default database.\n'
        'Do you want to continue?',
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )

    if reply != QMessageBox.StandardButton.Yes:
        return

    # Delete DB File
    try:
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
    except Exception as e:
        QMessageBox.critical(self, 'Error', 'Unable to delete database')
        return

    # Show restart app message
    QMessageBox.information(self,
        'Restart Required',
        'The default database has been restored.\n'
        'Please restart AstroTracker for the changes to take effect.'
    )


# --- Export Multi Data in .yaml file ---
def multidata_export(self):

    file_path, _ = QFileDialog.getSaveFileName(
        self, f'Save YAML File', 'multidata.yaml', 'YAML Files (*.yaml)'
    )
    if not file_path:
        return

    try:
        # Ensure it ends with .yaml
        if not file_path.lower().endswith('.yaml'):
            file_path += '.yaml'

        # Export Data
        multi_mode = self.selmultidata.currentText()
        multi_values = get_multi_values(multi_mode=multi_mode, removeduplicates=True, self=self)
        if multi_mode == 'Multi Days':
            multi_values = [m.toString('yyyy-MM-dd') for m in multi_values]
            multi_values = list(dict.fromkeys(multi_values))
        config = {
            'multi_mode': multi_mode,
            'items': multi_values
        }
        with open(file_path, 'w') as f:
            yaml.dump(config, f, sort_keys=False)
        QMessageBox.information(self, 'Success', f'File saved as:\n{file_path}')

    except Exception as e:
        QMessageBox.critical(self, 'Error', f'Could not save file:\n{str(e)}')


# --- Import Multi Data .yaml file ---
def multidata_import(self):

    file_path, _ = QFileDialog.getOpenFileName(
        self, 'Open YAML File', '', 'YAML Files (*.yaml)'
    )
    if not file_path:
        return

    # Import Data
    with open(file_path, 'r') as f:
        config = yaml.safe_load(f)
        multi_mode = config['multi_mode']
        items = config['items']
        n_items = len(items)

        # Set Multi Type
        if multi_mode == 'Multi Objects': nidx = 1
        elif multi_mode == 'Multi Locations': nidx = 2
        elif multi_mode == 'Multi Days': nidx = 3
        else: nidx = None # Error
        self.selmultidata.setCurrentIndex(nidx)

        # Set number of data
        self.nrows.setValue(n_items)

        # Write Table (Multi Days)
        if multi_mode == 'Multi Days': # Multi Days

            for row in range(n_items):
                combo = self.multitable.cellWidget(row, 0)  # get the QComboBox
                if combo is not None:
                    y, m, d = map(int, items[row].split('-'))
                    qdate = QDate(y, m, d)
                    self.multitable.cellWidget(row, 0).setDate(qdate)

        # Write Table (Multi Objects or Multi Locations)
        else:

            # Look for missing Objects / Locations
            if multi_mode == 'Multi Locations': search_x = self.df_loc.location.tolist()
            elif multi_mode == 'Multi Objects': search_x = self.ssobj + self.df_stars.star.tolist()
            items_missing = [i for i in items if i not in list(search_x)]
            multi_label = multi_mode[6:].lower()

            # Manage missing parts
            if items_missing:
                message = (
                    f'The following {multi_label} are missing:\n' +
                    'Do you want to add them to the database?' +
                    ''.join(f'\n- {im}' for im in items_missing)
                )
                reply = QMessageBox.question(self, f'Add missing {multi_label}', message,
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )

                if reply != QMessageBox.StandardButton.Yes: # Exclude all missing items
                    items_exclude = items_missing

                else: # Search for missing items. If found, update the DB. If not, exclide them

                    if multi_mode == 'Multi Locations':
                        items_exclude = []
                        for im in items_missing:
                            lat, lon, time_zone, civil_utc, local_utc, _ = (
                                myal.get_location_coord(im))
                            if local_utc != []:
                                self.df_loc.loc[len(self.df_loc)] = {
                                    'id': max(self.df_loc.id) + 1,
                                    'location': im,
                                    'latitude': lat,
                                    'longitude': lon,
                                    'time_zone': time_zone,
                                    'civil_utc': civil_utc,
                                    'local_utc': local_utc
                                }
                                self.df_loc.sort_values(by='location', inplace=True)

                            else:
                                items_exclude.append(im)

                        # Warning if some items are not found
                        if items_exclude:
                            message = (
                                f'The following {multi_label} have not been found:\n' +
                                ''.join(f'\n- {im}' for im in items_exclude)
                            )
                            QMessageBox.information(self, f'Missing {multi_label}', message)

                        # Update GUI
                        self.select_location.clear()
                        self.select_location.addItems(self.df_loc.location.tolist())
                        if self.select_location.count() > 0:
                            self.select_location.setCurrentIndex(0)

                        # Update DB
                        with sqlite3.connect(self.db_path) as conn:
                            self.df_loc.to_sql('LOCATIONS', conn, if_exists='replace', index=False)
                            QMessageBox.information(self, 'Success', 'DB updated')
                            #if conn is not None: conn.close()

                    elif multi_mode == 'Multi Objects':
                        items_exclude = []
                        for im in items_missing:
                            vizier_name, ra0, dec0, pm_ra, pm_dec = (
                                myal.get_star_info(im))
                            if vizier_name:
                                self.df_stars.loc[len(self.df_stars)] = {
                                    'id': max(self.df_stars.id) + 1,
                                    'star': im,
                                    'vizier_name': vizier_name,
                                    'ra0': ra0,
                                    'dec0': dec0,
                                    'pm_ra': pm_ra,
                                    'pm_dec': pm_dec
                                }
                                self.df_stars.sort_values(by='star', inplace=True)

                            else:
                                items_exclude.append(im)

                        # Warning if some items are not found
                        if items_exclude:
                            message = (
                                f'The following {multi_label} have not been found:\n' +
                                ''.join(f'\n- {im}' for im in items_exclude)
                            )
                            QMessageBox.information(self, f'Missing {multi_label}', message)

                        # Update GUI
                        self.select_object.clear()
                        self.select_object.addItems(self.ssobj + self.df_stars.star.tolist())
                        if self.select_object.count() > 0:
                            self.select_object.setCurrentIndex(0)

                        # Update DB
                        with sqlite3.connect(self.db_path) as conn:
                            self.df_stars.to_sql('STARS', conn, if_exists='replace', index=False)
                            QMessageBox.information(self, 'Success', 'DB updated')
                            #if conn is not None: conn.close()

            else:
                items_exclude= []

            # Add items
            items_add = [i for i in items if i not in items_exclude]
            n_items_a = len(items_add)
            print('ITEMS ADD')
            print(items_add)
            self.nrows.setValue(n_items_a)
            for row in range(n_items_a):
                combo = self.multitable.cellWidget(row, 0)  # get the QComboBox
                if combo is not None:
                    self.multitable.cellWidget(row, 0).clear()
                    if multi_mode == 'Multi Locations':
                        self.multitable.cellWidget(row, 0).addItems(self.df_loc.location.tolist())
                    elif multi_mode == 'Multi Objects':
                        self.multitable.cellWidget(row, 0).addItems(self.ssobj + self.df_stars.star.tolist())
                    self.multitable.cellWidget(row, 0).setCurrentText(items_add[row])

        return


