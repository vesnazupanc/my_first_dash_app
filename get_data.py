import pandas as pd

genders = ['male', 'female', 'both']

regions = ['Pomurska',
           'Podravska',
           'Koroška',
           'Savinjska',
           'Zasavska',
           'Spodnjeposavska',
           'Jugovzhodna Slovenija',
           'Osrednjeslovenska',
           'Gorenjska',
           'Notranjsko-kraška',
           'Goriška',
           'Obalno-kraška']

age_groups = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59',
              '60-64', '65-69', '70-74', '75-79', '80']

stadiji = ['Omejen','Razsirjen', 'Razsejan', 'inSitu', 'Neznan']

measures = {'2a1': 'Incidenca',
            '2a2': 'Groba Incidenčna stopnja',
            '2b1': 'Umrljivost',
            '2b2': 'Groba umrljivostna stopnja',
            '2c1': 'Prevalenca',
            '2d1': 'Preživetje'}

raki = {'2a1': '229',
        '2a2': '229',
        '2b1': '300',
        '2b2': '300',
        '2c1': '229',
        '2d1': '229'}

poudarjeni = {'debelo črevo (C18)': '#e41a1c',
              'dojka (C50)': '#377eb8',
              'druge maligne neoplazme kože (C44)': '#4daf4a',
              'maligni melanom kože (C43)': '#984ea3',
              'maternični vrat (C53)': '#ff7f00',
              'prostata (C61)': '#F2E92D',
              'rektum in rektosigmoidna zveza (C19–C20)': '#a65628',
              'sapnik, sapnici in pljuča (C33–C34)': '#f781bf',
              'ostali raki': '#C9C9C9'}

def get_data_plot1():
    prefix = 'http://www.slora.si/SLORA-Web/excelExport'
    df_final = pd.DataFrame()
    for measure in ['2a1', '2b1']:
        for gender in genders:
            postfix = (f'gender={gender}&'
                       f'groupBy=RakihOsnovno&'
                       f'obmocje=X&'
                       f'raki={raki[measure]}|0&'
                       f'yearsInterval=1985-2016&'
                       f'ageGroup=0-80&'
                       f'stadij=All&'
                       f'locale=sl')
            url = prefix + measure + '?' + postfix
            data = pd.read_excel(url)
            cols, rows, values = data.iloc[6, 1:].values, data.iloc[7:, 0].values, data.iloc[7:, 1:].values
            df = pd.DataFrame(values, columns=cols)
            df['vrstaRaka'] = rows
            df = df.melt(id_vars='vrstaRaka', var_name='Leto', value_name='Vrednost')
            df['spol'], df['mera'] = gender, measures[measure]
            df_final = df_final.append(df)
    df_final = df_final.pivot_table(index=['Leto', 'vrstaRaka', 'spol'], columns='mera',
                                    values='Vrednost').reset_index()

    df_final['Skupina'] = [x if x in poudarjeni.keys() else 'ostali raki' for x in df_final.vrstaRaka]
    df_final['barva'] = [poudarjeni[x] for x in df_final.Skupina]
    df_final.Leto = df_final.Leto.astype(int)
    return df_final


def get_data_plot2():
    prefix = 'http://www.slora.si/SLORA-Web/excelExport'
    df_final = pd.DataFrame()
    for measure in ['2a1', '2b1']:
        for gender in ['male', 'female']:
            postfix = (f'gender={gender}&'
                       f'groupBy=RakihOsnovno&'
                       f'obmocje=X&'
                       f'raki={raki[measure]}|0&'
                       f'yearsInterval=1985-2016&'
                       f'ageGroup=0-80&'
                       f'stadij=All&'
                       f'locale=sl')
            url = prefix + measure + '?' + postfix
            data = pd.read_excel(url)
            cols, rows, values = data.iloc[6, 1:].values, data.iloc[7:, 0].values, data.iloc[7:, 1:].values
            df = pd.DataFrame(values, columns=cols)
            df['vrstaRaka'] = rows
            df = df.melt(id_vars='vrstaRaka', var_name='Leto', value_name='Vrednost')
            df['spol'], df['mera'] = gender, measures[measure]
            df_final = df_final.append(df)
    for measure in ['2c1']:
        for gender in ['male', 'female']:
            postfix = (f'gender={gender}&'
                       f'groupBy=RakihOsnovno&'
                       f'obmocje=X&'
                       f'raki={raki[measure]}|0&'
                       f'yearsInterval=1985-2016&'
                       f'prevalenca=celokupna&'
                       f'locale=sl')
            url = prefix + measure + '?' + postfix
            data = pd.read_excel(url)
            cols, rows, values = data.iloc[6, 1:].values, data.iloc[7:, 0].values, data.iloc[7:, 1:].values
            df = pd.DataFrame(values, columns=cols)
            df['vrstaRaka'] = rows
            df = df.melt(id_vars='vrstaRaka', var_name='Leto', value_name='Vrednost')
            df['spol'], df['mera'] = gender, measures[measure]
            df_final = df_final.append(df)

    df_final['Skupina'] = [x if x in poudarjeni.keys() else 'ostali raki' for x in df_final.vrstaRaka]
    df_final = df_final.groupby(['Leto', 'spol', 'mera', 'Skupina']).sum().reset_index()
    df_final = df_final.rename(columns={'Skupina': 'vrstaRaka'})
    df_final = df_final.pivot_table(index=['Leto', 'vrstaRaka', 'spol'], columns='mera',
                                    values='Vrednost').reset_index()
    df_final.Leto = df_final.Leto.astype(int)

    sortiranje = {'ostali raki': '0',
                  'druge maligne neoplazme kože (C44)': '1',
                  'maligni melanom kože (C43)': '2',
                  'sapnik, sapnici in pljuča (C33–C34)': '3',
                  'rektum in rektosigmoidna zveza (C19–C20)': '4',
                  'prostata (C61)': '6',
                  'maternični vrat (C53)': '7',
                  'dojka (C50)': '8',
                  'debelo črevo (C18)': '9'}

    df_final['sort_index'] = df_final.vrstaRaka.replace(sortiranje).astype(int)

    df_final = df_final.sort_values('sort_index')

    return df_final