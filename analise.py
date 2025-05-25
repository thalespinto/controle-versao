import pandas as pd


def main():
    # Carrega o CSV
    df = pd.read_csv("docusaurus_issues_2025-05.csv")

    # Converte a coluna 'createdAt' para datetime
    df['createdAt'] = pd.to_datetime(df['createdAt'])

    # Verifica se os dados têm timezone; remove se tiver
    if df['createdAt'].dt.tz is not None:
        df['createdAt'] = df['createdAt'].dt.tz_convert(None)

    # Cria uma coluna com o ano
    df['ano'] = df['createdAt'].dt.year
    df = df[df['ano'] < 2025]
    menor_ano = df['ano'].min()
    df = df[df['ano'] != menor_ano]
    # Define o período (antes ou depois de 2023)
    df['periodo'] = df['ano'].apply(lambda x: 'Antes_2023' if x < 2023 else 'Depois_2023')

    # Agrupa por ano e conta quantas issues em cada ano
    contagem_por_ano = df.groupby(['periodo', 'ano']).size()

    print("📊 Contagem de issues por ano:\n")
    print(contagem_por_ano)

    # Calcula média anual por período
    media_anual = contagem_por_ano.groupby(level=0).mean()

    print("\n📈 Média anual de issues por período:\n")
    print(media_anual)


if __name__ == "__main__":
    main()
