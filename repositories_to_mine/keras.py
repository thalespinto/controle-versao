from core.baseGithubApi import BaseGithubIssues


class KerasIssues(BaseGithubIssues):
    def get_repository_owner(self):
        return "keras-team"

    def get_repository_name(self):
        return "keras"

    def get_bug_labels(self):
        return '["type:Bug"]'

    def get_excluded_labels(self):
        return ["To investigate"]