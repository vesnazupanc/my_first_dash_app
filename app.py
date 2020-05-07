import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

from get_data import get_data_plot1, get_data_plot2
from risanjeAnimacij import narisi_graf_1, narisi_graf_2

# =============================================================================
# DEFINIRAMO MOŽNOSTI ZA DROPDOWN SEZNAME
# =============================================================================

spol_dict = {'female': 'Ženski',
             'male': 'Moški',
             'both': 'Skupaj'}

mere = ['Prevalenca', 'Incidenca', 'Umrljivost']

# =============================================================================
# PRIDOBIVANJE PODATKOV IN RISANJE GRAFOV
# =============================================================================

# PLOTS 1

df1 = get_data_plot1()
plots1 = {}
for key, value in spol_dict.items():
    dff1 = df1[df1.spol == key]
    fig = narisi_graf_1(dff1, dff1.Incidenca.max() + 100, dff1.Incidenca.max() + 100)
    plots1[key] = fig

# PLOTS 2

df2 = get_data_plot2()
plots2 = {}
for mera in mere:
    fig = narisi_graf_2(df2, mera, df2[mera].max() + 100)
    plots2[mera] = fig

# =============================================================================
# BESEDILA ZA PRVA DVA ZAVIRHKA
# =============================================================================

besedilo_uvod = '''
#### Dobrodošli!
                    
Avtorja pregleda: 

* Vesna Zupanc (vz1459@student.uni-lj.si)
* Janez Bijec (...)

Predstavljamo vam spletno aplikacijo, ki je nastala z namenom prikaza 
učinkovitosti zdravstvenega sistema pri rakavih obolenjih. 

##### Kazalo

**Metedološka pojasnila**

Tu se nahajajo pojasnila in opombe.

**Zemljevid**

Na zemljevidu si lahko pri poljubnem spolu in vrsti raka pogledate...

**Grafični pregled 1**

spet neko besedilo

**Grafični pregled 2**

še tuki pojasnilo ... 
'''

besedilo_pojasnila = '''
##### Nekaj pojasnil
'''
# =============================================================================
# APLIKACIJA
# =============================================================================

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.H1('Prikaz podatkov SLORA'),
    html.Div([
        dcc.Tabs(id="tabs", value='tab-domov', children=[
            dcc.Tab(label='Domov', value='tab-domov'),
            dcc.Tab(label='Metodološka pojasnila', value='tab-pojasnila'),
            dcc.Tab(label='Grafični prikaz 1', value='tab-g1'),
            dcc.Tab(label='Grafični prikaz 2', value='tab-g2'),
        ]),
        html.Div(id='tabs-content', style={'width': '600'})
    ])
])

tab1 = html.Div([
    dcc.Markdown(besedilo_uvod)
])
tab2 = html.Div([
    dcc.Markdown(besedilo_pojasnila)
])

tab3 = html.Div([
    html.Div(className="row", children=[
        html.Div(className="three columns",
                 children=[html.H6('Izberi spol:'),
                           dcc.Dropdown(
                               id='d1-spol-filter',
                               options=[{'label': spol_dict[i], 'value': i} for i in ['male', 'female', 'both']],
                               value='both')
                           ]),
        html.Div(className="nine columns", style={'height': '700px'},
                 children=[dcc.Graph(id='plot1', style={'height': 'inherit'})
                           ])
    ])
])

tab4 = html.Div([
    html.Div(className="row", children=[
        html.Div(className="three columns",
                 children=[html.H6('Izberi mero:'),
                           dcc.Dropdown(
                               id='d2-mera-filter',
                               options=[{'label': i, 'value': i} for i in mere],
                               value='Incidenca')
                           ]),
        html.Div(className="nine columns", style={'height': '700px'},
                 children=[dcc.Graph(id='plot2', style={'height': 'inherit'})
                           ])
    ])
])

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-domov':
        return tab1
    elif tab == 'tab-pojasnila':
        return tab2
    elif tab == 'tab-g1':
        return tab3
    elif tab == 'tab-g2':
        return tab4


@app.callback(
    Output(component_id='plot1', component_property='figure'),
    [Input(component_id='d1-spol-filter', component_property='value')])
def callback_plot1(spol_value):
    fig = plots1[spol_value]
    return fig


@app.callback(
    Output(component_id='plot2', component_property='figure'),
    [Input(component_id='d2-mera-filter', component_property='value')])
def callback_plot2(mera_input):
    fig = plots2[mera_input]
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
