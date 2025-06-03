from core.baseGithubApi import BaseGithubIssues


class NextcloudServerIssues(BaseGithubIssues):
    def get_repository_owner(self):
        return "nextcloud"

    def get_repository_name(self):
        return "server"

    def get_bug_labels(self):
        return '["bug"]'

    def get_excluded_labels(self):
        return ["0. Needs triage"]