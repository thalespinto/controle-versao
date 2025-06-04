
from core.baseGithubApi import BaseGithubIssues
class VideDevHlsIssues(BaseGithubIssues):
    def get_repository_owner(self):
        return "video-dev"
    
    def get_repository_name(self):
        return "hls.js"
    
    def get_bug_labels(self):
        return []
    
    def get_excluded_labels(self):
        return ["Needs Triage","Needs review"]
    
    def get_special_filters(self):
        bug_labels = ["Regression","Bug"]

        def has_bug_label(issue):
            labels = [label["name"].lower() for label in issue["labels"]["nodes"]]
            return any(bug_label.lower() in labels for bug_label in bug_labels)

        return [has_bug_label]