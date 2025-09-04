import streamlit as st 
import pandas as pd
import plotly.express as px

#import plotly
st.set_page_config(page_title='Relatório CASIU',layout='wide',page_icon='imagens/logo-casiu-png.png')
dados = pd.read_csv('dados/dados_finais/dados_combinados.csv')
calendario = pd.read_csv('dados/dados_finais/dados_calendario.csv')
############ ETL ##################
dados['vl_transacao'] = pd.to_numeric(dados['vl_transacao'], errors='coerce')
dados['dt_transacao'] = pd.to_datetime(dados['dt_transacao'], format="%d-%m-%Y")
###################################


# =================================================================
#               ADICIONE ESTE BLOCO PARA DEBUG
# =================================================================
debug='''
st.markdown("---")
st.header("🕵️‍♂️ Área de Debug")

st.subheader("1. Amostra dos dados lidos do CSV:")
st.write(f"O DataFrame 'dados' tem {dados.shape[0]} linhas.")
st.dataframe(dados.head())

st.subheader("2. Análise da coluna 'vl_transacao' (após conversão):")
st.write(dados['vl_transacao'].describe())

st.subheader("3. DataFrame 'receitas' (após filtrar transações > 0):")
receitas_debug = dados[dados['vl_transacao'] > 0].copy()
st.write(f"O DataFrame 'receitas' tem {receitas_debug.shape[0]} linhas.")
st.dataframe(receitas_debug.head())

faturamento_por_categoria = receitas_debug.groupby('ds_transacao')['vl_transacao'].sum()
st.dataframe(faturamento_por_categoria)
st.markdown("---")
# =================================================================
#                       FIM DO BLOCO DE DEBUG
# =================================================================
'''
############ Métricas #############
# (seu código continua aqui...)
st.title('Relatório CASIU')
col1_metrica, col2_metrica, col3_metrica,col4_metrica = st.columns(4)
col1_grafico, col2_grafico = st.columns(2)

sidebar = st.sidebar.header('Filtros')

# Pega os valores únicos da coluna mes_ano, ordena e transforma em lista
# 1. Primeiro, ordene o DataFrame 'calendario' pela coluna de data real
calendario_ordenado = calendario.sort_values(by='data')

# 2. Agora sim, extraia os meses únicos. O pandas manterá a ordem da primeira aparição.
lista_meses = list(calendario_ordenado['mes_ano'].unique())
lista_meses.insert(0,'Todos')

with sidebar:
    st.write('Filtros')
    mes_selecionado = st.sidebar.selectbox(
        "Selecione o Mês",
        options=lista_meses
    )
    
    
if mes_selecionado != 'Todos':
    mask_meses = calendario_ordenado['mes_ano'] == mes_selecionado
    data_min = calendario_ordenado[mask_meses]['data'].min()
    data_max = calendario_ordenado[mask_meses]['data'].max()
        
else:
    data_min = calendario_ordenado['data'].min()
    data_max = calendario_ordenado['data'].max()
    faturamento_anterior = 0
    lucro_anterior = 0
    custo_anterior = 0
    margem_lucro_anterior = 0
        
        
# Aplica a máscara ao DataFrame principal
mascara_data = (dados['dt_transacao'] >= pd.to_datetime(data_min)) & (dados['dt_transacao'] <= pd.to_datetime(data_max))
dados_filtrados = dados.loc[mascara_data]

############ Métricas #############

faturamento_total = dados_filtrados[dados_filtrados['vl_transacao'] > 0]['vl_transacao'].sum()
custo_total = abs(dados_filtrados[dados_filtrados['vl_transacao'] < 0]['vl_transacao'].sum())
lucro_liquido = faturamento_total - custo_total
margem_lucro = ((faturamento_total - custo_total) / faturamento_total) * 100
if mes_selecionado != "Todos":
    mask_mes = calendario_ordenado['mes_ano'] ==  mes_selecionado
    
    num_mes_selecionado_lista = list(calendario_ordenado[mask_mes]['nr_diferenca_meses'])
    num_mes_selecionado = num_mes_selecionado_lista[0]
        # --- PASSO 2: Calcular o número correspondente ao mês anterior ---
    num_mes_anterior = num_mes_selecionado - 1
    # --- PASSO 3: Usar o novo número para encontrar as datas do mês anterior ---
    mask_mes_anterior = calendario_ordenado['nr_diferenca_meses'] == num_mes_selecionado - 1
    # Verifica se existe um mês anterior nos dados
        # Filtra o calendário para pegar todas as linhas do mês anterior
    df_mes_anterior = calendario_ordenado[mask_mes_anterior]

        # Pega a data mínima e máxima desse novo dataframe filtrado
    data_min_anterior = df_mes_anterior['data'].min()
    data_max_anterior = df_mes_anterior['data'].max()

    st.success("Mês anterior encontrado!")

    # Aplica a máscara ao DataFrame principal
    mascara_data_anterior = (dados['dt_transacao'] >= pd.to_datetime(data_min_anterior)) & (dados['dt_transacao'] <= pd.to_datetime(data_max_anterior))
    dados_filtrados_anterior = dados.loc[mascara_data_anterior]

    faturamento_anterior = dados_filtrados_anterior[dados_filtrados_anterior['vl_transacao'] > 0]['vl_transacao'].sum()

    custo_anterior = abs(dados_filtrados_anterior[dados_filtrados_anterior['vl_transacao'] < 0]['vl_transacao'].sum())
    lucro_anterior= faturamento_anterior - custo_anterior
    margem_lucro_anterior = ((faturamento_anterior - custo_anterior) / faturamento_anterior) * 100
    
    
