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

mere = ['Prevalenca', 'Incidenca', 'Umrljivost','Groba incidenčna stopnja','Groba umrljivostna stopnja']

# =============================================================================
# PRIDOBIVANJE PODATKOV IN RISANJE GRAFOV
# =============================================================================

# PLOTS 1

df1 = get_data_plot1()
plots1 = {}
for key, value in spol_dict.items():
    dff1 = df1[df1.spol == key]
    fig = narisi_graf_1(dff1, dff1['Incidenca'].max()*1.1, dff1['Umrljivost'].max()*1.1)
    plots1[key] = fig

# PLOTS 2

df2 = get_data_plot2()
plots2 = {}
for mera in mere:
    fig = narisi_graf_2(df2, mera, df2[mera].max()*1.1)
    plots2[mera] = fig

# =============================================================================
# BESEDILA ZA PRVA DVA ZAVIRHKA
# =============================================================================

besedilo_uvod1 = '''
### **DOBRODOŠLI!**
  
Nahajate se na interaktivni spletni aplikaciji za prikaz podatkov iz Registra raka Republike Slovenije, 
ki je nastala v skladu predmeta Viri podatkov na študijskem programu druge stopnje Uporabna statistika. 
'''

besedilo_uvod2 = '''
##### **NAMEN APLIKACIJE**

Namen spletne aplikacije je predstaviti pojavnost, breme raka in uspešnost spopadanja s to boleznijo v Sloveniji. 
Podatki so prikazani v obliki dveh grafičnih prikazov, kjer so uporabljene različne mere, s katerimi opisujemo pojavnost bolezni.
Več o uporabljenih merah in razlagi le teh, si lahko preberete v zavihku **Metodološka pojasnila.** 
'''
besedilo_uvod3 = '''
##### **PRIKAZI**

Do prikazov dostopate pod zavihkoma **Grafični prikaz 1** in **Grafični prikaz 2**.

V prikazih boste opazili, da so nekatere lokacije raka posebej poudarjene. 
Poudarjene so na podlagi več različnih dejavnikov, ki so predvsem pogostost pojavitve in s tem večja "zanimivost", 
poleg tega pa so vedno poudarjene lokacije raka, ki so vključene v nacionalne presejalne programe **ZORA**, **DORA** in **SVIT**. 
Namen je predvsem pokazati vpliv presejalnih programov na prej omenjene mere.

Več o presejalnik programih si lahko preberete na spodnjih povezavah:

* [ZORA](https://zora.onko-i.si/): Državni program zgodnjega odkrivanja  predrakavih sprememb  materničnega vratu
* [DORA](https://dora.onko-i.si/): Državni presejalni program za raka dojke
* [SVIT](https://www.program-svit.si/): Državni program presejanja in zgodnjega odkrivanja predrakavih sprememb in raka na debelem črevesu in danki

Vir podatkov o incidenci ter prevalenci je podatkovna zbirka [Registra raka RS](https://www.onko-i.si/rrs), 
podatke o umrljivosti pa zbira Nacionalni inštitut za javno zdravje ([NIJZ](https://www.nijz.si/)). 
'''
besedilo_uvod4 = '''
##### **OPIS GRAFIČNIH PRIKAZOV**

###### **Grafični prikaz 1**

Točkovni grafični prikaz ponuja primerjavo med incidenco in umrljivostjo glede na
lokacijo raka od leta 1985 do leta 2016. 
Prav tako ponuja tudi izbiro spola, kjer s tem lahko filtriramo podatke na ženski ali moški spol, podatke pa lahko
pogledamo tudi za oba spola skupaj. 
Z ukazom "Play" ali pa z ročno interakcijo po letih, si lahko opazujemo kakšen je trend posameznega raka.
S pomikom kurzorja na neko točko pa lahko dobimo lokacijo pripadajočega raka ter podatek o grobi incidenčni in umrljivostni stopnji. 

###### **Grafični prikaz 2**

Stolpčni diagram prav tako prikazuje trend gibanja posameznega raka, kjer sta prikazana oba spola hkrati.
V tem primeru izbiramo med posameznimi merami, ki so nam na voljo v spustnem seznamu. 
Prav tako lahko izbiramo med leti od 1985 do leta 2016 ali pa s klikom na gumb "Play" opazujemo animacijo.
'''

besedilo_pojasnila1 = '''
##### **INCIDENCA**
**Incidenca** je mera, ki izraža absolutno število vseh novih primerov neke bolezni v časovnem intervalu, 
ponavadi koledarskem letu. Ker incidenca ne meri število bolnikov, se lahko zgodi, da isti bolnik v 
incidenco prispeva več primerov, če zboli za različnimi raki. **Groba incidenčna stopnja** je mera, 
ki absolutno velikost incidence v populaciji preračuna glede na 100 tisoč prebivalcev. 
Groba incidenčna stopnja nam omogoča lažjo primerljivost med geografskimi in časovnimi območji.  
'''
besedilo_pojasnila2 = '''
##### **UMRLJIVOST**
**Umrljivost** je mera, ki izraža absolutno število umrlih v neki populaciji, kot posledica neke bolezni, 
v našem primeru raka, v določenem časovnem obdobju, najbolj pogosto se za časovno obdobje uporablja koledarsko leto. 
Analogno grobi incidenčni stopnji, tudi v tem primeru definiramo **Grobo umrljivostno stopnjo**, 
ki absolutno število, po enaki enačbi, preračuna na 100 tisoč prebivalcev. 
Med merami umrljivosti poznamo še starostno standardizirano umrljivostno stopnjo. 
'''
besedilo_pojasnila3 = '''
##### **PREVALENCA**
**Prevalenca** je mera, ki nam pove, koliko bolnikov, s postavljeno diagnozo, je bilo na določen datum še živih. 
Ponavadi je ta datum zadnji dan v letu. Za mere prevalence ni pomembno, kdaj je oseba zbolela.
'''

