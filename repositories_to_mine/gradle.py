from core.baseGithubApi import BaseGithubIssues


class GradleIssues(BaseGithubIssues):
    def get_repository_owner(self):
        return "gradle"

    def get_repository_name(self):
        return "gradle"

    def get_bug_labels(self):
        return '["a:bug"]'

    def get_excluded_labels(self):
        return ["to-triage"]