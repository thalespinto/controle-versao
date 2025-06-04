from core.baseGithubApi import BaseGithubIssues
class MitmproxyIssues(BaseGithubIssues):
    def get_repository_owner(self):
        return "mitmproxy"
    
    def get_repository_name(self):
        return "mitmproxy"
    
    def get_bug_labels(self):
        return '["kind/bug"]'
    
    def get_excluded_labels(self):
        return ["kind/triage",]