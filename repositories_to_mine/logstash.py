from core.baseGithubApi import BaseGithubIssues


class LogstashIssues(BaseGithubIssues):
    def get_repository_owner(self):
        return "elastic"

    def get_repository_name(self):
        return "logstash"

    def get_bug_labels(self):
        return '["bug", "status:confirmed"]'

    def get_excluded_labels(self):
        return []