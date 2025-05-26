from core.baseGithubApi import BaseGithubIssues

class MediamtxIssues(BaseGithubIssues):
    def get_repository_owner(self):
        return "bluenviron"
    
    def get_repository_name(self):
        return "mediamtx"
    
    def get_bug_labels(self):
        return '["bug"]'
    
    def get_excluded_labels(self):
        return ["status: needs triage", "duplicate", "invalid"]
    
    def get_special_filters(self):
        return [
            lambda issue: any(
                keyword in issue["title"].lower() for keyword in ["error", "fail", "panic", "crash", "unexpected"]
            )
        ]