from core.baseGithubApi import BaseGithubIssues

class DocusaurusIssues(BaseGithubIssues):
    def get_repository_owner(self):
        return "facebook"
    
    def get_repository_name(self):
        return "docusaurus"
    
    def get_bug_labels(self):
        return '["bug"]'
    
    def get_excluded_labels(self):
        return ["status: needs triage"]