komentar1 = '''
Breme raka se je med letoma 1985 in 2016 v Sloveniji povečalo. 
Pri obeh spolih je največja umrljivost za vrsto raka, ki spada v skupino **sapnik, sapnici in pljuča**.
Tu je vredno omembe, da v skupino ne spada rak mezoteliom, za katerega je znano, da je glavni povzročitelj azbest. 
Mezoteliom ne spada v osnovno razdelitev raka, zato ni posebej prikazan. 

Pri moških ima opazno povečanje incidence rak **prostate**, kjer pa incidenca narašča hitreje kot umrljivost.

Opazno je tudi veliko povečanje incidence pri **drugih malignih neoplazmah kože**, je pa tu umrljivost skozi leta
konstantno nizka.

**Raki iz presejalnih programov**:

Pri **materničnem vratu** vidimo, da padata tako incidenca kot umrljivost, kar kaže uspeh presejalnega programa **ZORA**.

Pri raku **dojke** je videti upočasnitev rasti umrljivosti, kar kaže na učinkovitost presejalnega programa **DORA**
'''

komentar2 = '''
Glede na grobo incidenčno stopnjo in grobo umrljivosto stopnjo opazimo, da je v splošnem rak pogostejši
pri moških, kot pri ženskah. Posledično je tudi umrljivost pri moških večja. Opazimo lahko tudi, da se je 
pri moških zelo povečalo breme raka **prostate**. 

Prevalenca se v splošnem z leti povečuje, kar pa je posledica tudi večje incidence. Zato si moramo pogledati obe meri,
v kolikor nekaj sklepati. 

**Raki iz presejalnih programov**:

Pri raku **materničnega vratu** lako opazimo da se incidenca in groba incidenčna stopnja z leti zmanjšujeta, prevalenca pa se 
povečuje. To nakazuje, da je presejalni program **ZORA** zelo uspešen.

Pri raku **dojke** se incidenca in groba incidenčna stopnja sicer z leti povečujeta, vendar pa se prevalenca povečuje hitreje,
groba stopnja umrljivosti pa je v zadnjih letih celo padla. Tudi to nakazuje na uspešnost presejalnega programa **DORA**.

Uspešnost programa **SVIT** je trenutno težje oceniti, vendar bo le to najverjetneje močneje opazno čez nekaj let, ko
bomo imeli na voljo več podatkov.
'''



# =============================================================================
# APLIKACIJA
# =============================================================================
tabtitle = 'Prikaz podatkov SLORA'
external_stylesheets = ['https://codepen.io/vesnazupanc/pen/oNjqeMJ.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = tabtitle
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
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
    html.Div([dcc.Markdown(besedilo_uvod1)], style={'padding': '0px 0px 20px 0px'}),
    html.Div([dcc.Markdown(besedilo_uvod2)], style={'padding': '0px 0px 20px 0px'}),
    html.Div([dcc.Markdown(besedilo_uvod3)], style={'padding': '0px 0px 20px 0px'}),
    html.Div([dcc.Markdown(besedilo_uvod4)], style={'padding': '0px 0px 20px 0px'}),
], style={'padding': '70px 450px 20px 20px'})
tab2 = html.Div([
    html.Div([dcc.Markdown(besedilo_pojasnila1)], style={'padding': '0px 0px 20px 0px'}),
    html.Div([dcc.Markdown(besedilo_pojasnila2)], style={'padding': '0px 0px 20px 0px'}),
    html.Div([dcc.Markdown(besedilo_pojasnila3)], style={'padding': '0px 0px 20px 0px'})
], style={'padding': '70px 450px 20px 20px'})

tab3 = html.Div([
    html.Div(className="row", children=[
        html.Div(className="three columns",
                 children=[html.H5('Izberi spol:'),
                           dcc.Dropdown(
                               id='d1-spol-filter',
                               options=[{'label': spol_dict[i], 'value': i} for i in ['male', 'female', 'both']],
                               value='both',
                               clearable=False),
                           html.H5('Komentar:'),
                           html.Div([dcc.Markdown(komentar1)], style={'padding': '0px 0px 20px 0px'})
                           ]),
        html.Div(className="nine columns", style={'height': '800px'},
                 children=[dcc.Graph(id='plot1', style={'height': 'inherit'})
                           ])
    ])
])

tab4 = html.Div([
    html.Div(className="row", children=[
        html.Div(className="three columns",
                 children=[html.H5('Izberi mero:'),
                           dcc.Dropdown(
                               id='d2-mera-filter',
                               options=[{'label': i, 'value': i} for i in mere],
                               value='Incidenca',
                               clearable=False),
                           html.H5('Komentar:'),
                           html.Div([dcc.Markdown(komentar2)], style={'padding': '0px 0px 20px 0px'})
                           ]),
        html.Div(className="nine columns", style={'height': '800px'},
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
    app.run_server()
