from repositories_to_mine.mediamtx import MediamtxIssues
from repositories_to_mine.docusaurus import DocusaurusIssues
from repositories_to_mine.mui import MuiIssues
from repositories_to_mine.react import ReactIssues
from repositories_to_mine.rn import ReactNativeIssues 
from repositories_to_mine.vscode import VSCodeIssues

class GithubRepoFactory:
    @staticmethod
    def create(repo_name):
        repos = {
            "mediamtx":MediamtxIssues ,
            "docusaurus":DocusaurusIssues ,
            "mui":MuiIssues ,
            "react":ReactIssues ,
            "rn":ReactNativeIssues ,
            "vscode":VSCodeIssues ,
        }
        
        repo_class = repos.get(repo_name.lower())
        if repo_class:
            return repo_class()
        raise ValueError(f"Repositório não suportado: {repo_name}")