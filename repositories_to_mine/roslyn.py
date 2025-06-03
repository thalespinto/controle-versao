from core.baseGithubApi import BaseGithubIssues


class RoslynIssues(BaseGithubIssues):
    def get_repository_owner(self):
        return "dotnet"

    def get_repository_name(self):
        return "roslyn"

    def get_bug_labels(self):
        return '["Bug"]'

    def get_excluded_labels(self):
        return []