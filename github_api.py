import requests
import os
from dotenv import load_dotenv
load_dotenv()  

token = os.getenv("GITHUB_TOKEN")

class GithubApi:
    url = "https://api.github.com/graphql"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    def get(self, query):
        response = requests.post(self.url, json={"query": query}, headers=self.headers)
        if response.status_code == 200:
            return response.json()

        print("Erro:", response.status_code, response.text)

    def get_all_react_issues(self):
        all_issues = []
        has_next_page = True
        end_cursor = None

        while has_next_page:
            query = f"""
                {{
                  repository(owner: "facebook", name: "react") {{
                    issues(
                      first: 100,
                      labels: ["Type: Bug"],
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

            response = requests.post(self.url, json={"query": query}, headers=self.headers)
            if response.status_code != 200:
                print("Erro:", response.status_code, response.text)
                break

            data = response.json()
            issues = data["data"]["repository"]["issues"]["nodes"]
            all_issues.extend(issues)

            page_info = data["data"]["repository"]["issues"]["pageInfo"]
            has_next_page = page_info["hasNextPage"]
            end_cursor = page_info["endCursor"]

        print(f"Total de issues coletadas: {len(all_issues)}")
        return all_issues

    def get_all_vscode_issues(self):
        all_issues = []
        has_next_page = True
        end_cursor = None

        while has_next_page:
            query = f"""
                        {{
                          repository(owner: "microsoft", name: "vscode") {{
                            issues(
                              first: 100,
                              labels: ["bug"],
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

            response = requests.post(self.url, json={"query": query}, headers=self.headers)
            if response.status_code != 200:
                print("Erro:", response.status_code, response.text)
                break

            data = response.json()
            issues = data["data"]["repository"]["issues"]["nodes"]
            all_issues.extend(issues)

            page_info = data["data"]["repository"]["issues"]["pageInfo"]
            has_next_page = page_info["hasNextPage"]
            end_cursor = page_info["endCursor"]

        print(f"Total de issues coletadas: {len(all_issues)}")
        return all_issues

    def get_all_mui_issues(self):
        all_issues = []
        has_next_page = True
        end_cursor = None

        while has_next_page:
            query = f"""
                                {{
                                  repository(owner: "mui", name: "material-ui") {{
                                    issues(
                                      first: 100,
                                      labels: ["bug 🐛"],
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

            response = requests.post(self.url, json={"query": query}, headers=self.headers)
            if response.status_code != 200:
                print("Erro:", response.status_code, response.text)
                break

            data = response.json()
            issues = data["data"]["repository"]["issues"]["nodes"]
            all_issues.extend(issues)

            page_info = data["data"]["repository"]["issues"]["pageInfo"]
            has_next_page = page_info["hasNextPage"]
            end_cursor = page_info["endCursor"]

        print(f"Total de issues coletadas: {len(all_issues)}")
        return all_issues

    def get_all_rn_issues(self):
        all_issues = []
        has_next_page = True
        end_cursor = None

        while has_next_page:
            query = f"""
                                {{
                                  repository(owner: "facebook", name: "react-native") {{
                                    issues(
                                      first: 100,
                                      labels: ["Bug"],
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

            response = requests.post(self.url, json={"query": query}, headers=self.headers)
            if response.status_code != 200:
                print("Erro:", response.status_code, response.text)
                break

            data = response.json()
            issues = data["data"]["repository"]["issues"]["nodes"]
            all_issues.extend(issues)

            page_info = data["data"]["repository"]["issues"]["pageInfo"]
            has_next_page = page_info["hasNextPage"]
            end_cursor = page_info["endCursor"]

        print(f"Total de issues coletadas: {len(all_issues)}")
        return all_issues

    def get_all_docusaurus_issues(self):
        all_issues = []
        has_next_page = True
        end_cursor = None

        while has_next_page:
            query = f"""
                                {{
                                  repository(owner: "facebook", name: "docusaurus") {{
                                    issues(
                                      first: 100,
                                      labels: ["bug"],
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

            response = requests.post(self.url, json={"query": query}, headers=self.headers)
            if response.status_code != 200:
                print("Erro:", response.status_code, response.text)
                break

            data = response.json()
            issues = data["data"]["repository"]["issues"]["nodes"]
            all_issues.extend(issues)

            page_info = data["data"]["repository"]["issues"]["pageInfo"]
            has_next_page = page_info["hasNextPage"]
            end_cursor = page_info["endCursor"]

        print(f"Total de issues coletadas: {len(all_issues)}")
        return all_issues