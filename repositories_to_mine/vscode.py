from core.baseGithubApi import BaseGithubIssues
class VSCodeIssues(BaseGithubIssues):
    def get_repository_owner(self):
        return "microsoft"
    
    def get_repository_name(self):
        return "vscode"
    
    def get_bug_labels(self):
        return '["bug"]'
    
    def get_excluded_labels(self):
        return ["*duplicate"]