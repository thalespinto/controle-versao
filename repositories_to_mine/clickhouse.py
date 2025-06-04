from core.baseGithubApi import BaseGithubIssues


class ClickhouseIssues(BaseGithubIssues):
    def get_repository_owner(self):
        return "clickhouse"

    def get_repository_name(self):
        return "clickhouse"

    def get_bug_labels(self):
        return '["bug"]'

    def get_excluded_labels(self):
        return []