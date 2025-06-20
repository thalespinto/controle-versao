import glob

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
import os


class AnalisadorDeIssues:
    """
    Uma classe para analisar a diferença no número de issues criadas
    entre dois períodos de tempo e visualizar os resultados.
    """

    def __init__(self, caminho_csv: str):
        """
        Inicializa o analisador carregando os dados do arquivo CSV.

        Args:
            caminho_csv (str): O caminho para o arquivo CSV com os dados das issues.
        """

        self.periodo_1 = ("2020-05-01", "2022-05-31")
        self.periodo_2 = ("2023-06-01", "2025-06-30")
        try:
            self.df = pd.read_csv(caminho_csv)
            self.df['createdAt'] = pd.to_datetime(self.df['createdAt'])
            print("Arquivo CSV carregado com sucesso!")
        except FileNotFoundError:
            print(f"Erro: O arquivo {caminho_csv} não foi encontrado.")
            self.df = None
        except KeyError:
            print(
                "Erro: A coluna 'createdAt' não foi encontrada no CSV. Por favor, verifique o nome da coluna no arquivo.")
            self.df = None

    def _get_contagens_mensais(self, data_inicio: str, data_fim: str) -> pd.Series:
        """
        Filtra o DataFrame por um período e retorna a contagem mensal de issues.
        """
        mask = (self.df['createdAt'] >= data_inicio) & (self.df['createdAt'] <= data_fim)
        df_periodo = self.df.loc[mask]
        df_periodo = df_periodo.set_index('createdAt')

        if df_periodo.empty:
            return pd.Series([], dtype=int)

        contagens_mensais = df_periodo.groupby(df_periodo.index.to_period('M')).size()
        return contagens_mensais

    def analisar_e_visualizar(self, nome_arquivo_saida):
        """
        Executa a análise completa, realiza o teste t e salva um boxplot.
        """
        with open(f"{nome_arquivo_saida}_logs.txt", 'w', encoding='utf-8') as f:
            if self.df is None:
                print("A análise não pode continuar porque o DataFrame não foi carregado.", file=f)
                return

            contagens_p1 = self._get_contagens_mensais(self.periodo_1[0], self.periodo_1[1])
            contagens_p2 = self._get_contagens_mensais(self.periodo_2[0], self.periodo_2[1])

            print("\n--- Resumo das Contagens Mensais ---", file=f)
            print(f"Período 1 ({self.periodo_1[0]} a {self.periodo_1[1]}):", file=f)
            if not contagens_p1.empty:
                print(contagens_p1.describe().to_string(), file=f)
            else:
                print("Nenhum dado encontrado para este período.", file=f)

            print(f"\nPeríodo 2 ({self.periodo_2[0]} a {self.periodo_2[1]}):", file=f)
            if not contagens_p2.empty:
                print(contagens_p2.describe().to_string(), file=f)
            else:
                print("Nenhum dado encontrado para este período.", file=f)

            if len(contagens_p1) < 2 or len(contagens_p2) < 2:
                print("\n--- Teste de Significância Estatística ---", file=f)
                print("Não é possível realizar o teste t: um ou ambos os períodos têm menos de duas amostras mensais.", file=f)
            else:
                t_stat, p_value = ttest_ind(contagens_p1, contagens_p2, equal_var=False)
                print("\n--- Teste de Significância Estatística ---", file=f)
                print(f"Estatística t: {t_stat:.4f}", file=f)
                print(f"P-valor: {p_value:.4f}", file=f)
                alpha = 0.05
                if p_value < alpha:
                    print(f"Conclusão: Existe uma diferença estatisticamente significativa.", file=f)
                else:
                    print(f"Conclusão: Não há evidências de uma diferença estatisticamente significativa.", file=f)

        plt.figure(figsize=(12, 8))
        sns.set_theme(style="whitegrid")

        df1 = pd.DataFrame({'contagem': contagens_p1, 'periodo': f'Período 1\n({self.periodo_1[0]} a {self.periodo_1[1]})'})
        df2 = pd.DataFrame({'contagem': contagens_p2, 'periodo': f'Período 2\n({self.periodo_2[0]} a {self.periodo_2[1]})'})

        df_plot = pd.concat([df1, df2])

        if not df_plot.empty:
            sns.boxplot(data=df_plot, x='periodo', y='contagem', palette="pastel", width=0.5)

            plt.title('Comparação Mensal de Issues Criadas', fontsize=16)
            plt.ylabel('Número de Issues por Mês', fontsize=12)
            plt.xlabel('Períodos', fontsize=12)
            plt.tight_layout()

            try:
                plt.savefig(f"{nome_arquivo_saida}_boxplot.png")
                print(f"\nGráfico salvo com sucesso como '{nome_arquivo_saida}_boxplot.png'")
            except Exception as e:
                print(f"\nOcorreu um erro ao salvar o gráfico: {e}")
        else:
            print("\nNenhum dado para plotar.")

    def define_boxplot_path(self, name):
        nome_do_arquivo = os.path.basename(name)
        nome_base, extensao = os.path.splitext(nome_do_arquivo)
        return nome_base


if __name__ == '__main__':
    mine_results_folder = "mine_results"
    csv_files_to_process = glob.glob(os.path.join(mine_results_folder, "*.csv"))

    for csv_path in csv_files_to_process:
        analisador = AnalisadorDeIssues(csv_path)
        print(os.path.join('generated_plots', analisador.define_boxplot_path(csv_path)))
        print(analisador.define_boxplot_path(csv_path))
        if analisador.df is not None:
            analisador.analisar_e_visualizar(os.path.join('generated_plots', analisador.define_boxplot_path(csv_path)))
