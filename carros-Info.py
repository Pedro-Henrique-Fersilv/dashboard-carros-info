import streamlit as st
import pandas as pd
import plotly.graph_objects as go

#Configuração da página
st.set_page_config(
    layout="wide",
    page_title="Carros Info",
    page_icon="🚗",
)
st.title('CARROS INFO')

#Importando estilo CSS
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#Cor dos elementos dashboard
background_graficos = 'rgb(30, 30, 30)'
cor_gráficos = 'rgb(217, 41, 41)'
cor_borda_tabela = 'rgb(255, 138, 138)'

#---------------------------REGISTRO DE ACIDENTES---------------------------

#Criação de colunas
col1, col2 = st.columns([2,1])

with col1:

    #Leitura do arquivo csv base de dados
    data_base = 'data/Road-Accident-Data.csv'
    df = pd.read_csv(data_base)

    st.header('ACIDENTES AUTOMOBILÍSTICOS')

    #Criando colunas internas
    colin1, colin2 = st.columns([3,2])

    with colin1:
        
        #Extraindo os valores da coluna para o gráfico
        causas = df['Junction_Control'].value_counts()
        values = causas.values.tolist()

        #Criando e exibindo o gráfico
        fig = go.Figure([go.Bar(
            x= ('Descontrole', 'Sinal de trânsito', 'Cruzamento','Placa de Pare'),
            y= (values),text=(values),textposition='outside',
            marker_color = cor_gráficos
        )])

        fig.update_layout(
            annotations=[
                dict(
                    text="Causas",
                    x=0.5,
                    y=1.15,
                    xref='paper',
                    yref='paper',
                    font=dict(size=16),
                    showarrow=False
                )
            ],
            width = 400,
            height = 250,
            margin=dict(t=30, b=10, l=10, r=10),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor= background_graficos
        )

        st.plotly_chart(fig,use_container_width=True)

    #---------------------------GRÁFICO DE QUANTIDADE DE ACIDENTES POR MÊS---------------------------

        #Convertendo valor do 'Accident-date' para data e agrupando os dias em meses
        df['Accident-Date'] = pd.to_datetime(df['Accident-Date']).dt.to_period('M')
        
        acidentes_por_mes = df['Accident-Date'].value_counts().sort_index()

        fig = go.Figure(data=[
            go.Scatter(
            x=acidentes_por_mes.index.astype(str), 
            y=acidentes_por_mes, mode='lines+markers',
            marker_color = cor_gráficos
            )
        ])

        fig.update_layout(
            annotations=[
                dict(
                    text="Ocorrências por mês",
                    x=0.5,
                    y=1.15,
                    xref='paper',
                    yref='paper',
                    font=dict(size=16),
                    showarrow=False
                )
            ],
            width = 400,
            height = 200,
            margin=dict(t=20, b=10, l=10, r=10),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor= background_graficos
        )

        st.plotly_chart(fig,use_container_width=True)

    #---------------------------GRÁFICOS DE PIZZA---------------------------

    with colin2:

        #Criando e exibindo o gráfico de pizza em plotly express(Número de acidentes por semana)
        dias = df['Day_of_Week'].value_counts()

        #Contando acidentes ocorridos em cada dia da semana
        labels = ['Segunda','Terça','Quarta','Quinta', 'Sexta']
        values = dias.values.tolist()

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

        #Colocando texto em cima do gráfico
        fig.update_layout(
            annotations=[
                dict(
                    text="Taxa de acidentes por dia da semana",
                    x=0.5,
                    y=1.3,
                    font=dict(size=16),
                    showarrow=False
                )
            ],
            width = 250,
            height = 200,
            margin=dict(t=40, b=10, l=70, r=10),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor= background_graficos
        )

        st.plotly_chart(fig,use_container_width=True)


        #Criando e exibindo o segundo gráfico de pizza (gravidade dos acidentes)
        gravidade = df['Accident_Severity'].value_counts()

        labels = ['Leve', 'Grave']
        values = gravidade.values.tolist()

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

        #Colocando texto em cima do gráfico
        fig.update_layout(
            annotations=[
                dict(
                    text="Taxa de gravidade dos acidentes",
                    x=0.5,
                    y=1.3,
                    font=dict(size=16),
                    showarrow=False
                )
            ],
            width = 250,
            height = 200,
            margin=dict(t=40, b=10, l=70, r=10),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor= background_graficos
        )

        st.plotly_chart(fig,use_container_width=True)


