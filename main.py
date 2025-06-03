from core.factory import GithubRepoFactory
import csv
from datetime import datetime
import os
import argparse

def export_to_csv(issues, repo_name):
    """
    Exports a list of issues to a CSV file.

    This function takes a list of issues and a repository name, and writes the issues
    to a CSV file. The CSV file will contain the fields 'number' and 'createdAt', and
    will be named using the format '{repo_name}_issues_{year-month}.csv'.

    :param issues: A list of issues to be written to the CSV
    :type issues: list of dict
    :param repo_name: The name of the repository to be used in the filename
    :type repo_name: str
    """
    os.makedirs("mine_results", exist_ok=True)
    filename = os.path.join("mine_results", f"{repo_name}_issues_{datetime.now().strftime('%Y-%m')}.csv")
    fieldnames = ['number', 'createdAt']
    if repo_name == "mui":
        fieldnames.append('is_duplicate')
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(issues)

def main(repo_name):
    try:
        handler = GithubRepoFactory.create(repo_name)
        issues = handler.get_all_filtered_issues()
        
        if repo_name == "mui":
            duplicates = handler.get_duplicates()
            print(f"Total de duplicates no MUI: {len(duplicates)}")
        
        export_to_csv(issues, repo_name)
        print(f"Arquivo gerado com {len(issues)} issues válidas")
        
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Mineração de issues de repositórios do GitHub")
    # parser.add_argument("repo_name", type=str, help="Nome do repositório a ser minerado")
    # args = parser.parse_args()

    repos = [
        "docusaurus",
        "mui",
        "react",
        "rn",
        "vscode",
        "flutter",
        'bokeh',
        'clickhouse',
        'gradle',
        'kera',
        'logstash',
        'metabase',
        'nextcloud_server',
        'openwrt',
        'qbittorrent',
        'roslyn',
    ]
    for repo in repos:
        print(f"Iniciando mineração do repositório: {repo}")
        main(repo)