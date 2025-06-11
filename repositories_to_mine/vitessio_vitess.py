from core.baseGithubApi import BaseGithubIssues
class VitessioVitessIssues(BaseGithubIssues):
    def get_repository_owner(self):
        return "vitessio"
    
    def get_repository_name(self):
        return "vitess"
    
    def get_bug_labels(self):
        return '["Type: Bug"]'
    
    def get_excluded_labels(self):
        return ["Needs Triage","Status: Duplicate"]
    

