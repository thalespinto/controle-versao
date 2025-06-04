from core.baseGithubApi import BaseGithubIssues
class FreeCadIssues(BaseGithubIssues):
    def get_repository_owner(self):
        return "FreeCAD"
    
    def get_repository_name(self):
        return "FreeCAD"
    
    def get_bug_labels(self):
        return []
    
    def get_excluded_labels(self):
        return ["Status: Duplicate","Status: Needs confirmation","Status: Needs triage"]
    
    def get_special_filters(self):
        bug_labels = ["Type: Bug", "Type: Crash", "Type: Regression"]

        def has_bug_label(issue):
            labels = [label["name"].lower() for label in issue["labels"]["nodes"]]
            return any(bug_label.lower() in labels for bug_label in bug_labels)

        return [has_bug_label]