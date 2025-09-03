import pandas as pd
import os

caminho = "dados/"

arquivos = os.listdir(caminho)
lista_dfs = []
# Itera sobre cada arquivo CSV, lê e adiciona o DataFrame à lista
for arquivo in arquivos:
    caminho_arquivo = os.path.join(caminho, arquivo)
    try:
        df = pd.read_csv(caminho_arquivo)
        lista_dfs.append(df)
    except Exception as e:
        print(f"Erro ao ler o arquivo {arquivo}: {e}")

        # Concatena todos os DataFrames da lista em um único DataFrame
if lista_dfs:
    df_combinado = pd.concat(lista_dfs, ignore_index=True)

            # Salva o DataFrame combinado em um novo arquivo CSV
    df_combinado.to_csv('../dados/dados_finais/dados_combinados.csv', index=False)

    print("Arquivos CSV combinados com sucesso!")
    print("O arquivo combinado foi salvo como 'dados_combinados.csv'.")