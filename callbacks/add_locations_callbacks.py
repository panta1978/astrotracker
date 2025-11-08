# --- CALLBACKS USED BY ADD_LOCATIONS ---

import sqlite3
from PyQt6.QtWidgets import QMessageBox
import importlib
import myastrolib as myal

importlib.reload(myal)



# --- CHECK IF A LOCATION EXISTS
def check_location(self):

    # Look for Location
    self.lat, self.lon, self.time_zone, self.civil_utc, self.local_utc = (
        myal.get_location_coord(self.location_name_field.text()))
    self.locationname = self.location_name_field.text()
    if not self.local_utc:
        self.check_result_field.setText('NOT FOUND')
        self.lat_field.setText('')
        self.lon_field.setText('')
        self.civilutc_field.setText('')
        self.localutc_field.setText('')
        self.timezone_field.setText('')
        self.update_btn.setEnabled(False)
    else:
        self.check_result_field.setText('OK')
        self.lat_field.setText(str(self.lat))
        self.lon_field.setText(str(self.lon))
        self.civilutc_field.setText(str(self.civil_utc))
        self.localutc_field.setText(str(self.local_utc))
        self.timezone_field.setText(self.time_zone)
        self.update_btn.setEnabled(True)



# --- UPDATE DB
def update_db(self):

    # Check if Location already exists
    if self.locationname.lower() in [x.lower() for x in self.main.df_loc.location.tolist()]:
        QMessageBox.warning(self, 'Not updated', 'Location already present. DB not updated')
        return

    # Update LOCATION Table
    self.main.df_loc.loc[len(self.main.df_loc)] = {
        'id': max(self.main.df_loc.id) + 1,
        'location': self.locationname,
        'latitude': self.lat,
        'longitude': self.lon,
        'time_zone': self.time_zone,
        'civil_utc': self.civil_utc,
        'local_utc': self.local_utc
    }
    self.main.df_loc.sort_values(by='location', inplace=True)

    # Update GUI
    self.main.select_location.clear()
    self.main.select_location.addItems(self.main.df_loc.location.tolist())
    if self.main.select_location.count() > 0:
        self.main.select_location.setCurrentIndex(0)

    # Update DB
    with sqlite3.connect(self.main.db_path) as conn:
        self.main.df_loc.to_sql('LOCATIONS', conn, if_exists='replace', index=False)
        QMessageBox.information(self, 'Success', 'DB updated')




