from core.baseGithubApi import BaseGithubIssues


class MetabaseIssues(BaseGithubIssues):
    def get_repository_owner(self):
        return "metabase"

    def get_repository_name(self):
        return "metabase"

    def get_bug_labels(self):
        return '["Type:Bug"]'

    def get_excluded_labels(self):
        return [".Needs Triage"]