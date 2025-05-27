from core.baseGithubApi import BaseGithubIssues

class MediamtxIssues(BaseGithubIssues):
    def get_repository_owner(self):
        return "bluenviron"
    
    def get_repository_name(self):
        return "mediamtx"
    
    def get_bug_labels(self):
        return '["bug"]'