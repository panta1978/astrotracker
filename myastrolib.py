# MIT License
# Copyright (c) 2025 Stefano Pantaleoni
#
# This file is part of the Astrotracker project.
# See the LICENSE.txt file in the project root for full license information.

import pandas as pd
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime, timedelta, timezone
from dateutil.tz import tzoffset
from zoneinfo import ZoneInfo
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz
from astropy.coordinates import solar_system_ephemeris, get_body
import astropy.units as u
from astropy.coordinates import SkyCoord
from astroquery.vizier import Vizier
from astroquery.simbad import Simbad
Simbad.TIMEOUT = 2
import warnings
from erfa import ErfaWarning
warnings.simplefilter('ignore', ErfaWarning)



# --- GET LOCATION INFO ---
def get_location_coord(sel_location):

    # Init output structures
    lat, lon, tz_name, fixed_utc, local_utc = [], [], [], [], []
    current_year = datetime.now().year

    geolocator = Nominatim(user_agent='city_locator')
    location = geolocator.geocode(sel_location)

    if location: # Location found

        # Get Latitude, Longitude, and Time Zone
        lat, lon = location.latitude, location.longitude
        tf_i = TimezoneFinder()
        tz_name = tf_i.timezone_at(lat=lat, lng=lon)

        # Get UTC of Timezone without DST
        tz_info = ZoneInfo(tz_name)
        if lat >= 0: # Northern Hemisphere. Consider Jan, 1st
            fixed_utc = tz_info.utcoffset(datetime(current_year, 1, 1)).total_seconds()/3600
        else: # Southern Hemisphere. Consider Jul, 1st
            fixed_utc = tz_info.utcoffset(datetime(current_year, 7, 1)).total_seconds()/3600

        # Get Local Time
        local_utc = lon / 15

    else: # Location not found
        print(f'Location {sel_location} not found. Skipped')

    return lat, lon, tz_name, fixed_utc, local_utc



# --- GET STAR INFO ---
def get_star_info(sel_star):

    # Init output structures
    Simbad.add_votable_fields('main_id')
    try:
        simbad_query = Simbad.query_object(sel_star)
        vizier_name = simbad_query['main_id'][0].replace('*', '').strip()
    except:
        return [], [], [], [], []

    # Set-up Star catalogue
    Vizier.ROW_LIMIT = 1
    catalog = 'I/239/hip_main'

    # Get Star Coordinates at 2000 AD
    try:
        result = Vizier(
            columns=['RAICRS', 'DEICRS', 'pmRA', 'pmDE'],
            timeout=5
        ).query_object(sel_star, catalog=catalog)[0]
    except:
        print(f'Star {sel_star} (Vizier name: {vizier_name}) not found. Skipped')
        return [], [], [], [], []

    star_ra0 = result['RAICRS'][0]
    star_dec0 = result['DEICRS'][0]
    star_pm_ra = result['pmRA'][0]  # milliarcsec/year
    star_pm_dec = result['pmDE'][0]   # milliarcsec/year
    return vizier_name, star_ra0, star_dec0, star_pm_ra, star_pm_dec



