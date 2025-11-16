# MIT License
# Copyright (c) 2025 Stefano Pantaleoni
#
# This file is part of the Astrotracker project.
# See the LICENSE.txt file in the project root for full license information.

import os
import sys
from functools import partial
import traceback
from datetime import datetime

import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QTableWidget, QMessageBox,
    QPushButton, QSpacerItem, QSizePolicy, QHBoxLayout, QDateEdit, QCheckBox, QTimeEdit, QSpinBox, QSplashScreen
)
from PyQt6.QtGui import QAction, QFont, QIcon, QPixmap
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt, QDate, QTimer, QTime
from astroquery.simbad import Simbad
Simbad.TIMEOUT = 2
import importlib
import myastrolib as myal
import myastroplot as myap
from callbacks import callbacks as cb

importlib.reload(myal)
importlib.reload(myap)
importlib.reload(cb)

# Environment (True for compiled version, False for development)
IS_FROZEN = getattr(sys, 'frozen', False)


# --- GLOBAL EXCEPTION HANDLING ---
def qt_exception_hook(exctype, value, tb):
    """
    Global exception hook: logs traceback to a file and shows a QMessageBox with details.
    This prevents unhandled exceptions inside Qt callbacks from killing the process.
    """
    try:
        tb_text = ''.join(traceback.format_exception(exctype, value, tb))
        # Log to stderr / console
        print(tb_text, file=sys.stderr)

        # Determine base path for log file (handle PyInstaller)
        try:
            base_path = sys._MEIPASS  # when frozen by PyInstaller
        except Exception:
            base_path = os.path.dirname(__file__) if '__file__' in globals() else os.getcwd()

        log_path = os.path.join(base_path, 'astrotracker_error.log')
        timestamp = datetime.now().strftime('%d-%b-%Y, %H:%M:%S')
        with open(log_path, 'a', encoding='utf-8') as fh:
            fh.write('=' * 32 + '\n')
            fh.write(f'Timestamp: {timestamp}\n\n')
            fh.write(tb_text)
            fh.write('\n')

        # Show a friendly dialog with expandable details
        # Use a minimal-safe approach: avoid complex UI creation if QApplication not available
        if QApplication.instance() is not None:
            try:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setWindowTitle('Unexpected Error')
                msg.setTextFormat(Qt.TextFormat.RichText)
                msg.setText(
                    'An unexpected error occurred.<br>'
                    'The app will attempt to continue.<br><br>'
                    f'See <a href="file:///{log_path}">astrotracker.log</a> for more information.'
                )
                # Short informative text
                msg.setInformativeText(str(value))
                # Expandable detailed traceback
                msg.setDetailedText(tb_text)
                msg.exec()
            except Exception:
                # If something goes wrong building the dialog, fallback to printing
                print('Failed to show QMessageBox for exception.', file=sys.stderr)
    except Exception as e:
        # Last-resort: print everything
        print('Error in qt_exception_hook:', e, file=sys.stderr)
        traceback.print_exc()


class SafeApplication(QApplication):
    """
    Subclass QApplication and override notify to catch exceptions raised during event processing.
    This prevents Qt from crashing when a signal/slot raises an exception.
    """
    def notify(self, receiver, event):
        try:
            return super().notify(receiver, event)
        except Exception:
            qt_exception_hook(*sys.exc_info())
            # Returning False indicates the event was not handled; prevents crash.
            return False


