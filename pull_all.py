import logging
import git
import os
from configparser import ConfigParser
from logging.handlers import RotatingFileHandler


config = ConfigParser()
config.read('git_config.ini')
USERNAME = config.get('GIT', 'USERNAME')
PASSWORD = config.get('GIT', 'PASSWORD')
DIR_PATH = config.get('GIT', 'DIR_PATH')
GITDOMAIN = config.get('GIT', 'GITDOMAIN', fallback='github.com')
# 設定紀錄log等級 DEBUG,INFO,WARNING,ERROR,CRITICAL 預設WARNING
LOG_LEVEL = config.get('GIT', 'LOG_LEVEL', fallback='WARNING')


logger = logging.getLogger(__name__)

if LOG_LEVEL == 'DEBUG':
    logger.setLevel(logging.DEBUG)
elif LOG_LEVEL == 'INFO':
    logger.setLevel(logging.INFO)
elif LOG_LEVEL == 'WARNING':
    logger.setLevel(logging.WARNING)
elif LOG_LEVEL == 'ERROR':
    logger.setLevel(logging.ERROR)
elif LOG_LEVEL == 'CRITICAL':
    logger.setLevel(logging.CRITICAL)

log_handler = RotatingFileHandler(f'{__name__}.log', maxBytes=5000, backupCount=1)
msg_handler = logging.StreamHandler()
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)
msg_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)
logger.addHandler(msg_handler)


class Git:
    '''使用git做一個類別'''

    def __init__(self,dir_path:str, user: str, token: str, git_domain: str, credentials_file_path: str = '.sample-credentials') -> None:
        """建立 驗證檔案

        Args:
            dir_path: 專案資料夾位置
            user (str): 用戶名
            token (str): 驗證token
            git_domain (str): git主機
            credentials_file_path (str): 驗證檔案名稱位置. Defaults to '.sample-credentials'.
        """
        ''''''
        self.user = user
        self.token = token
        self.dir_path = dir_path
        self.git_domain = git_domain
        os.system(f"git config --global credential.helper 'store --file {credentials_file_path}'")

    def is_git_repo(self) -> bool:
        '''檢查是否為git專案'''
        all_items = os.listdir(self.dir_path)
        return '.git' in all_items

    def set_repo(self):
        self.repo = git.Repo(self.dir_path)

    def get_remote(self):
        return self.repo.remotes

    def do_pull(self):
        git_action = self.repo.remote()
        result = git_action.pull()
        return [i.__str__() for i in result]


if __name__ == '__main__':
    files = os.listdir(DIR_PATH)

    for file in files:
        git_path = f'{DIR_PATH}/{file}'
        if os.path.isdir(git_path):
            git_obj = Git(
                dir_path=git_path,
                user=USERNAME,
                token=PASSWORD,
                git_domain=GITDOMAIN
            )
            if git_obj.is_git_repo():
                git_obj.set_repo(git_path)
                result = git_obj.do_pull()
                logger.info(f'git pull {file} 結果:{result}')
            else:
                logger.info(f'{file} 非git專案資料夾')
