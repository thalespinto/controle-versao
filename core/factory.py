from repositories_to_mine.bokeh import BokehIssues
from repositories_to_mine.clickhouse import ClickhouseIssues
from repositories_to_mine.docusaurus import DocusaurusIssues
from repositories_to_mine.gradle import GradleIssues
from repositories_to_mine.keras import KerasIssues
from repositories_to_mine.logstash import LogstashIssues
from repositories_to_mine.metabase import MetabaseIssues
from repositories_to_mine.mui import MuiIssues
from repositories_to_mine.nextcloud_server import NextcloudServerIssues
from repositories_to_mine.openwrt import OpenwrtIssues
from repositories_to_mine.qbittorrent import QbittorrentIssues
from repositories_to_mine.react import ReactIssues
from repositories_to_mine.rn import ReactNativeIssues
from repositories_to_mine.roslyn import RoslynIssues
from repositories_to_mine.vscode import VSCodeIssues


class GithubRepoFactory:
    @staticmethod
    def create(repo_name):
        repos = {
            "docusaurus":DocusaurusIssues ,
            "mui":MuiIssues ,
            "react":ReactIssues ,
            "rn":ReactNativeIssues ,
            "vscode":VSCodeIssues ,
            'bokeh': BokehIssues,
            'clickhouse': ClickhouseIssues,
            'gradle': GradleIssues,
            'kera': KerasIssues,
            'logstash': LogstashIssues,
            'metabase': MetabaseIssues,
            'nextcloud_server': NextcloudServerIssues,
            'openwrt': OpenwrtIssues,
            'qbittorrent': QbittorrentIssues,
            'roslyn': RoslynIssues,
        }
        
        repo_class = repos.get(repo_name.lower())
        if repo_class:
            return repo_class()
        raise ValueError(f"Repositório não suportado: {repo_name}")