else:
    faturamento_anterior = 0
    lucro_anterior = 0
    custo_anterior = 0
    margem_lucro_anterior = 0

# 1. Crie um DataFrame contendo apenas as receitas (transações > 0)
receitas = dados_filtrados[dados_filtrados['vl_transacao'] > 0].copy()
# 2. Agora, agrupe e some a partir deste novo DataFrame de receitas
faturamento_por_categoria = receitas.groupby('ds_transacao')['vl_transacao'].sum()
faturamento_por_tempo = receitas.groupby('dt_transacao')['vl_transacao'].sum()


###################################


############ Gráficos #############
categorias = faturamento_por_categoria.index
valores = faturamento_por_categoria.values

# 1. Ordenar os dados para o gráfico (da maior categoria para a menor)
# O resultado do groupby já é uma Series (índice=categoria, valor=faturamento)

# 2. Criar a figura do gráfico, passando a Series ordenada DIRETAMENTE
df_grafico_faturamento_por_categorias = faturamento_por_categoria.reset_index().sort_values(by='vl_transacao', ascending=False)

# 3. Criar a figura do gráfico, passando o DataFrame e os NOMES das colunas
fig_faturamento_por_categorias = px.bar(
    df_grafico_faturamento_por_categorias,  # <--- Passando o DataFrame aqui
    x='ds_transacao', # <--- Nome da coluna para o eixo X
    y='vl_transacao', # <--- Nome da coluna para o eixo Y
    
    title="<b>Faturamento por Categoria</b>",
    labels={
        "ds_transacao": "Categorias",  # <--- Agora o mapeamento funciona perfeitamente
        "vl_transacao": "Faturamento (R$)"
    },
    color='ds_transacao', # Você também pode usar o nome da coluna aqui
    text_auto=True
)

# 4. Seus ajustes de layout continuam os mesmos
fig_faturamento_por_categorias.update_layout(
    title={
        'text': "📊 Faturamento por Categoria",  # título
        'x': 0.5,  # centraliza
        'xanchor': 'center',
        'yanchor': 'top'
    },
    title_font=dict(size=24, color="white"),  # aumenta fonte
    title_pad=dict(t=20),  # espaçamento superior
    title_x=0.5, # Centraliza o título
    font_family="Arial",
    template="plotly_white", # Temas: "plotly_dark", "ggplot2", "seaborn", etc.
    legend_title_text='Produtos' # Muda o título da legenda
    # ... (seu código de update_layout continua igual)
)
fig_faturamento_por_categorias.update_traces(texttemplate='R$ %{y:,.2f}', textposition='outside')



df_grafico_faturamento_por_tempo = faturamento_por_tempo.reset_index().sort_values(by='dt_transacao', ascending=False)
fig_faturamento_por_tempo = px.line(
    # --- DADOS ---
    df_grafico_faturamento_por_tempo, # Passando o DataFrame completo
    x='dt_transacao',
    y='vl_transacao',
    
    # --- PERSONALIZAÇÃO PRINCIPAL ---
    title="<b>Faturamento Por Tempo</b>",
    
    labels={
        "dt_transacao": "Data da Venda",
        "vl_transacao": "Faturamento (R$)"
    },

    markers=True # Adiciona marcadores (pontos) em cada ponto de dado na linha
)

# ==============================================================================
# 3. AJUSTES FINOS DE LAYOUT (Opcional)
# ==============================================================================

fig_faturamento_por_tempo.update_layout(
    title={
        'text': "📊 Faturamento por Tempo",  # título
        'x': 0.5,  # centraliza
        'xanchor': 'center',
        'yanchor': 'top'
    },
    title_font=dict(size=24, color="white"),  # aumenta fonte
    title_pad=dict(t=20),  # espaçamento superior
    title_x=0.5, # Centraliza o título
    font_family="Arial",
    template="plotly_white", # Temas: "plotly_dark", "ggplot2", "seaborn", etc.
    legend_title_text='Produtos' # Muda o título da legenda
)

###################################

col1_metrica.metric(
        label="Faturamento Total",
        value=f"R$ {faturamento_total:.2f}",
        delta=f"R$ {faturamento_total - faturamento_anterior:.2f}",
        help="Soma de todas as entradas positivas."
    )
col2_metrica.metric(
        label="Custo Total",
        value=f"R$ {custo_total:.2f}",
        delta=f"R$ {custo_total - custo_anterior:.2f}",
        help="Soma de todas as entradas negativas."
    )
col3_metrica.metric(
        label="Lucro Líquido",
        value=f"R$ {lucro_liquido:.2f}",
        delta=f"R$ {lucro_liquido - lucro_anterior:.2f}",
        help="Diferença entre faturamento e custos."
    )
#Margem de Lucro (%) = [(Preço de Venda - Custos Totais) / Preço de Venda] x 100
col4_metrica.metric(
        label="Margem de Lucro",
        value=f"{margem_lucro:.2f}%",
        delta=f"R$ {margem_lucro - margem_lucro_anterior:.2f}",
        help="Percentual de lucro em relação ao faturamento."
    )

col1_grafico.plotly_chart(fig_faturamento_por_categorias, use_container_width=True)
col2_grafico.plotly_chart(fig_faturamento_por_tempo, use_container_width=True)


