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
import plotly.express as px


# --- LAUNCH PLOT (SINGLE) ---
def makeplot_multi(df_out, curr_obj, curr_location, curr_day, plot_type, multi_mode, multi_values, self):

    # multi_mode can be 'Single Data', 'Multi Objects', 'Multi Locations', 'Multi Days'
    # Init new structure (that will be filtered)
    df_outspl = {}

    # Routine to extract filtered values
    def dfos_get(df, curr_obj):
        dfos = df[[
            't_current', 'n_day', 'hour_current', 'day_sel', 'loc_sel', 'n_loc',
            f'{curr_obj}_azimuth_deg', f'{curr_obj}_altitude_deg', f'{curr_obj}_ha', f'{curr_obj}_declination_deg'
            ]].copy()
        dfos.rename(columns={
            f'{curr_obj}_azimuth_deg': 'obj_azimuth_deg',
            f'{curr_obj}_altitude_deg': 'obj_altitude_deg',
            f'{curr_obj}_ha': 'obj_ha',
            f'{curr_obj}_declination_deg': 'obj_declination_deg'
        }, inplace=True)
        return dfos

    # Case 1 - Multi Objects
    if multi_mode == 'Multi Objects':
        for curr_obj in multi_values:
            dfos = dfos_get(df_out, curr_obj)
            df_outspl[curr_obj] = dfos
        curr_obj_txt = 'Multiple Objects'
    else:
        curr_obj_txt = curr_obj

    # Case 2 - Multi Locations
    if multi_mode == 'Multi Locations':
        for curr_location in multi_values:
            dfos = df_out[df_out['loc_sel'] == curr_location]
            dfos = dfos_get(dfos, curr_obj)
            df_outspl[curr_location] = dfos
        curr_location = 'Multiple Locations'

    # Case 3 - Multi Days
    if multi_mode == 'Multi Days':
        for curr_day in multi_values:
            dfos = df_out[df_out['day_sel'] == curr_day]
            dfos = dfos_get(dfos, curr_obj)
            df_outspl[curr_day] = dfos
        curr_day = 'Multiple Days'

    # Labels
    if 'Azimuth/Altidude' in plot_type:
        label1 = 'Altitude [°]'
        label2 = 'Azimuth [°]'
    elif 'Equatorial' in plot_type:
        label1 = 'Declination [°]'
        label2 = 'Ha [h]'

    # Init variables
    y1s = {} ; y2s = {}
    times = {} ; azs = {} ; alts = {} ; has = {} ; decs = {}

    for multi_value in multi_values:
        dfos = df_outspl[multi_value]

        # Define Variables
        if 'Azimuth/Altidude' in plot_type:
            y1 = dfos['obj_altitude_deg'].copy()
            y2 = dfos['obj_azimuth_deg'].copy()
        elif 'Equatorial' in plot_type:
            y1 = dfos['obj_declination_deg'].copy()
            y2 = dfos['obj_ha'].copy()
            if 'Polar' in plot_type:
                if 'North' in plot_type:
                    y1 = -y1
                y2 = y2 * 15
        if 'Polar' in plot_type:
            y1 = y1 + 90

        # For 2-axis plots, manage discontinuities of y1 (Azimuth) and y2 (hour angle)
        if not('Polar' in plot_type):
            ymax = 24 if 'Equatorial' in plot_type else 360
            y2_isdisc = y2.diff().abs() > ymax*0.9
            y2[y2_isdisc] = np.nan

        # Write variables
        y1s[multi_value] = [y for y in y1]
        y2s[multi_value] = [y for y in y2]

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
        times[multi_value] = [f'{t:%H %M %S}' for t in dfos['t_current'].copy()]
        azs[multi_value] = [to_dms(x) for x in dfos['obj_azimuth_deg'].copy()]
        alts[multi_value] = [to_dms(x) for x in dfos['obj_altitude_deg'].copy()]
        has[multi_value] = [to_hms(x) for x in dfos['obj_ha'].copy()]
        decs[multi_value] = [to_dms(x) for x in dfos['obj_declination_deg'].copy()]

    # Define x-axis (time) - Equal for all lines. A dummy day is used for reference
    t_series = df_outspl[multi_values[0]].t_current
    first_date = t_series.iloc[0].date()
    x_gr = t_series.apply(
        lambda t: datetime.combine(
            date(1970, 1, 1) + timedelta(days=(t.date() - first_date).days),
            t.time()
        )
    )

    hover_templ = (
        'Time: %{customdata[0]}<br>'
        'Azimuth: %{customdata[1]}°<br>'
        'Altitude: %{customdata[2]}°<br>'
        'Hour Angle: %{customdata[3]}<br>'
        'Declination: %{customdata[4]}°<br>'
        '<extra></extra>'
    )

    # Prepare colours
    graphcols = px.colors.qualitative.Plotly

    # --- 2-AXIS PLOT ---
    if not('Polar' in plot_type):

        # Create subplots: 2 rows, 1 col
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, row_heights=[0.5, 0.5],
            subplot_titles=[
                f'{curr_obj_txt} in {curr_location} on {curr_day} - {label1} ({self.sel_time} Time)',
                f'{curr_obj_txt} in {curr_location} on {curr_day} - {label2} ({self.sel_time} Time)'
            ]
            )

        # Add lines 1st ROW
        for nv, multi_value in enumerate(multi_values):
            cust_data = list(zip(times[multi_value], azs[multi_value], alts[multi_value], has[multi_value], decs[multi_value]))
            fig.add_trace(go.Scatter(x=x_gr, y=y1s[multi_value], mode='lines',
                line=dict(color=graphcols[nv], width=1),
                customdata=cust_data, hovertemplate='<b>' + multi_value + '</b><br>'+hover_templ,
                name=multi_value), row=1, col=1)

        # Axes 1st ROW
        fig.update_xaxes(range=[x_gr.min(), x_gr.max()], row=1, col=1, tickformat='%H:%M', nticks=20)
        fig.update_yaxes(range=[-90, 90], tickvals=np.arange(-90, 91, 30), title_text=label1, row=1, col=1)

        # Add lines 2nd ROW
        for nv, multi_value in enumerate(multi_values):
            cust_data = list(zip(times[multi_value], azs[multi_value], alts[multi_value], has[multi_value], decs[multi_value]))
            fig.add_trace(go.Scatter(x=x_gr, y=y2s[multi_value], mode='lines',
                line=dict(color=graphcols[nv], width=1),
                customdata=cust_data, hovertemplate='<b>' + multi_value + '</b><br>'+hover_templ,
                name=multi_value, showlegend=False), row=2, col=1)

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
            title=f'{curr_obj_txt} in {curr_location} on {curr_day} ({self.sel_time} Time)'
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
        for nv, multi_value in enumerate(multi_values):
            cust_data = list(zip(times[multi_value], azs[multi_value], alts[multi_value], has[multi_value], decs[multi_value]))
            fig.add_trace(go.Scatterpolar(r=y1s[multi_value], theta=y2s[multi_value], mode='lines',
                line=dict(color=graphcols[nv], width=1),
                customdata=cust_data, hovertemplate='<b>' + multi_value + '</b><br>'+hover_templ,
                name=multi_value)
            )

        # Add black circle
        theta_circle = np.linspace(0, 360, 361)  # full circle, 1° step
        r_circle = np.full_like(theta_circle, 90)  # constant radius = 90°
        fig.add_trace(go.Scatterpolar(
            r=r_circle, theta=theta_circle,
            mode='lines', line=dict(color='black', width=1.5),
            name='Horizon', hoverinfo='skip', showlegend=False # optional: disable hover
        ))

    # Render in PyQt6 WebView
    html = fig.to_html(include_plotlyjs='cdn')
    self.webview.setHtml(html)
