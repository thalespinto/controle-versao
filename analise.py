import pandas as pd
import os
import glob


def main():
    folder = "mine_results"

    padrao_arquivos_data = os.path.join(folder, '*_issues_*.csv')
    padrao_arquivos_simples = os.path.join(folder, '*_issues.csv')

    arquivos_ignorados_padroes = [
        '*_contagem_anual.csv',
        '*_analise_periodo.csv'  # Novo padrão para ignorar
    ]

    todos_arquivos_csv_issues = glob.glob(padrao_arquivos_data) + glob.glob(padrao_arquivos_simples)

    arquivos_csv_para_processar = []
    for f_path in todos_arquivos_csv_issues:
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

    print("🔄 Processando arquivos de issues...")
    for file_path in arquivos_csv_para_processar:
        try:
            base_name_original_file = os.path.basename(file_path)
            print(f"\n  -> Processando arquivo: {base_name_original_file}")
            df_temp = pd.read_csv(file_path)

            date_column = None
            if 'createdAt' in df_temp.columns:
                date_column = 'createdAt'
            elif 'created_at' in df_temp.columns:
                date_column = 'created_at'

            if date_column:
                df_temp[date_column] = pd.to_datetime(df_temp[date_column], errors='coerce')
                df_temp.dropna(subset=[date_column], inplace=True)

                if df_temp.empty:
                    print(f"    Aviso: Nenhuma data válida em '{base_name_original_file}' após conversão. Pulando.")
                    continue

                if df_temp[date_column].dt.tz is not None:
                    df_temp[date_column] = df_temp[date_column].dt.tz_convert(None)

                df_temp['ano'] = df_temp[date_column].dt.year
                df_temp['ano'] = df_temp['ano'].astype(int)

                # --- 1. Gerar CSV de contagem anual para este arquivo (como antes) ---
                contagem_anual_arquivo = df_temp.groupby('ano').size().reset_index(name='numero_de_issues')
                contagem_anual_arquivo = contagem_anual_arquivo.sort_values(by='ano')

                name_sem_ext, _ = os.path.splitext(base_name_original_file)
                output_csv_name_anual = f"{name_sem_ext}_contagem_anual.csv"
                output_csv_path_anual = os.path.join(folder, output_csv_name_anual)

                contagem_anual_arquivo.to_csv(output_csv_path_anual, index=False)
                print(f"    ✅ CSV de contagem anual salvo: {output_csv_path_anual}")

                # --- 2. Análise por período para este arquivo ---
                print(f"    🔍 Realizando análise por período para: {base_name_original_file}")

                # Criar uma cópia para a análise de período para não afetar df_temp original para outras possíveis análises
                df_analise_periodo = df_temp.copy()

                # Aplicar filtros:
                # 2a. Ignorar 2025 (e anos posteriores)
                df_analise_periodo = df_analise_periodo[df_analise_periodo['ano'] < 2025]

                if df_analise_periodo.empty:
                    print(
                        f"      Aviso: Nenhum dado para '{base_name_original_file}' após filtro 'ano < 2025'. Análise de período não gerada.")
                    continue

                # 2b. Ignorar o menor ano (após o filtro de 2025)
                menor_ano = df_analise_periodo['ano'].min()
                df_analise_periodo_filtrado = df_analise_periodo[df_analise_periodo['ano'] != menor_ano]
                print(f"      Filtros para período: Ano < 2025, Menor ano ignorado: {menor_ano}")

                if df_analise_periodo_filtrado.empty:
                    print(
                        f"      Aviso: Nenhum dado para '{base_name_original_file}' após remover o menor ano ({menor_ano}). Análise de período não gerada.")
                    continue

                # 2c. Criar coluna 'periodo'
                df_analise_periodo_filtrado['periodo'] = df_analise_periodo_filtrado['ano'].apply(
                    lambda x: 'Antes_2023' if x < 2023 else 'Depois_2023'
                )

                # 2d. Calcular contagem total de issues por período
                contagem_total_periodo = df_analise_periodo_filtrado.groupby('periodo').size().reset_index(
                    name='total_issues_periodo')

                # 2e. Calcular média anual de issues por período
                # Primeiro, contar issues por ano dentro de cada período
                issues_por_ano_periodo = df_analise_periodo_filtrado.groupby(['periodo', 'ano']).size().reset_index(
                    name='issues_no_ano')
                # Depois, calcular a média dessas contagens anuais para cada período
                media_anual_periodo = issues_por_ano_periodo.groupby('periodo')['issues_no_ano'].mean().reset_index(
                    name='media_anual_issues_periodo')

                # Formatar a média para 2 casas decimais
                media_anual_periodo['media_anual_issues_periodo'] = media_anual_periodo[
                    'media_anual_issues_periodo'].round(2)

                if contagem_total_periodo.empty and media_anual_periodo.empty:
                    print(
                        f"      Aviso: Nenhum dado de período para '{base_name_original_file}' após filtros. Análise de período não gerada.")
                    continue

                # Juntar os resultados (contagem total e média anual)
                if not contagem_total_periodo.empty and not media_anual_periodo.empty:
                    df_resultado_periodo = pd.merge(contagem_total_periodo, media_anual_periodo, on='periodo',
                                                    how='outer')
                elif not contagem_total_periodo.empty:
                    df_resultado_periodo = contagem_total_periodo
                    df_resultado_periodo['media_anual_issues_periodo'] = pd.NA  # ou 0, ou float('nan')
                elif not media_anual_periodo.empty:  # Caso menos provável sem contagem total
                    df_resultado_periodo = media_anual_periodo
                    df_resultado_periodo['total_issues_periodo'] = pd.NA  # ou 0, ou float('nan')
                else:  # Ambos vazios, embora já verificado acima
                    print(
                        f"      Aviso: Nenhum dado de período para '{base_name_original_file}' após filtros. Análise de período não gerada.")
                    continue

                output_csv_name_periodo = f"{name_sem_ext}_analise_periodo.csv"
                output_csv_path_periodo = os.path.join(folder, output_csv_name_periodo)

                df_resultado_periodo.to_csv(output_csv_path_periodo, index=False)
                print(f"    ✅ CSV de análise por período salvo: {output_csv_path_periodo}")
                print(f"      Conteúdo de {output_csv_name_periodo}:")
                print(df_resultado_periodo.to_string())


            else:  # Se date_column não foi encontrada
                print(
                    f"    Aviso: Coluna de data (ex: 'createdAt', 'created_at') não encontrada em '{base_name_original_file}'. Pulando este arquivo.")

        except Exception as e:
            print(f"    ❌ Erro ao processar o arquivo '{base_name_original_file}': {e}")

    print("\n🏁 Processamento concluído.")


if __name__ == "__main__":
    main()