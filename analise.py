import pandas as pd
import os
import glob  # Adicionado para buscar arquivos


def main():
    folder = "mine_results"

    # Padrão para encontrar arquivos de issues
    # Busca por arquivos que terminam com "_issues_AAAA-MM.csv" ou "_issues.csv"
    padrao_arquivos_data = os.path.join(folder, '*_issues_*.csv')
    padrao_arquivos_simples = os.path.join(folder, '*_issues.csv')  # Para arquivos como react_issues.csv

    # Lista de arquivos de issues que não devem ser processados (se houver)
    # Ex: arquivos que já são resultado de análises anteriores
    arquivos_ignorados_padroes = ['*_contagem_anual.csv']
    # Adicione outros padrões se necessário

    todos_arquivos_csv = glob.glob(padrao_arquivos_data) + glob.glob(padrao_arquivos_simples)

    arquivos_csv_para_processar = []
    for f_path in todos_arquivos_csv:
        ignorar = False
        for padrao_ignorado in arquivos_ignorados_padroes:
            if glob.fnmatch.fnmatch(os.path.basename(f_path), padrao_ignorado):
                ignorar = True
                break
        if not ignorar:
            arquivos_csv_para_processar.append(f_path)

    if not arquivos_csv_para_processar:
        print(
            f"Nenhum arquivo CSV de issue para processar encontrado em '{folder}' (após ignorar arquivos de resultado).")
        return

    print("🔄 Processando arquivos de issues e gerando CSVs de contagem anual individuais:")
    for file_path in arquivos_csv_para_processar:
        try:
            print(f"\n  -> Processando arquivo: {os.path.basename(file_path)}")
            df_temp = pd.read_csv(file_path)

            date_column = None
            if 'createdAt' in df_temp.columns:
                date_column = 'createdAt'
            elif 'created_at' in df_temp.columns:
                date_column = 'created_at'
            # Adicione outras variações de nome de coluna de data se necessário
            # elif 'Date' in df_temp.columns:
            #     date_column = 'Date'

            if date_column:
                # Converter para datetime, remover timezone e extrair ano
                df_temp[date_column] = pd.to_datetime(df_temp[date_column], errors='coerce')
                df_temp.dropna(subset=[date_column], inplace=True)  # Remover linhas onde a data não pôde ser convertida

                if df_temp.empty:
                    print(
                        f"    Aviso: Nenhuma data válida encontrada em '{os.path.basename(file_path)}' após conversão. Pulando.")
                    continue

                if df_temp[date_column].dt.tz is not None:
                    df_temp[date_column] = df_temp[date_column].dt.tz_convert(None)

                df_temp['ano'] = df_temp[date_column].dt.year
                df_temp['ano'] = df_temp['ano'].astype(int)  # Garantir que o ano seja inteiro

                # Contar issues por ano para o arquivo atual
                contagem_anual_arquivo = df_temp.groupby('ano').size().reset_index(name='numero_de_issues')
                contagem_anual_arquivo = contagem_anual_arquivo.sort_values(by='ano')

                # Definir nome do arquivo de saída
                base_name = os.path.basename(file_path)
                name_sem_ext, ext = os.path.splitext(base_name)
                output_csv_name = f"{name_sem_ext}_contagem_anual.csv"  # Alterado para .csv
                output_csv_path = os.path.join(folder, output_csv_name)

                # Salvar o CSV de contagem anual para este arquivo
                contagem_anual_arquivo.to_csv(output_csv_path, index=False)
                print(f"    ✅ CSV de contagem anual salvo como: {output_csv_path}")

            else:
                print(
                    f"    Aviso: Coluna de data (ex: 'createdAt', 'created_at') não encontrada em '{os.path.basename(file_path)}'. Pulando este arquivo.")

        except Exception as e:
            print(f"    ❌ Erro ao processar o arquivo '{os.path.basename(file_path)}': {e}")

    print("\n🏁 Processamento concluído.")

    # A lógica anterior de combinar todos os DataFrames (df_completo) e as análises
    # detalhadas subsequentes (periodo, média_anual) foram removidas conforme
    # o novo requisito de gerar um CSV por arquivo de entrada.
    # Se precisar dessas análises de forma agregada ou por arquivo,
    # elas podem ser readaptadas.


if __name__ == "__main__":
    main()