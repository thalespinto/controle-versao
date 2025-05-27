import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
from matplotlib.ticker import MaxNLocator  # Para melhor controle dos ticks do eixo X


def plotar_contagem_consolidada_anual():
    """
    Lê todos os arquivos CSV de contagem anual de issues,
    plota todos em um único gráfico de linhas e salva como uma imagem PNG.
    """
    pasta_entrada = "mine_results"
    pasta_saida_plots = os.path.join(pasta_entrada, "plots_contagem_anual")

    # Criar a pasta de saída para os gráficos, se não existir
    os.makedirs(pasta_saida_plots, exist_ok=True)

    # Padrão para encontrar os arquivos CSV de contagem anual
    padrao_arquivos_csv = os.path.join(pasta_entrada, '*_contagem_anual.csv')
    arquivos_csv_contagem = glob.glob(padrao_arquivos_csv)

    if not arquivos_csv_contagem:
        print(f"Nenhum arquivo CSV de contagem anual ('*_contagem_anual.csv') encontrado em '{pasta_entrada}'.")
        print("Certifique-se de que o script 'analise.py' foi executado e gerou esses arquivos.")
        return

    print(f"📊 Encontrados {len(arquivos_csv_contagem)} arquivos de contagem anual para plotar no gráfico consolidado.")

    plt.figure(figsize=(15, 8))  # Figura única para todos os plots

    cores = plt.cm.get_cmap('tab10', len(arquivos_csv_contagem))  # Define um mapa de cores

    for i, csv_file_path in enumerate(arquivos_csv_contagem):
        try:
            base_name = os.path.basename(csv_file_path)
            print(f"  -> Processando arquivo para gráfico consolidado: {base_name}")

            df_contagem = pd.read_csv(csv_file_path)

            if 'ano' not in df_contagem.columns or 'numero_de_issues' not in df_contagem.columns:
                print(f"    Aviso: Colunas 'ano' ou 'numero_de_issues' não encontradas em '{base_name}'. Pulando.")
                continue

            if df_contagem.empty:
                print(f"    Aviso: DataFrame vazio para '{base_name}'. Pulando.")
                continue

            # Ordenar por ano para garantir que o gráfico de linha seja correto
            df_contagem = df_contagem.sort_values(by='ano')

            # Extrair nome para a legenda (primeira parte do nome do arquivo antes do '_')
            # Ex: 'mediamtx_issues_2025-05_contagem_anual.csv' -> 'mediamtx'
            # Ex: 'react_issues_contagem_anual.csv' -> 'react'
            nome_legenda = base_name.split('_')[0]

            plt.plot(df_contagem['ano'], df_contagem['numero_de_issues'],
                     marker='o', linestyle='-', label=nome_legenda, color=cores(i))

        except Exception as e:
            print(f"    ❌ Erro ao processar o arquivo '{base_name}' para o gráfico consolidado: {e}")

    # Configurações do gráfico consolidado
    plt.title('Evolução Anual de Issues por Repositório', fontsize=18)
    plt.xlabel('Ano', fontsize=14)
    plt.ylabel('Número de Issues', fontsize=14)

    plt.grid(True, linestyle='--', alpha=0.7)

    # Assegurar que os ticks do eixo X sejam inteiros (anos)
    ax = plt.gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Adicionar legenda
    if arquivos_csv_contagem:  # Só adiciona legenda se houver algo para plotar
        plt.legend(title="Repositório", bbox_to_anchor=(1.05, 1), loc='upper left')  # Coloca a legenda fora do gráfico

    plt.xticks(rotation=45)
    plt.tight_layout(
        rect=[0, 0, 0.85, 1])  # Ajusta o layout para não cortar os labels e dar espaço para legenda externa

    # Definir nome do arquivo de saída para o gráfico consolidado
    plot_filename = 'consolidado_evolucao_anual_issues.png'
    plot_output_path = os.path.join(pasta_saida_plots, plot_filename)

    try:
        plt.savefig(plot_output_path)
        print(f"\n✅ Gráfico consolidado salvo como: {plot_output_path}")
    except Exception as e:
        print(f"\n❌ Erro ao salvar o gráfico consolidado: {e}")

    plt.close()  # Fecha a figura para liberar memória

    print(f"\n🏁 Processamento de gráfico consolidado concluído. O gráfico foi salvo em: '{pasta_saida_plots}'")


if __name__ == "__main__":
    plotar_contagem_consolidada_anual()