#---------------------------GRÁFICO DO DESEMPENHO DE CARROS---------------------------

with col2:

    #Leitura do arquivo csv base de dados (desempenho)
    data_base = 'data/Automobile.csv'
    df = pd.read_csv(data_base)

    st.header('Desempenho')

    #Filtro de pesquisa por nome selecionado
    options = df['name']
    st.sidebar.header('Desempenho')
    selected_option = st.sidebar.selectbox("Selecione o modelo:", options)
    selected_name = df[df['name'] == selected_option]
    
    #Dividindo o peso para ficar melhor a visualização do gráfico 
    selected_name['weight'] = selected_name['weight'] / 2205
    selected_name['displacement'] = selected_name['displacement'] / 100
    selected_name['horsepower'] = selected_name['horsepower'] / 10

    #Formatando o peso para 2 numeros somente depois da virgula
    selected_name['weight'] = selected_name['weight'].map('{:.2f}'.format).astype(float)

    #Extraindo os valores das colunas para o gráfico
    y_values = selected_name[['mpg', 'cylinders', 'weight','displacement','horsepower', 'acceleration', 'model_year']].values.flatten()
    
    #Criando e exibindo o gráfico
    fig = go.Figure([go.Bar(
        x= ('MPG', 'Cilíndros', 'Peso (tonelada)','Deslocamento (L)', ' Potência (/10)', 'Aceleração (0 - 100/s)'),
        y= (y_values),text=(y_values),textposition='outside',
        marker_color = cor_gráficos
    )])

    fig.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor= background_graficos
    )

    st.plotly_chart(fig,use_container_width=True)

#Criação de colunas
col1, col2, col3 = st.columns(3)

with col1:

    #Leitura do arquivo csv base de dados
    data_base = 'data/Top10Report_wTotalThefts.csv'
    df = pd.read_csv(data_base)

    #Abreviando os valores para ficar compátivel com o mapa dos EUA
    state_abbreviations = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA', 'Colorado': 'CO', 
        'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID', 
        'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 
        'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 
        'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 
        'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 
        'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 
        'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 
        'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
    }

    df['State'] = df['State'].map(state_abbreviations)

    #Removendo valores "nan" do 'Make/Model'
    df = df.dropna(subset=['Make/Model'])

    #Removendo caracteres que não sejam valores inteiros ou float
    df['Thefts'] = df['Thefts'].replace({',': '', '"': ''}, regex=True).astype(float)

    #Select box para selecionar o carro que deseja buscar
    st.header('Registro de veículos roubados')
    options = df['Make/Model'].unique()
    st.sidebar.header('Registro de veículos roubados')
    selected_option = st.sidebar.selectbox("Selecione o modelo:", options)
    selected_car = df[df['Make/Model'] == selected_option]

    #Agrupando os dados do carro selecionado por estado
    df_selected_grouped = selected_car.groupby('State')['Thefts'].sum().reset_index()

    #---------------------------MAPA DE REGISTRO DE ROUBOS---------------------------

    #Quantidade de roubos são indicados pela intensidade da cor
    fig = go.Figure(data=go.Choropleth(
        locations = df_selected_grouped['State'],
        z = df_selected_grouped['Thefts'],
        locationmode = 'USA-states',
        colorscale = 'Reds',
        colorbar=dict(
        title="Registros",
        thickness=15,
        len=0.6,
        x=1,
        )
    ))

    fig.update_layout(
        geo_scope='usa',
        height = 350,
        margin=dict(t=10, b=10, l=10, r=10),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor= background_graficos
    )

    #Removendo background do mapa
    fig.update_geos(
        bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig,use_container_width=True)

