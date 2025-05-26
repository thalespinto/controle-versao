import requests
import os
from dotenv import load_dotenv
from abc import ABC, abstractmethod

load_dotenv()

class BaseGithubIssues(ABC):
    BASE_URL = "https://api.github.com/graphql"
    
    def __init__(self):
        """
        Inicializa a classe com o token de acesso ao GitHub.

        :param:
            None

        :return:
            None
        """
        self.token = os.getenv("GITHUB_TOKEN")
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    @abstractmethod
    def get_repository_owner(self):
        """
        Retorna o nome do proprietário do repositório.

        :return:
            String com o nome do proprietário do repositório
        """
        pass
    
    @abstractmethod
    def get_repository_name(self):
        """
        Retorna o nome do repositório.

        :return:
            String com o nome do repositório
        """
        pass
    
    @abstractmethod
    def get_bug_labels(self):
        """
        Retorna uma lista de labels de defeitos/bugs do repositório.
        Se uma issue tiver ao menos uma dessas labels, ela será considerada um bug.

        :return:
            Uma lista de strings, cada string representando uma label de bug
        """
        pass
    
    def get_excluded_labels(self):
        """
        Retorna uma lista de labels de exclusão.
        Qualquer issue que contenha ao menos uma dessas labels será excluída dos resultados filtrados.

        :return:
            Uma lista de strings, cada string representando uma label de exclusão
        """
        return []
    
    def get_special_filters(self):
        """
        Retorna uma lista de funções de filtro especiais.
        Essas funções receberão uma issue como parâmetro e devem retornar True se a issue deve ser incluída e False caso contrário.
        Qualquer issue rejeitada por uma dessas funções será excluída dos resultados filtrados.

        :return:
            Uma lista de funções de filtro especiais
        """
        return []
    
    def post_process_issue(self, issue):
        """
        Função que remove as chaves "labels", "title", "url" e "author" de uma issue, caso existam.
        Isso é feito para padronizar a forma como as issues são armazenadas e para evitar que
        informações desnecessárias sejam incluídas nos relatórios.

        :param issue: Uma issue do GitHub
        :type issue: dict
        :return: A issue sem as chaves mencionadas acima
        :rtype: dict
        """
        issue.pop("labels", None)
        issue.pop("title", None)
        issue.pop("url", None)
        issue.pop("author", None)
        return issue
    
    def get_all_filtered_issues(self):
        """
        Retrieves all issues from the repository, applies specified filters, and returns a list of processed issues.

        This function fetches raw issues from the repository using `_fetch_raw_issues()`, applies filters defined
        in `_apply_filters()` to exclude unwanted issues based on labels and special filter functions, and then
        processes each issue using `post_process_issue()` to remove unnecessary information.

        :return: A list of filtered and processed issues from the repository
        :rtype: list of dict
        """
        raw_issues = self._fetch_raw_issues()
        filtered = self._apply_filters(raw_issues)
        return [self.post_process_issue(issue) for issue in filtered]
    
    def _fetch_raw_issues(self):
        """
        Fetches all issues from the repository using the GraphQL API.

        This function builds a GraphQL query using `_build_query()` and sends it to the GitHub API using
        `_make_graphql_request()`. It then extracts the issues from the response and stores them in a list.
        The function repeats this process until it has fetched all issues from the repository.

        :return: A list of raw issues from the repository
        :rtype: list of dict
        """
        
        all_issues = []
        has_next_page = True
        end_cursor = None

        while has_next_page:
            query = self._build_query(end_cursor)
            data = self._make_graphql_request(query)
            
            if not data:
                break

            issues = data["data"]["repository"]["issues"]["nodes"]
            all_issues.extend(issues)

            page_info = data["data"]["repository"]["issues"]["pageInfo"]
            has_next_page = page_info["hasNextPage"]
            end_cursor = page_info["endCursor"]

        print(f"[{self.get_repository_name()}] Issues brutas coletadas: {len(all_issues)}")
        return all_issues
    
    def _apply_filters(self, issues):
        
        """
        Applies filters to the list of issues.

        This function takes a list of issues and applies filters to it. The filters are defined in the
        `get_excluded_labels()` and `get_special_filters()` methods. The function returns the filtered
        list of issues.

        :param issues: The list of issues to filter
        :type issues: list of dict
        :return: The filtered list of issues
        :rtype: list of dict
        """
        filtered = issues
        
        if excluded := self.get_excluded_labels():
            filtered = [i for i in filtered if not any(
                label["name"] in excluded for label in i["labels"]["nodes"]
            )]
        
        for special_filter in self.get_special_filters():
            filtered = list(filter(special_filter, filtered))
            
        print(f"[{self.get_repository_name()}] Issues após filtros: {len(filtered)}")
        return filtered
    
    def _build_query(self, end_cursor=None):
        """
        Builds a GraphQL query for fetching issues from the repository.

        The query fetches the first 100 issues from the repository, filtered by the labels returned
        by `get_bug_labels()`. The issues are ordered by creation date in descending order.

        If `end_cursor` is provided, the query includes a pagination cursor to fetch the next page of
        issues.

        :param end_cursor: The pagination cursor for the next page of issues
        :type end_cursor: str
        :return: The GraphQL query as a string
        :rtype: str
        """
        return f"""
        {{
          repository(owner: "{self.get_repository_owner()}", name: "{self.get_repository_name()}") {{
            issues(
              first: 100,
              labels: {self.get_bug_labels()},
              states: [OPEN, CLOSED],
              orderBy: {{field: CREATED_AT, direction: DESC}}
              {f', after: "{end_cursor}"' if end_cursor else ""}
            ) {{
              nodes {{
                title
                number
                url
                createdAt
                labels(first: 20) {{
                  nodes {{
                    name
                  }}
                }}
                author {{
                  login
                }}
              }}
              pageInfo {{
                endCursor
                hasNextPage
              }}
            }}
          }}
        }}
        """
    
    def _make_graphql_request(self, query):
        """
        Makes a GraphQL request to the GitHub API using the provided query.

        The request is sent using the `requests` library and the response is parsed
        as JSON. If the response is successful (200 status code), the function
        returns the parsed JSON response. Otherwise, it prints an error message
        with the status code and response text.

        :param query: The GraphQL query as a string
        :type query: str
        :return: The parsed JSON response if the request was successful, None otherwise
        :rtype: dict or None
        """
        response = requests.post(self.BASE_URL, json={"query": query}, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        print("Erro:", response.status_code, response.text)
        return None