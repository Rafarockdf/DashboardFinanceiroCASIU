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

############ ETL ##################
dados['vl_transacao'] = pd.to_numeric(dados['vl_transacao'], errors='coerce')
dados['dt_transacao'] = pd.to_datetime(dados['dt_transacao'], format="%d-%m-%Y")

# =================================================================
#               ADICIONE ESTE BLOCO PARA DEBUG
# =================================================================
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

############ Métricas #############
# (seu código continua aqui...)



############ Métricas #############

faturamento_total = dados[dados['vl_transacao'] > 0]['vl_transacao'].sum()
custo_total = abs(dados[dados['vl_transacao'] < 0]['vl_transacao'].sum())
lucro_liquido = faturamento_total - custo_total
margem_lucro = ((faturamento_total - custo_total) / faturamento_total) * 100
faturamento_anterior = 1000
faturamento_por_categoria = 1

# 1. Crie um DataFrame contendo apenas as receitas (transações > 0)
receitas = dados[dados['vl_transacao'] > 0].copy()
# 2. Agora, agrupe e some a partir deste novo DataFrame de receitas
faturamento_por_categoria = receitas.groupby('ds_transacao')['vl_transacao'].sum()
#faturamento_por_categoria = pd.DataFrame(faturamento_por_categoria)
###################################


############ Gráficos #############
categorias = faturamento_por_categoria.index
valores = faturamento_por_categoria.values

# 1. Ordenar os dados para o gráfico (da maior categoria para a menor)
# O resultado do groupby já é uma Series (índice=categoria, valor=faturamento)

# 2. Criar a figura do gráfico, passando a Series ordenada DIRETAMENTE
fig_faturamento_por_categorias = px.bar(
    faturamento_por_categoria,
    x=categorias,
    y=valores,
    
    # --- PERSONALIZAÇÃO PRINCIPAL ---
    title="<b>Faturamento por Categoria</b>", # Título mais descritivo
    labels={
        "x": "Categoria da Transação",
        "y": "Faturamento (R$)"
    },
    color=categorias,
    text_auto=True
)

# 3. Ajustes finos de layout e formatação dos textos
fig_faturamento_por_categorias.update_layout(
    title_x=0.5,
    xaxis_title_font_size=14,
    yaxis_title_font_size=14,
    font_family="Arial",
    template="plotly_white",
    showlegend=False # Oculta a legenda, pois as cores já são distintas
)

# Formata o texto em cima das barras para o formato de moeda R$
# O 'y' se refere ao valor no eixo y. O ':,.2f' formata com separador de milhar e 2 casas decimais.
fig_faturamento_por_categorias.update_traces(texttemplate='R$ %{y:,.2f}', textposition='outside')

###################################


st.title('Relatório CASIU')
col1_metrica, col2_metrica, col3_metrica,col4_metrica = st.columns(4)
col1_grafico, col2_grafico = st.columns(2)
col1_metrica.metric(
        label="Faturamento Total",
        value=f"R$ {faturamento_total:.2f}",
        delta=f"R$ {faturamento_total - faturamento_anterior:.2f}",
        help="Soma de todas as entradas positivas."
    )
col2_metrica.metric(
        label="Custo Total",
        value=f"R$ {custo_total:.2f}",
        delta=f"R$ {faturamento_total - faturamento_anterior:.2f}",
        help="Soma de todas as entradas negativas."
    )
col3_metrica.metric(
        label="Lucro Líquido",
        value=f"R$ {lucro_liquido:.2f}",
        delta=f"R$ {faturamento_total - faturamento_anterior:.2f}",
        help="Diferença entre faturamento e custos."
    )
#Margem de Lucro (%) = [(Preço de Venda - Custos Totais) / Preço de Venda] x 100
col4_metrica.metric(
        label="Margem de Lucro",
        value=f"{margem_lucro:.2f}%",
        delta=f"R$ {faturamento_total - faturamento_anterior:.2f}",
        help="Percentual de lucro em relação ao faturamento."
    )

col1_grafico.plotly_chart(fig_faturamento_por_categorias, use_container_width=True)