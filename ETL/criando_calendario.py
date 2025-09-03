import pandas as pd
from datetime import datetime

data_inicio = "2025-01-01"
data_fim = "2026-12-31"

sequencia_datas = pd.date_range(start=data_inicio, end=data_fim)

df = pd.DataFrame({'data': sequencia_datas})
df['ds_ano'] = df['data'].dt.year
df['mes_ano'] = df['data'].dt.strftime('%b/%y').str.upper()

# Remove pontos, ex: "MAI." -> "MAI"
df['mes_ano'] = df['mes_ano'].str.replace('.', '', regex=False)

# ================================
# Criar diferença em meses em relação ao mês atual
# ================================
hoje = datetime.today()
ano_atual = hoje.year
mes_atual = hoje.month

# diferença = (ano*12 + mês) - (ano_atual*12 + mes_atual)
df['nr_diferenca_meses'] = (
    (df['ds_ano'] * 12 + df['data'].dt.month) -
    (ano_atual * 12 + mes_atual)
)

print("### DataFrame criado ###")
print(df.head(20))

print("\n### Informações do DataFrame ###")
df.info()

# Salvar no CSV
df.to_csv(r'C:\Users\rafam\OneDrive\Área de Trabalho\RelatóriosFinanceirosCASIU\dados\dados_finais\dados_calendario.csv', index=False)
