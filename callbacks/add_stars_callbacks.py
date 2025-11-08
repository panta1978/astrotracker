# --- CALLBACKS USED BY ADD_STARS ---

import sqlite3
from PyQt6.QtWidgets import QMessageBox
import importlib
import myastrolib as myal

importlib.reload(myal)



# --- CHECK IF A STAR EXISTS
def check_star(self):

    # Look for Star
    self.vizier_name, self.ra0, self.dec0, self.pm_ra, self.pm_dec = (
        myal.get_star_info(self.star_name_field.text()))
    self.starname = self.star_name_field.text().title() # Make all letters uppercase
    if not self.vizier_name:
        self.check_result_field.setText('NOT FOUND')
        self.ra_field.setText('')
        self.dec_field.setText('')
        self.pm_ra_field.setText('')
        self.pm_dec_field.setText('')
        self.vizier_field.setText('')
        self.update_btn.setEnabled(False)
    else:
        self.check_result_field.setText('OK')
        self.star_name_field.setText(self.starname)
        self.ra_field.setText(str(self.ra0))
        self.dec_field.setText(str(self.dec0))
        self.pm_ra_field.setText(str(self.pm_ra))
        self.pm_dec_field.setText(str(self.pm_dec))
        self.vizier_field.setText(self.vizier_name)
        self.update_btn.setEnabled(True)



# --- UPDATE DB
def update_db(self):

    # Check if Star already exists
    if self.starname in self.main.df_stars.star.tolist():
        QMessageBox.warning(self, 'Not updated', 'Star already present. DB not updated')
        return

    # Update STAR Table
    self.main.df_stars.loc[len(self.main.df_stars)] = {
        'id': max(self.main.df_stars.id) + 1,
        'star': self.starname,
        'vizier_name': self.vizier_name,
        'ra0': self.ra0,
        'dec0': self.dec0,
        'pm_ra': self.pm_ra,
        'pm_dec': self.pm_dec
    }
    self.main.df_stars.sort_values(by='star', inplace=True)

    # Update GUI
    self.main.select_object.clear()
    self.main.select_object.addItems(self.main.ssobj + self.main.df_stars.star.tolist())
    if self.main.select_object.count() > 0:
        self.main.select_object.setCurrentIndex(0)

    # Update DB
    with sqlite3.connect(self.main.db_path) as conn:
        self.main.df_stars.to_sql('STARS', conn, if_exists='replace', index=False)
        QMessageBox.information(self, 'Success', 'DB updated')


