import plotly.graph_objects as go

def narisi_graf_1(df, xlim, ylim):
    years = list(range(1985, 2017))
    skupine_rakov = df['Skupina'].unique()

    # make figure
    fig_dict = {
        "data": [],
        "layout": {},
        "frames": []
    }

    # fill in most of layout
    fig_dict["layout"]["plot_bgcolor"] = "white"
    fig_dict["layout"]["xaxis"] = {"range": [-50, xlim], "title": "Incidenca",
                                   "showline": True, "linecolor": 'black', 'gridcolor': None,
                                   'zerolinecolor': None}
    fig_dict["layout"]["yaxis"] = {"range": [-50, ylim], "title": "Umrljivost",
                                   "showline": True, "linecolor": 'black', 'gridcolor': '#cccccc',
                                   'gridwidth': 1}
    fig_dict["layout"]["hovermode"] = "closest"
    fig_dict["layout"]["font"] = {"size": 17}
    fig_dict["layout"]["updatemenus"] = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 500, "redraw": False},
                                    "fromcurrent": True, "transition": {"duration": 300,
                                                                        "easing": "quadratic-in-out"}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                      "mode": "immediate",
                                      "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }
    ]

    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Leto:",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 300, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": []
    }

    # make data
    year = 1985
    for skupina in skupine_rakov:
        df_leto = df[df["Leto"] == year]
        df_leto_skupina = df_leto[df_leto["Skupina"] == skupina]

        data_dict = {
            "x": list(df_leto_skupina["Incidenca"]),
            "y": list(df_leto_skupina["Umrljivost"]),
            "mode": "markers",
            "text": list(df_leto_skupina["vrstaRaka"]),
            "hovertemplate": '<b>%{text}</b><br><br>Umrljivost: %{y}<br>Incidenca: %{x}',
            "marker": {
                "size": 15,
                "color": list(df_leto_skupina["barva"])
            },
            "name": skupina
        }
        fig_dict["data"].append(data_dict)

    # make frames
    for year in years:
        frame = {"data": [], "name": str(year)}
        for skupina in skupine_rakov:
            df_leto = df[df["Leto"] == year]
            df_leto_skupina = df_leto[df_leto["Skupina"] == skupina]

            data_dict = {
                "x": list(df_leto_skupina["Incidenca"]),
                "y": list(df_leto_skupina["Umrljivost"]),
                "mode": "markers",
                "text": list(df_leto_skupina["vrstaRaka"]),
                "hovertemplate": '<b>%{text}</b><br><br>Umrljivost: %{y}<br>Incidenca: %{x}',
                "marker": {
                    "size": 15,
                    "color": list(df_leto_skupina["barva"])
                },
                "name": skupina
            }
            frame["data"].append(data_dict)

        fig_dict["frames"].append(frame)
        slider_step = {"args": [
            [year],
            {"frame": {"duration": 300, "redraw": False},
             "mode": "immediate",
             "transition": {"duration": 300}}
        ],
            "label": year,
            "method": "animate"}
        sliders_dict["steps"].append(slider_step)

    fig_dict["layout"]["sliders"] = [sliders_dict]

    fig = go.Figure(fig_dict)

    return fig


def narisi_graf_2(df, mera, xlim):
    years = list(range(1985, 2017))
    spoli = ['Moški', 'Ženski']
    df.spol = df.spol.replace({"male": "Moški", "female": "Ženski"})

    # make figure
    fig_dict = {
        "data": [],
        "layout": {},
        "frames": []
    }

    # fill in most of layout
    fig_dict["layout"]["plot_bgcolor"] = "white"
    fig_dict["layout"]["xaxis"] = {"range": [0, xlim], "title": mera, "showline": True, "linecolor": 'black'}
    fig_dict["layout"]["yaxis"] = {"title": None}
    fig_dict["layout"]["hovermode"] = "closest"
    fig_dict["layout"]["font"] = {"size": 17}
    fig_dict["layout"]["updatemenus"] = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 500, "redraw": False},
                                    "fromcurrent": True, "transition": {"duration": 300,
                                                                        "easing": "quadratic-in-out"}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                      "mode": "immediate",
                                      "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }
    ]

    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Leto:",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 300, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": []
    }

    # make data
    year = 1985
    for spol in spoli:
        df_leto = df[df["Leto"] == year]
        df_leto_skupina = df_leto[df_leto["spol"] == spol]

        data_dict = {
            "x": list(df_leto_skupina[mera]),
            "y": list(df_leto_skupina["vrstaRaka"]),
            "text": list(df_leto_skupina["vrstaRaka"]),
            "hovertemplate": '<b>%{text}</b><br>%{x}',
            "type": "bar",
            "orientation": 'h',
            "name": spol,
        }
        fig_dict["data"].append(data_dict)

    # make frames
    for year in years:
        frame = {"data": [], "name": str(year)}
        for spol in spoli:
            df_leto = df[df["Leto"] == year]
            df_leto_skupina = df_leto[df_leto["spol"] == spol]

            data_dict = {
                "x": list(df_leto_skupina[mera]),
                "y": list(df_leto_skupina["vrstaRaka"]),
                "text": list(df_leto_skupina["vrstaRaka"]),
                "hovertemplate": '<b>%{text}</b><br>%{x}',
                "type": "bar",
                "orientation": 'h',
                "name": spol
            }
            frame["data"].append(data_dict)

        fig_dict["frames"].append(frame)
        slider_step = {"args": [
            [year],
            {"frame": {"duration": 300, "redraw": False},
             "mode": "immediate",
             "transition": {"duration": 300}}
        ],
            "label": year,
            "method": "animate"}
        sliders_dict["steps"].append(slider_step)

    fig_dict["layout"]["sliders"] = [sliders_dict]

    fig = go.Figure(fig_dict)

    return fig

