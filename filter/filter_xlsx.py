import pandas as pd
def main():
    file_path = "projets_with_1000_stars_or_more.xlsx"  # <<< COLOQUE O NOME CORRETO DO SEU ARQUIVO .XLSX AQUI
    sheet_name = 0

    date_column = 'createdAt'
    commits_column = 'commits'
    contributors_column = 'contributors'
    issues_column = 'issues'

    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        print(f"Arquivo '{file_path}' (planilha '{sheet_name}') carregado com sucesso. Total de {len(df)} repositórios.")

        required_columns = [date_column, commits_column, contributors_column]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"\n⚠️ Atenção: As seguintes colunas esperadas não foram encontradas na planilha: {missing_columns}")
            print(f"Por favor, verifique os nomes das colunas no seu arquivo Excel e ajuste as variáveis 'date_column', 'commits_column' e 'contributors_column' no script.")
            print(f"Colunas encontradas na planilha: {list(df.columns)}")
        else:
            try:
                df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
                df.dropna(subset=[date_column], inplace=True) # Remover linhas onde a conversão de data falhou
            except Exception as e:
                print(f"\n❌ Erro ao converter a coluna de data '{date_column}': {e}")
                print("Verifique se o nome da coluna de data está correto e se os dados estão em um formato de data reconhecível.")
                df = None

            if df is not None and not df.empty:
                # 2. Filtrar repositórios criados antes de novembro de 2020
                filter_date = pd.to_datetime('2020-05-01')
                condition_date = pd.to_datetime(df[date_column], errors='coerce', dayfirst=True) < filter_date

                # 3. Filtrar repositórios com mais de 10000 commits
                df[commits_column] = pd.to_numeric(df[commits_column], errors='coerce')
                condition_commits = df[commits_column] > 10000

                # 4. Filtrar repositórios com mais de 10 contribuidores
                df[contributors_column] = pd.to_numeric(df[contributors_column], errors='coerce')
                condition_contributors = df[contributors_column] > 10

                # 5. Filtrar repositório com mais de 5000 issues
                df[issues_column] = pd.to_numeric(df[issues_column], errors='coerce')
                condition_issues = df[issues_column] > 5000

                # Combinar todas as condições
                filtered_df = df[condition_date & condition_commits & condition_contributors & condition_issues]

                # Exibir os resultados
                print(f"\n📊 Foram encontrados {len(filtered_df)} repositórios que atendem aos critérios.")
                if not filtered_df.empty:
                    print("\nPrimeiros 5 repositórios filtrados:")
                    print(filtered_df.head())

                    # Salvar o DataFrame filtrado em um novo arquivo CSV
                    output_file_csv = 'repositorios_filtrados.csv'
                    filtered_df.to_csv(output_file_csv, index=False,
                                       encoding='utf-8-sig')  # encoding='utf-8-sig' é bom para compatibilidade com Excel
                    print(f"\n✅ Repositórios filtrados salvos em '{output_file_csv}'")
                else:
                    print("Nenhum repositório correspondeu a todos os critérios de filtragem.")

    except FileNotFoundError:
        print(f"❌ Erro: O arquivo '{file_path}' não foi encontrado.")
        print("Por favor, verifique se o nome e o caminho do arquivo estão corretos.")
    except ImportError:
        print(f"❌ Erro: A biblioteca 'openpyxl' (ou 'xlrd') não foi encontrada. Ela é necessária para ler arquivos Excel.")
        print("Você pode instalá-la com o comando: pip install openpyxl")
    except Exception as e:
        print(f"❌ Ocorreu um erro inesperado: {e}")

if __name__ == '__main__':
    main()