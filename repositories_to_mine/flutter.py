from core.baseGithubApi import BaseGithubIssues

class FlutterIssues(BaseGithubIssues):
    def get_repository_owner(self):
        return "flutter"
    
    def get_repository_name(self):
        return "flutter"
    
    def get_bug_labels(self):
        return []  
    
    def get_excluded_labels(self):
        return ["waiting for customer response", "working as intended"]
    
    def get_special_filters(self):
        bug_labels = ["type: bug", "c: crash", "c: fatal crash", "regression", "performance"]

        def has_bug_label(issue):
            labels = [label["name"].lower() for label in issue["labels"]["nodes"]]
            return any(bug_label.lower() in labels for bug_label in bug_labels)

        return [has_bug_label]
