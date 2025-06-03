from core.baseGithubApi import BaseGithubIssues


class OpenwrtIssues(BaseGithubIssues):
    def get_repository_owner(self):
        return "openwrt"

    def get_repository_name(self):
        return "openwrt"

    def get_bug_labels(self):
        return '["bug"]'

    def get_excluded_labels(self):
        return []