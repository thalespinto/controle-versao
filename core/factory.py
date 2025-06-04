from repositories_to_mine.bokeh import BokehIssues
from repositories_to_mine.clickhouse import ClickhouseIssues
from repositories_to_mine.docusaurus import DocusaurusIssues
from repositories_to_mine.gradle import GradleIssues
from repositories_to_mine.keras import KerasIssues
from repositories_to_mine.logstash import LogstashIssues
from repositories_to_mine.metabase import MetabaseIssues
from repositories_to_mine.nextcloud_server import NextcloudServerIssues
from repositories_to_mine.openwrt import OpenwrtIssues
from repositories_to_mine.qbittorrent import QbittorrentIssues
from repositories_to_mine.react import ReactIssues
from repositories_to_mine.rn import ReactNativeIssues
from repositories_to_mine.roslyn import RoslynIssues
from repositories_to_mine.vscode import VSCodeIssues
from repositories_to_mine.flutter import FlutterIssues
from repositories_to_mine.vitessio_vitess import VitessioVitessIssues
from repositories_to_mine.aws_cli import AwsCliIssues
from repositories_to_mine.freeCad import FreeCadIssues
from repositories_to_mine.mitmproxy import MitmproxyIssues
from repositories_to_mine.videodev_hls import VideDevHlsIssues

class GithubRepoFactory:
    @staticmethod
    def create(repo_name):
        repos = {
            "docusaurus":DocusaurusIssues ,
            "react":ReactIssues ,
            "rn":ReactNativeIssues ,
            "vscode":VSCodeIssues ,
            "flutter":FlutterIssues,
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
            "vitess":VitessioVitessIssues,
            "aws_cli": AwsCliIssues, 
            "free_cad":FreeCadIssues,
            "mitmproxy": MitmproxyIssues,
            "videodev_hls": VideDevHlsIssues
        }
        
        repo_class = repos.get(repo_name.lower())
        if repo_class:
            return repo_class()
        raise ValueError(f"Repositório não suportado: {repo_name}")