class MainWindow(QMainWindow):

    # --- MAIN WINDOW ---
    def __init__(self):

        ssobj: list[str]
        df_stars: pd.DataFrame
        df_loc: pd.DataFrame
        df_out: pd.DataFrame
        sel_time: str
        recalc: bool

        try:

            # Window Setup
            super().__init__()
            self.setWindowTitle('Astrotracker')
            self.ver = '1.2'
            self.recalc = True
            self.multimin = 2
            self.multimax = 18
            self.day_min = QDate(1900, 1, 1)
            self.day_max = QDate(2100, 12, 31)
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
            self.select_object.currentIndexChanged.connect(lambda: cb.change_objparam(self))
            top_row.addWidget(self.select_object)
            top_row.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum))

            # Location Selection
            label_location = QLabel('Location:')
            label_location.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            top_row.addWidget(label_location)

            self.select_location = QComboBox()
            self.select_location.addItems(self.df_loc.location)
            self.select_location.setFixedWidth(200)
            self.select_location.currentIndexChanged.connect(lambda: cb.change_objparam(self))
            top_row.addWidget(self.select_location)
            top_row.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum))

            # Day Selection
            label_day = QLabel('Day:')
            label_day.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            top_row.addWidget(label_day)

            self.select_day = QDateEdit()
            self.select_day.setDate(myap.capdate(QDate.currentDate(), self.day_min, self.day_max))
            self.select_day.setMinimumDate(self.day_min)
            self.select_day.setMaximumDate(self.day_max)
            self.select_day.setCalendarPopup(True)
            self.select_day.dateTimeChanged.connect(lambda: cb.change_objparam(self))
            top_row.addWidget(self.select_day)
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


            # -- SIDE MENU (WITHIN MAIN ROW) ---
            sidemenu = QVBoxLayout()
            sidemenu.setAlignment(Qt.AlignmentFlag.AlignTop)

            # Graph Selection
            label_graph = QLabel('Graph Type:')
            label_graph.setFont(QFont('', -1, QFont.Weight.Bold))
            label_graph.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            sidemenu.addWidget(label_graph)

            self.select_graph = QComboBox()
            self.select_graph.addItems([
                'Azimuth/Altidude',
                'Azimuth/Altidude (Polar)',
                'Equatorial',
                'Equatorial (Polar, North)',
                'Equatorial (Polar, South)'
            ])
            self.select_graph.setFixedWidth(170)
            sidemenu.addWidget(self.select_graph)
            sidemenu.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum))

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
            self.tmin.dateTimeChanged.connect(lambda: cb.tminmaxsel(self))
            tminmax.addWidget(self.tmin)
            label_tminmax = QLabel('-')
            tminmax.addWidget(label_tminmax)
            self.tmax = QTimeEdit()
            self.tmax.setDisplayFormat('HH:mm')
            self.tmax.setEnabled(False)
            self.tmax.setFixedWidth(80)
            self.tmax.setTime(QTime(0, 0))
            self.tmax.dateTimeChanged.connect(lambda: cb.tminmaxsel(self))
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
            self.tdelta.setSingleStep(1)
            self.tdelta.setValue(5)
            self.tdelta.valueChanged.connect(lambda: cb.change_objparam(self))
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


            # -- SIDE MENU 2 (WITHIN MAIN ROW) FOR MULTIPLE DATA ---
            multidatamenu = QVBoxLayout()
            multidatamenu.setAlignment(Qt.AlignmentFlag.AlignTop)

            # Multi Data
            label_selmultidata = QLabel('Multi Data:')
            label_selmultidata.setFont(QFont('', -1, QFont.Weight.Bold))
            label_selmultidata.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            multidatamenu.addWidget(label_selmultidata)

            # Multi Selector
            self.selmultidata = QComboBox()
            self.selmultidata.addItems([
                'Single Data',
                'Multi Objects',
                'Multi Locations',
                'Multi Days'
            ])
            self.selmultidata.setFixedWidth(120)
            self.selmultidata.currentIndexChanged.connect(lambda: cb.selmultidata(self))
            multidatamenu.addWidget(self.selmultidata)
            multidatamenu.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum))

            # Colour Selector
            label_selcolour = QLabel('Colour Scheme:')
            label_selcolour.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            multidatamenu.addWidget(label_selcolour)
            self.selcolour = QComboBox()
            self.selcolour.addItems([
                'Default (Categorical)',
                'Magma (Sequential)'
            ])
            self.selcolour.setFixedWidth(180)
            self.selcolour.setEnabled(False)
            multidatamenu.addWidget(self.selcolour)
            multidatamenu.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum))

            # Table Height Menu
            nrows = QHBoxLayout()
            nrows.setContentsMargins(0, 0, 0, 0)
            label_nrows = QLabel('Nr of rows')
            nrows.addWidget(label_nrows)
            self.nrows = QSpinBox()
            self.nrows.setRange(self.multimin, self.multimax)
            self.nrows.setSingleStep(1)
            self.nrows.setValue(self.multimin)
            self.nrows.valueChanged.connect(lambda: cb.selmultidata(self))
            self.nrows.setEnabled(False)
            nrows.addWidget(self.nrows)
            nrows.addSpacerItem(QSpacerItem(5, 5, QSizePolicy.Policy.Expanding))
            nrows_widget = QWidget()
            nrows_widget.setLayout(nrows)
            multidatamenu.addWidget(nrows_widget)

            # Multi Table
            self.multitable = QTableWidget()
            self.multitable.setRowCount(self.multimin)
            self.multitable.setColumnCount(1)
            self.multitable.horizontalHeader().hide()
            self.multitable.verticalHeader().hide()
            multi_options = ['']
            for row in range(12):
                combo = QComboBox()
                combo.addItems(multi_options)
                combo.setCurrentIndex(0)  # default to empty
                combo.currentIndexChanged.connect(lambda index, r=row: cb.change_objparam(self))
                combo.setMinimumHeight(24)  # makes it look better
                self.multitable.setCellWidget(row, 0, combo)
            self.multitable.horizontalHeader().setStretchLastSection(True)
            self.multitable.setEnabled(False)
            multidatamenu.addWidget(self.multitable)
            multidatamenu.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding))

            # Side Menu Container
            multidata_widget = QWidget()
            multidata_widget.setFixedWidth(200)
            multidata_widget.setLayout(multidatamenu)
            main_row.addWidget(multidata_widget)


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
            self.star_menu = menubar.addMenu('Stars')
            star_add = QAction('Add Stars', self)
            star_add.triggered.connect(lambda: cb.call_add_stars(self))
            self.star_menu.addAction(star_add)
            star_remove = QAction('Remove Stars', self)
            star_remove.triggered.connect(lambda: cb.call_remove_stars(self))
            self.star_menu.addAction(star_remove)

            # Locations Menu
            self.loc_menu = menubar.addMenu('Locations')
            loc_add = QAction('Add Locations', self)
            loc_add.triggered.connect(lambda: cb.call_add_locations(self))
            self.loc_menu.addAction(loc_add)
            loc_remove = QAction('Remove Locations', self)
            loc_remove.triggered.connect(lambda: cb.call_remove_locations(self))
            self.loc_menu.addAction(loc_remove)

            # Info Menu
            loc_info = menubar.addMenu('Info')
            loc_about = QAction('About', self)
            loc_about.triggered.connect(lambda: cb.show_about_dialog(self))
            loc_info.addAction(loc_about)

            # Initial Plot
            cb.update_plot(self)

            # Check if online
            try:
                Simbad.add_votable_fields('main_id')
                self.isonline = True
            except:
                self.isonline = False
                QMessageBox.warning(self, 'Offline', 'You are offline. Adding Stars / Locations features disabled')
                self.star_menu.setEnabled(False)
                self.loc_menu.setEnabled(False)

        except: # Fatal Error, DB restored
            cb.restore_db(self)
            QMessageBox.critical(self, 'Error', 'Problem with Astrotracker DB.<br>Please restart the tool.')


# --- MAIN APP EXECUTION ---
if __name__ == '__main__':
    # Install global exception hook so uncaught exceptions are handled consistently
    sys.excepthook = qt_exception_hook

    app = SafeApplication(sys.argv)
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS  # PyInstaller temp dir
    else:
        base_path = os.path.dirname(__file__)

    # Splashscreen
    if IS_FROZEN:
        splash_path = os.path.join(base_path, 'assets', 'astrotracker.png')
        pixmap = QPixmap(splash_path)
        scaled_pixmap = pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        splash = QSplashScreen(scaled_pixmap, Qt.WindowType.WindowStaysOnTopHint)
        splash.show()

    app.processEvents()
    icon_path = os.path.join(base_path, 'assets', 'astrotracker.ico')
    app.setWindowIcon(QIcon(icon_path))
    window = MainWindow()

    # Force Qt to process splash screen immediately
    if IS_FROZEN:
        QTimer.singleShot(200, splash.close)
    
    window.show()
    sys.exit(app.exec())
