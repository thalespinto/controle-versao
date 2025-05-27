from core.baseGithubApi import BaseGithubIssues
class MuiIssues(BaseGithubIssues):
    def get_repository_owner(self):
        return "mui"
    
    def get_repository_name(self):
        return "material-ui"
    
    def get_bug_labels(self):
        return '["bug 🐛"]'
    
    def get_excluded_labels(self):
        return ["duplicate"]
    
    def get_duplicates(self):
        """Método específico para obter apenas duplicates"""
        issues = self._fetch_raw_issues()
        return [i for i in issues if any(
            label["name"] == "duplicate" for label in i["labels"]["nodes"]
        )]