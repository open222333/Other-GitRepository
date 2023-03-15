import logging
import git
import os
from configparser import ConfigParser
from logging.handlers import RotatingFileHandler


config = ConfigParser()
config.read('git_config.ini', encoding='utf-8')
USERNAME = config.get('GIT', 'USERNAME')
PASSWORD = config.get('GIT', 'PASSWORD')
DIR_PATH = config.get('GIT', 'DIR_PATH')
GITDOMAIN = config.get('GIT', 'GITDOMAIN', fallback='github.com')
# 設定紀錄log等級 DEBUG,INFO,WARNING,ERROR,CRITICAL 預設WARNING
LOG_LEVEL = config.get('GIT', 'LOG_LEVEL', fallback='WARNING')
NAME = config.get('GIT', 'NAME', fallback=None)
EMAIL = config.get('GIT', 'EMAIL', fallback=None)


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

logs_dir = 'logs'
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

log_handler = RotatingFileHandler(f'{logs_dir}/{__name__}.log', maxBytes=500, backupCount=1)
msg_handler = logging.StreamHandler()
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)
msg_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)
logger.addHandler(msg_handler)


class Git:
    '''使用git做一個類別'''

    def __init__(self, user: str, token: str, git_domain: str, credentials_file_path: str = '.sample-credentials') -> None:
        """建立 驗證檔案

        Args:
            user (str): 用戶名
            token (str): 驗證token
            git_domain (str): git主機
            credentials_file_path (str): 驗證檔案名稱位置. Defaults to '.sample-credentials'.
        """
        ''''''
        self.user = user
        self.token = token
        self.git_domain = git_domain
        command = f"git config --global credential.helper \'store --file {credentials_file_path}\'"
        logger.debug(command)
        os.system(command)

    def set_git_repo_dir(self, dir_path: str):
        """設置 git專案資料夾

        Args:
            dir_path (str): 專案資料夾位置
        """
        self.dir_path = dir_path

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
    if NAME and EMAIL:
        if '.git' in files:
            os.system(f"cd {DIR_PATH} && git config user.name {NAME}")
            os.system(f"cd {DIR_PATH} && git config user.email {EMAIL}")
    git_obj = Git(
        user=USERNAME,
        token=PASSWORD,
        git_domain=GITDOMAIN
    )
    for file in files:
        try:
            git_path = f'{DIR_PATH}/{file}'
            if os.path.isdir(git_path):
                logger.info(f'執行 {DIR_PATH}/{file}')
                git_obj.set_git_repo_dir(git_path)
                if git_obj.is_git_repo():
                    if NAME and EMAIL:
                        logger.info(f'{file} git config 設置 {NAME} {EMAIL}')
                        os.system(f"cd {git_path} && git config user.name {NAME}")
                        os.system(f"cd {git_path} && git config user.email {EMAIL}")
                    logger.info(f'{file} 執行 git pull ')
                    git_obj.set_repo()
                    result = git_obj.do_pull()
                    logger.info(f'git pull {file} 結果:{result}')
                else:
                    logger.info(f'{file} 非git專案資料夾')
        except Exception as err:
            logger.error(err, exc_info=True)
