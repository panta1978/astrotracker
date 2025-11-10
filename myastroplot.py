# MIT License
# Copyright (c) 2025 Stefano Pantaleoni
#
# This file is part of the Astrotracker project.
# See the LICENSE.txt file in the project root for full license information.

import numpy as np
import pandas as pd
from datetime import datetime, date, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots



# --- LAUNCH PLOT (SINGLE) ---
def makeplot_single(df_out, curr_obj, curr_location, curr_day, plot_type, self):

    # Define Variables
    if 'Azimuth/Altidude' in plot_type:
        y1 = df_out[f'{curr_obj}_altitude_deg'].copy()
        y2 = df_out[f'{curr_obj}_azimuth_deg'].copy()
        label1 = 'Altitude [°]'
        label2 = 'Azimuth [°]'
    elif 'Equatorial' in plot_type:
        y1 = df_out[f'{curr_obj}_declination_deg'].copy()
        y2 = df_out[f'{curr_obj}_ha'].copy()
        label1 = 'Declination [°]'
        label2 = 'Ha [h]'
        if 'Polar' in plot_type:
            if 'North' in plot_type:
                y1 = -y1
            y2 = y2*15
    if 'Polar' in plot_type:
        y1 = y1 + 90

    def to_dms(angle):
        sign = '+' if angle >= 0 else '-'
        angle = abs(angle)
        deg = int(angle)
        minutes = int((angle - deg) * 60)
        seconds = (angle - deg - minutes / 60) * 3600
        return f'{sign}{deg}° {minutes:02d}\' {seconds:04.1f}"'

    def to_hms(hours):
        hours = abs(hours)
        h = int(hours)
        minutes = int((hours - h) * 60)
        seconds = (hours - h - minutes / 60) * 3600
        return f'{h}h {minutes:02d}m {seconds:04.1f}s'

    # Define labels for graphs
    time = [f'{t:%H %M %S}' for t in df_out['t_current'].copy()]
    az = [to_dms(x) for x in df_out[f'{curr_obj}_azimuth_deg'].copy()]
    alt = [to_dms(x) for x in df_out[f'{curr_obj}_altitude_deg'].copy()]
    ha = [to_hms(x) for x in df_out[f'{curr_obj}_ha'].copy()]
    dec = [to_dms(x) for x in df_out[f'{curr_obj}_declination_deg'].copy()]

    hover_templ = (
        'Time: %{customdata[0]}<br>'
        'Azimuth: %{customdata[1]}°<br>'
        'Altitude: %{customdata[2]}°<br>'
        'Hour Angle: %{customdata[3]}<br>'
        'Declination: %{customdata[4]}°<br>'
        '<extra></extra>'
    )

    # Set colours
    if curr_obj == 'SUN':
        cols = {
            'Night': 'rgb(60, 0, 0)',
            'Twilight': 'rgb(220, 70, 20)',
            'Day': 'rgb(255, 190, 100)'
        }
    else:
        cols = {
            'Night': 'rgb(0, 10, 50)',
            'Twilight': 'rgb(30, 90, 220)',
            'Day': 'rgb(150, 210, 255)'
        }
    
    # Define x-axis (time) - A dummy day is used for reference
    t_series = df_out.t_current
    first_date = t_series.iloc[0].date()
    x_gr = t_series.apply(
        lambda t: datetime.combine(
            date(1970, 1, 1) + timedelta(days=(t.date() - first_date).days),
            t.time()
        )
    )
    
    # Prepare line styles with gaps
    sun_alt = df_out.SUN_altitude_deg.copy()
    star_alt = df_out[f'{curr_obj}_altitude_deg'].copy()

    # Look for (night, twilight, day) and (above, below)
    positions = [
        'Night Above', 'Twilight Above', 'Day Above',
        'Night Below', 'Twilight Below', 'Day Below'
    ]
    is_night = sun_alt<-6
    is_twilight = (sun_alt>=-6) & (sun_alt<0)
    is_day = sun_alt>=0
    is_above = star_alt >= 0
    is_below = star_alt < 0

    # Filter positions
    if self.daynight.currentText() == 'Night Only':
        positions = [p for p in positions if ('Night' in p) or ('Twilight' in p)]
    if self.daynight.currentText() == 'Day Only':
        positions = [p for p in positions if ('Day' in p) or ('Twilight' in p)]
    if self.horizonview.currentText() == 'Above Horizon':
        positions = [p for p in positions if ('Above' in p)]

    def extend(v): # Function to extend segments (for better plots)
        v_ext = v | np.concatenate(([False], v[:-1])) | np.concatenate((v[1:], [False]))
        return v_ext

    status = {
        'Night Above': extend(is_night & is_above),
        'Twilight Above': extend(is_twilight & is_above),
        'Day Above': extend(is_day & is_above),
        'Night Below': extend(is_night & is_below),
        'Twilight Below': extend(is_twilight & is_below),
        'Day Below': extend(is_day & is_below)
    }

    # For 2-axis plots, manage discontinuities of y1 (Azimuth) and y2 (hour angle)
    if not('Polar' in plot_type):
        ymax = 24 if 'Equatorial' in plot_type else 360
        y2_isdisc = y2.diff().abs() > ymax*0.9
        y2[y2_isdisc] = np.nan

    # Split y1, y2, and hover labels by positions
    y1s = {} ; y2s = {}
    times = {} ; azs = {} ; alts = {} ; has = {} ; decs = {}
    for position in positions:
        y1s[position] = [val if sts else None for (val, sts) in zip(y1, status[position])]
        y2s[position] = [val if sts else None for (val, sts) in zip(y2, status[position])]
        times[position] = [val if sts else None for (val, sts) in zip(time, status[position])]
        azs[position] = [val if sts else None for (val, sts) in zip(az, status[position])]
        alts[position] = [val if sts else None for (val, sts) in zip(alt, status[position])]
        has[position] = [val if sts else None for (val, sts) in zip(ha, status[position])]
        decs[position] = [val if sts else None for (val, sts) in zip(dec, status[position])]



    # --- 2-AXIS PLOT ---
    if not('Polar' in plot_type):

        # Create subplots: 2 rows, 1 col
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, row_heights=[0.5, 0.5],
            subplot_titles=[
                f'{curr_obj} in {curr_location} on {curr_day} - {label1} ({self.sel_time} Time)',
                f'{curr_obj} in {curr_location} on {curr_day} - {label2} ({self.sel_time} Time)'
            ]
            )

        # Add lines 1st ROW
        for position in positions:
            p1, p2 = position.split(' ')
            cust_data = list(zip(times[position], azs[position], alts[position], has[position], decs[position]))
            dash_type = 'solid' if p2 == 'Above' else 'dot'
            fig.add_trace(go.Scatter(x=x_gr, y=y1s[position], mode='lines',
                line=dict(color=cols[p1], dash=dash_type, width=3),
                customdata=cust_data, hovertemplate='<b>' + position + '</b><br>'+hover_templ,
                name=position), row=1, col=1)

        # Axes 1st ROW
        fig.update_xaxes(range=[x_gr.min(), x_gr.max()], row=1, col=1, tickformat='%H:%M', nticks=20)
        fig.update_yaxes(range=[-90, 90], tickvals=np.arange(-90, 91, 30), title_text=label1, row=1, col=1)

        # Add lines 2nd ROW
        for position in positions:
            p1, p2 = position.split(' ')
            cust_data = list(zip(times[position], azs[position], alts[position], has[position], decs[position]))
            dash_type = 'solid' if p2 == 'Above' else 'dot'
            fig.add_trace(go.Scatter(x=x_gr, y=y2s[position], mode='lines',
                line=dict(color=cols[p1], dash=dash_type, width=3),
                customdata=cust_data, hovertemplate='<b>' + position + '</b><br>'+hover_templ,
                name=position, showlegend=False), row=2, col=1)

        # Axes 2nd ROW
        if 'Azimuth/Altidude' in plot_type:
            tickvals2 = np.arange(0, 361, 45)
        elif 'Equatorial' in plot_type:
            tickvals2 = np.arange(0, 25, 3)
        fig.update_xaxes(range=[x_gr.min(), x_gr.max()], row=2, col=1, tickformat='%H:%M', nticks=20)
        fig.update_yaxes(range=[min(tickvals2), max(tickvals2)], tickvals=tickvals2, title_text=label2, row=2, col=1)
        fig.update_layout(margin=dict(t=20, b=10, l=50, r=50))



    # --- POLAR PLOT ---
    else:

        # Create Polar Graph
        tickvals_th = np.arange(0, 346, 15)
        ticktext_th = [f'{t}°' for t in tickvals_th]
        ticktext_r = ['-90°','-60°','-30°','0°','30°','60°','90°']
        if 'North' in plot_type:
            ticktext_r = ticktext_r[::-1]

        if 'Azimuth/Altidude' in plot_type:
            ticktext_th[0] = '<span style="font-size:18px;"><b>N</b></span>'
            ticktext_th[3] = '<span style="font-size:14px;"><b>NE</b></span>'
            ticktext_th[6] = '<span style="font-size:18px;"><b>E</b></span>'
            ticktext_th[9] = '<span style="font-size:14px;"><b>SE</b></span>'
            ticktext_th[12] = '<span style="font-size:18px;"><b>S</b></span>'
            ticktext_th[15] = '<span style="font-size:14px;"><b>SW</b></span>'
            ticktext_th[18] = '<span style="font-size:18px;"><b>W</b></span>'
            ticktext_th[21] = '<span style="font-size:14px;"><b>NW</b></span>'

        rng = 90 if ('Equatorial' in plot_type) and (self.halfhemisphere.isChecked()) else 180
        fig = go.Figure()
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    range=[0, rng],  # because radius = elevation + 90
                    tickvals=np.arange(0, 181, 30),
                    ticktext=ticktext_r,
                    showline=True,
                    linewidth=1,
                    gridcolor='lightgrey'
                ),
                angularaxis=dict(
                    direction='clockwise',
                    rotation=90,  # start from north at top (0°)
                    tickvals=tickvals_th,
                    ticktext=ticktext_th,
                    gridcolor='lightgrey'
                ),
                #bgcolor='rgb(240,240,240)'
            ),
            margin=dict(t=40, b=20, l=50, r=50),
            title=f'{curr_obj} in {curr_location} on {curr_day} ({self.sel_time} Time)'
        )

        # Add "N" or "S" at the center
        if 'Equatorial' in plot_type:
            center_label = 'N' if 'North' in plot_type else 'S'
            fig.add_annotation(
                text=f'<b>{center_label}</b>',   # bold
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=18),
                xref='paper', yref='paper'
            )

        # Add lines
        for position in positions:
            p1, p2 = position.split(' ')
            cust_data = list(zip(times[position], azs[position], alts[position], has [position], decs[position]))
            dash_type = 'solid' if p2 == 'Above' else 'dot'
            fig.add_trace(go.Scatterpolar(r=y1s[position], theta=y2s[position], mode='lines',
                line=dict(color=cols[p1], dash=dash_type, width=3),
                customdata=cust_data, hovertemplate='<b>' + position + '</b><br>'+hover_templ,
                name=position)
            )

        # Add black circle
        theta_circle = np.linspace(0, 360, 361)  # full circle, 1° step
        r_circle = np.full_like(theta_circle, 90)  # constant radius = 90°
        fig.add_trace(go.Scatterpolar(
            r=r_circle, theta=theta_circle,
            mode='lines', line=dict(color='black', width=1.5),
            name='Horizon', hoverinfo='skip', showlegend=False # optional: disable hover
        ))


    # --- RENDER PLOT ---
    html = fig.to_html(include_plotlyjs='cdn')
    self.webview.setHtml(html)