with col2:

    #---------------------------TABELA DE VEÍCULOS MAIS ROUBADOS---------------------------

    st.header('Veículos mais roubados')

    fig = go.Figure(data=[go.Table(
        columnwidth=[3.5, 1, 1],
        header=dict(
        values=['Modelo', 'Ano' , 'Roubos'],
        fill_color =  'rgb(20, 20, 20)',
        line_color = cor_borda_tabela
        ),

        cells=dict(
            values= [
                df['Make/Model'],
                df['Model-Year'],
                df['Thefts'],
            ],
            fill_color = 'rgb(30, 30, 30)',
            line_color = cor_borda_tabela
        )
    )])

    #Ajuste no tamanho
    fig.update_layout(
        width = 200,
        height = 350,
        margin=dict(t=10, b=40, l=10, r=40),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor= background_graficos
    )

    st.plotly_chart(fig,use_container_width=True)

with col3:

    #---------------------------TABELA FIPE---------------------------

    #Leitura do arquivo csv base de dados (tabela fipe)
    data_base = 'data/tabela-fipe-historico-precos.csv'
    df = pd.read_csv(data_base)

    st.header('Tabela Fipe')

    st.sidebar.header ('Tabela Fipe')
    #Filtro de pesquisa por nome selecionado
    options = df['marca'].unique()
    selected_marca = st.sidebar.selectbox("Marca:", options)

    #Filtro de pesquisa por ano do modelo selecionado
    options2 = sorted(df[df['marca'] == selected_marca]['modelo'].unique())
    selected_model = st.sidebar.selectbox("Modelo:", options2)

    #Filtro de pesquisa por ano do modelo selecionado
    options3 = sorted(df[(df['marca'] == selected_marca) & (df['modelo'] == selected_model)]['anoModelo'].unique())
    selected_date = st.sidebar.selectbox("Ano do modelo:", options3)

    #Filtro de pesquisa por ano de referência selecionado
    options4 = sorted(df[(df['marca'] == selected_marca) & (df['modelo'] == selected_model) & (df['anoModelo'] == selected_date)]['anoReferencia'].unique())
    selected_anoRef = st.sidebar.selectbox("Ano de referência:", options4)

    #Aplicando Filtros
    selected_option = df[(df['marca'] == selected_marca) & (df['modelo'] == selected_model) & (df['anoModelo'] == selected_date) & (df['anoReferencia'] == selected_anoRef)]

    #Tabela sendo exibida
    fig = go.Figure(data=[go.Table(
        columnwidth =[2, 1.5, 2, 1, 0.5, 2],
        header=dict(
        values=['CódigoFipe', 'Marca' , 'Modelo', 'Ano do modelo','Mês de referência', 'Ano de referencia', 'Valor'],
        fill_color =  'rgb(20, 20, 20)',
        line_color = cor_borda_tabela
        ),

        cells=dict(
            values= [
                selected_option['codigoFipe'],
                selected_option['marca'],
                selected_option['modelo'],
                selected_option['anoModelo'],
                selected_option['mesReferencia'],
                selected_option['anoReferencia'],
                selected_option['valor']
                ],
            fill_color =  'rgb(30, 30, 30)',
            line_color = cor_borda_tabela
        )
    )])

    #Ajuste no tamanho
    fig.update_layout(
        width = 200,
        height = 350,
        margin=dict(t=10, b=40, l=10, r=40),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor= background_graficos
    )

    st.plotly_chart(fig,use_container_width=True)

#Assinatura do rodapé
st.sidebar.markdown("Pedro Henrique Ferreira da Silva - PDITA433", unsafe_allow_html=True)