import pandas as pd

data_inicio = "2025-01-01"
data_fim = "2026-12-31"

sequencia_datas = pd.date_range(start=data_inicio, end=data_fim)

df = pd.DataFrame({'data': sequencia_datas})
df['ds_ano'] = df['data'].dt.year
df['mes_ano'] = df['data'].dt.strftime('%b/%y')

# Para deixar em maiúsculo, adicionamos .str.upper()
df['mes_ano'] = df['mes_ano'].str.upper()

# Opcional: Para remover o ponto de "Mai." ou "Set." (varia com o sistema)
df['mes_ano'] = df['mes_ano'].str.replace('.', '', regex=False)
print("### DataFrame criado ###")
print(df)

print("\n### Informações do DataFrame ###")
df.info()
df.to_csv(r'C:\Users\rafam\Desktop\Relatórios_Casiu\dados\dados_finais\dados_calendario.csv', index=False)