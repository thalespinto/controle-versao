from core.baseGithubApi import BaseGithubIssues


class QbittorrentIssues(BaseGithubIssues):
    def get_repository_owner(self):
        return "qbittorrent"

    def get_repository_name(self):
        return "qbittorent"

    def get_bug_labels(self):
        return '["Confirmed bug"]'

    def get_excluded_labels(self):
        return []