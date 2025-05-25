from github_api import GithubApi
import csv
from datetime import datetime
def main():
    github_api = GithubApi()

    issues = github_api.get_all_rn_issues()
    filtered_issues = [
        issue for issue in issues if not any(
            label["name"] == "Resolution: Locked" or
            label["name"] == "Resolution: Answered" or
            label["name"] == "Resolution: Duplicate" or
            label["name"] == "Resolution: Cannot Reproduce" or
            label["name"] == "Resolution: For Stack Overflow" or
            label["name"] == "Resolution: Issue in another tool or repo" or
            label["name"] == "Needs: Triage :mag:"
            for label in issue["labels"]["nodes"]
        )
    ]

    for issue in filtered_issues:
        del issue["labels"]
        del issue["title"]
        del issue["url"]
        del issue["author"]
        print(f"#{issue['number']} - ({issue['createdAt']})")

    data_hoje = datetime.now().strftime("%Y-%m")
    nome_arquivo = f"rn_issues_{data_hoje}.csv"
    with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["number", "createdAt"])
        writer.writeheader()
        writer.writerows(filtered_issues)


if __name__ == "__main__":
    main()