# --- GET SOLAR SYSTEM BODIES COORDINATES ---
def get_coords(
        sel_ssbodies,
        sel_stars, stars_ra0, stars_dec0, stars_pm_ra, stars_pm_dec,
        loc_names, lats, lons, tz_names, sel_time,
        sel_days, t_min, t_max, t_delta):

    df_s = [] # Init output structure

    # Loop through locations
    nl = 0
    for lat, lon, loc_name, tz_name in zip(lats, lons, loc_names,tz_names):
        nl += 1

        # Create location
        location = EarthLocation(
            lat = lat * u.deg,
            lon =lon * u.deg,
            height = 0 * u.m
        )

        # Select Time Type
        if sel_time == 'Civil': curr_tz = tz_name
        elif sel_time == 'Local': curr_tz = tzoffset(None, int((lon/15) * 3600))
        elif sel_time == 'Greenwich': curr_tz = 0

        # Get local time (multiple days)
        delta_days = 1 if t_min >= t_max else 0
        t_current_s = [pd.date_range(
            start=f'{sel_day} {t_min}',
            end=f'{pd.to_datetime(sel_day) + pd.Timedelta(days=delta_days):%Y-%m-%d} {t_max}',
            freq=f'{t_delta}min',
            tz=curr_tz,
            nonexistent='shift_forward'
        ) for sel_day in sel_days]
        t_current = pd.concat([r.to_series() for r in t_current_s]).index
        n_day_s = [[i+1 for _ in row] for i, row in enumerate(t_current_s)]
        n_day = [elem for row in n_day_s for elem in row]

        # Day and location
        day_sel = [f'{t:%Y-%m-%d}' for t in t_current]
        loc_sel = [loc_name] * len(t_current)
        n_loc = [nl] * len(t_current)

        # Conversion to UTC and sidereal
        hour_current = t_current.hour + t_current.minute / 60 + t_current.second / 3600
        t_utc = Time(t_current.to_pydatetime())
        t_current_sid = t_utc.sidereal_time('apparent', lon * u.deg)

        # Coordinate transform
        altaz_frame = AltAz(obstime=t_utc, location=location)

        # Init current location output structure
        df_s1 = [
            pd.DataFrame({
                't_current': t_current,
                'n_day': n_day,
                'hour_current': hour_current,
                'day_sel': day_sel,
                'loc_sel': loc_sel,
                'n_loc': n_loc
            })
        ]

        # Get Solar System Objects Position
        solar_system_ephemeris.set('builtin')
        for sel_ssbody in sel_ssbodies:
            try:
                ssb_radec = get_body(sel_ssbody, t_utc, location=location)
            except:
                print(f'Solar System Body {sel_ssbody} not found. Skipped')
            ssb_altaz = ssb_radec.transform_to(altaz_frame)
            ssb_ha = (t_current_sid - ssb_radec.ra).wrap_at(360 * u.deg)

            # Current Object results
            df_i = pd.DataFrame({
                f'{sel_ssbody}_azimuth_deg': ssb_altaz.az.degree,
                f'{sel_ssbody}_altitude_deg': ssb_altaz.alt.degree,
                f'{sel_ssbody}_ha': ssb_ha,
                f'{sel_ssbody}_declination_deg': ssb_radec.dec.degree,
            })
            df_s1.append(df_i)

        for (sel_star, star_ra0, star_dec0, star_pm_ra, star_pm_dec) in (
            zip(sel_stars, stars_ra0, stars_dec0, stars_pm_ra, stars_pm_dec)):

            # Propagte Star position to today
            star_2000 = SkyCoord(
                ra = star_ra0 * u.deg,
                dec = star_dec0 * u.deg,
                pm_ra_cosdec = star_pm_ra * u.mas / u.yr,  # milliarcsec/year
                pm_dec = star_pm_dec * u.mas / u.yr,  # milliarcsec/year
                frame='icrs',
                obstime=Time('J2000')
            )
            today = Time.now()
            star_today = star_2000.apply_space_motion(new_obstime=today)
            star_radec = SkyCoord(
                ra=star_today.ra,
                dec=star_today.dec,
                frame='icrs'
            )
            star_altaz = star_radec.transform_to(altaz_frame)
            star_ha = (t_current_sid - star_radec.ra).wrap_at(360 * u.deg)

            # Current Star results
            df_i = pd.DataFrame({
                f'{sel_star}_azimuth_deg': star_altaz.az.degree,
                f'{sel_star}_altitude_deg': star_altaz.alt.degree,
                f'{sel_star}_ha': star_ha,
                f'{sel_star}_declination_deg': star_radec.dec.degree,
            })
            df_s1.append(df_i)

        # Update output structure with current location values
        df_s.append(pd.concat(df_s1, axis=1))

    # Output
    df_out = pd.concat(df_s, axis=0)
    return df_out
