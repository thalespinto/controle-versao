import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
from matplotlib.ticker import MaxNLocator  # Para melhor controle dos ticks do eixo X


def plotar_analises_consolidadas():  # Renomeada para refletir que plota mais de uma análise
    """
    Gera dois gráficos consolidados:
    1. Evolução anual de issues por repositório.
    2. Média anual de issues por período (Antes_2023, Depois_2023) por repositório.
    Os gráficos são salvos como imagens PNG.
    """
    pasta_entrada = "mine_results"
    pasta_saida_plots = os.path.join(pasta_entrada, "plots_contagem_anual")

    os.makedirs(pasta_saida_plots, exist_ok=True)

    # --- GRÁFICO 1: Evolução Anual de Issues por Repositório ---
    print("--- Gerando Gráfico 1: Evolução Anual de Issues ---")
    padrao_arquivos_contagem_anual = os.path.join(pasta_entrada, '*_contagem_anual.csv')
    arquivos_csv_contagem_anual = glob.glob(padrao_arquivos_contagem_anual)

    if not arquivos_csv_contagem_anual:
        print(f"  Nenhum arquivo CSV de contagem anual ('*_contagem_anual.csv') encontrado em '{pasta_entrada}'.")
    else:
        print(f"  📊 Encontrados {len(arquivos_csv_contagem_anual)} arquivos para o gráfico de evolução anual.")
        plt.figure(figsize=(15, 8))
        cores_anual = plt.cm.get_cmap('tab10', len(arquivos_csv_contagem_anual))

        for i, csv_file_path in enumerate(arquivos_csv_contagem_anual):
            try:
                base_name = os.path.basename(csv_file_path)
                # print(f"    -> Processando {base_name} para evolução anual...")
                df_contagem = pd.read_csv(csv_file_path)

                if 'ano' not in df_contagem.columns or 'numero_de_issues' not in df_contagem.columns:
                    print(
                        f"      Aviso: Colunas 'ano' ou 'numero_de_issues' não encontradas em '{base_name}'. Pulando.")
                    continue
                if df_contagem.empty:
                    print(f"      Aviso: DataFrame vazio para '{base_name}'. Pulando.")
                    continue

                df_contagem = df_contagem.sort_values(by='ano')
                nome_legenda = base_name.split('_')[0]
                plt.plot(df_contagem['ano'], df_contagem['numero_de_issues'],
                         marker='o', linestyle='-', label=nome_legenda, color=cores_anual(i))
            except Exception as e:
                print(f"      ❌ Erro ao processar '{base_name}' para evolução anual: {e}")

        plt.title('Evolução Anual de Issues por Repositório', fontsize=18)
        plt.xlabel('Ano', fontsize=14)
        plt.ylabel('Número de Issues', fontsize=14)
        plt.grid(True, linestyle='--', alpha=0.7)
        ax = plt.gca()
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        if arquivos_csv_contagem_anual:
            plt.legend(title="Repositório", bbox_to_anchor=(1.05, 1), loc='upper left')

        plt.xticks(rotation=45)
        plt.tight_layout(rect=[0, 0, 0.85, 1])

        plot_filename_anual = 'consolidado_evolucao_anual_issues.png'
        plot_output_path_anual = os.path.join(pasta_saida_plots, plot_filename_anual)
        try:
            plt.savefig(plot_output_path_anual)
            print(f"  ✅ Gráfico de evolução anual salvo como: {plot_output_path_anual}\n")
        except Exception as e:
            print(f"  ❌ Erro ao salvar o gráfico de evolução anual: {e}\n")
        plt.close()

    # --- GRÁFICO 2: Média Anual de Issues por Período por Repositório ---
    print("--- Gerando Gráfico 2: Média Anual de Issues por Período ---")
    padrao_arquivos_analise_periodo = os.path.join(pasta_entrada, '*_analise_periodo.csv')
    arquivos_csv_analise_periodo = glob.glob(padrao_arquivos_analise_periodo)

    if not arquivos_csv_analise_periodo:
        print(f"  Nenhum arquivo CSV de análise por período ('*_analise_periodo.csv') encontrado em '{pasta_entrada}'.")
        print("  Certifique-se de que o script 'analise.py' foi executado e gerou esses arquivos.")
    else:
        print(f"  📊 Encontrados {len(arquivos_csv_analise_periodo)} arquivos para o gráfico de média por período.")
        plt.figure(figsize=(12, 7))  # Tamanho pode ser ajustado
        cores_periodo = plt.cm.get_cmap('Dark2', len(arquivos_csv_analise_periodo))  # Outro mapa de cores

        for i, csv_file_path in enumerate(arquivos_csv_analise_periodo):
            try:
                base_name = os.path.basename(csv_file_path)
                # print(f"    -> Processando {base_name} para média por período...")
                df_periodo = pd.read_csv(csv_file_path)

                if 'periodo' not in df_periodo.columns or 'media_anual_issues_periodo' not in df_periodo.columns:
                    print(
                        f"      Aviso: Colunas 'periodo' ou 'media_anual_issues_periodo' não encontradas em '{base_name}'. Pulando.")
                    continue
                if df_periodo.empty:
                    print(f"      Aviso: DataFrame vazio para '{base_name}'. Pulando.")
                    continue

                # Garantir a ordem dos períodos se necessário (ex: Antes_2023, Depois_2023)
                # Se 'periodo' já estiver ordenado no CSV ou for apenas esses dois, pode não ser crucial
                # df_periodo['periodo'] = pd.Categorical(df_periodo['periodo'], categories=['Antes_2023', 'Depois_2023'], ordered=True)
                # df_periodo = df_periodo.sort_values('periodo')

                nome_legenda = base_name.split('_')[0]
                plt.plot(df_periodo['periodo'], df_periodo['media_anual_issues_periodo'],
                         marker='s', linestyle='--', label=nome_legenda, color=cores_periodo(i), linewidth=2)
            except Exception as e:
                print(f"      ❌ Erro ao processar '{base_name}' para média por período: {e}")

        plt.title('Média Anual de Issues por Período e Repositório', fontsize=18)
        plt.xlabel('Período', fontsize=14)
        plt.ylabel('Média Anual de Issues', fontsize=14)
        plt.grid(True, axis='y', linestyle=':', alpha=0.7)  # Grid apenas no eixo Y para clareza com categorias

        if arquivos_csv_analise_periodo:
            plt.legend(title="Repositório", bbox_to_anchor=(1.05, 1), loc='upper left')

        plt.tight_layout(rect=[0, 0, 0.85, 1])

        plot_filename_periodo = 'consolidado_media_anual_por_periodo.png'
        plot_output_path_periodo = os.path.join(pasta_saida_plots, plot_filename_periodo)
        try:
            plt.savefig(plot_output_path_periodo)
            print(f"  ✅ Gráfico de média por período salvo como: {plot_output_path_periodo}\n")
        except Exception as e:
            print(f"  ❌ Erro ao salvar o gráfico de média por período: {e}\n")
        plt.close()

    print(f"🏁 Processamento de gráficos concluído. Os gráficos foram salvos em: '{pasta_saida_plots}'")


if __name__ == "__main__":
    # Renomear a chamada da função se você renomeou a função
    plotar_analises_consolidadas()