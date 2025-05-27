from core.baseGithubApi import BaseGithubIssues

class ReactIssues(BaseGithubIssues):
    def get_repository_owner(self):
        return "facebook"
    
    def get_repository_name(self):
        return "react"
    
    def get_bug_labels(self):
        return '["Type: Bug"]'
    
    def get_excluded_labels(self):
        return ["Status: Unconfirmed", "status: needs triage"]