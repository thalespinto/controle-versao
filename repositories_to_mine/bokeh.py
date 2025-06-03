from core.baseGithubApi import BaseGithubIssues


class BokehIssues(BaseGithubIssues):
    def get_repository_owner(self):
        return "bokeh"

    def get_repository_name(self):
        return "bokeh"

    def get_bug_labels(self):
        return '["type: bug"]'

    def get_excluded_labels(self):
        return []