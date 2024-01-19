from src.common_tool.src.logger import Log
from src.common_tool.src import LOG_LEVEL
import git
import os


class Git:
    '''使用git做一個類別'''

    logger = Log('Git')

    def __init__(self, user: str, token: str, git_domain: str, dir_path: str = '.') -> None:
        """建立 驗證檔案

        Args:
            user (str): 用戶名
            token (str): 驗證token
            git_domain (str): git主機
        """
        ''''''
        self.user = user
        self.token = token
        self.dir_path = dir_path
        self.git_domain = git_domain

        if self.is_git_repo():
            self.set_repo()

        self.logger.set_level(LOG_LEVEL)
        self.logger.set_msg_handler()

    def set_git_repo_dir(self, dir_path: str):
        """設置 git專案資料夾

        Args:
            dir_path (str): 專案資料夾位置
        """
        self.dir_path = dir_path

    def is_git_repo(self) -> bool:
        '''檢查是否為git專案'''
        try:
            git.Repo(self.dir_path)
            return True
        except git.exc.InvalidGitRepositoryError:
            return False

    def set_repo(self):
        self.repo = git.Repo(self.dir_path)

    def get_remote(self):
        return self.repo.remotes

    def do_pull(self):
        try:
            git_action = self.repo.remote()
            result = git_action.pull()
            return [i.__str__() for i in result]
        except Exception as e:
            self.logger.error(f'pull 發生錯誤: {e}', exc_info=True)
            return []

    def set_config(self, name: str, email: str):
        """設置 git 資料夾 config name email

        Args:
            name (str): _description_
            email (str): _description_
        """
        if self.is_git_repo():
            repo_config = self.repo.config_reader()
            try:
                root_user_name = repo_config.get_value('user', 'name')
                root_user_email = repo_config.get_value('user', 'email')
                if root_user_name != name or root_user_name == None:
                    self.logger.info(f'{self.dir_path} git config 設置 {name}')
                    os.system(f"cd {self.dir_path} && git config user.name {name}")
                if root_user_email != email or root_user_email == None:
                    self.logger.info(f'{self.dir_path} git config 設置 {email}')
                    os.system(f"cd {self.dir_path} && git config user.email {email}")
            except Exception as err:
                self.logger.error(f'設置 git 資料夾 config name email 發生錯誤: {err}', exc_info=True)


class GitConfig(Git):

    logger = Log('GitConfig')

    def __init__(self, dir_path: str = '.') -> None:
        self.dir_path = dir_path

    def set_config(self, name: str, email: str):
        if self.is_git_repo():
            repo = git.Repo(self.dir_path)
            repo_config = repo.config_reader()
            try:
                root_user_name = repo_config.get_value('user', 'name')
                root_user_email = repo_config.get_value('user', 'email')
                if root_user_name != name or root_user_name == None:
                    self.logger.info(f'{self.dir_path} git config 設置 {name}')
                    os.system(f"cd {self.dir_path} && git config user.name {name}")
                if root_user_email != email or root_user_email == None:
                    self.logger.info(f'{self.dir_path} git config 設置 {email}')
                    os.system(f"cd {self.dir_path} && git config user.email {email}")
            except Exception as err:
                self.logger.error(err, exc_info=True)
