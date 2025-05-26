from core.baseGithubApi import BaseGithubIssues

class ReactNativeIssues(BaseGithubIssues):
    def get_repository_owner(self):
        return "facebook"
    
    def get_repository_name(self):
        return "react-native"
    
    def get_bug_labels(self):
        return '["Bug"]'
    
    def get_excluded_labels(self):
        return [
            "Resolution: Locked",
            "Resolution: Answered",
            "Resolution: Duplicate",
            "Resolution: Cannot Reproduce",
            "Resolution: For Stack Overflow",
            "Resolution: Issue in another tool or repo",
            "Needs: Triage :mag:"
        ]