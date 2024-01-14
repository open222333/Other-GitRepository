from src import DIR_PATH, EMAIL, NAME, USERNAME, PASSWORD, GITDOMAIN
from src import LOG_LEVEL
from src.common_tool.src.logger import Log
from src.git_tool import Git, GitConfig
from src.common_tool.src.progress_bar import ProgressBar
import os


logger = Log('Pull_All')
logger.set_level(LOG_LEVEL)
logger.set_msg_handler()

if __name__ == '__main__':

    files = os.listdir(DIR_PATH)
    
    if NAME and EMAIL:
        gitconfig = GitConfig(dir_path=DIR_PATH)
        gitconfig.set_config(NAME, EMAIL)
        
    p = ProgressBar()
    
    for file in files:
        try:
            git_path = f'{DIR_PATH}/{file}'
            if os.path.isdir(git_path):
                git_obj = Git(
                    user=USERNAME,
                    token=PASSWORD,
                    git_domain=GITDOMAIN,
                    dir_path=git_path
                )
                result = ''
                if git_obj.is_git_repo():
                    if NAME and EMAIL:
                        git_obj.set_config(NAME, EMAIL)
                    result = len(git_obj.do_pull())
                else:
                    result = f'{file} 非git專案資料夾'
            p(total=len(files), in_loop=True, detail=f'git 資料夾路徑 {git_path} {result}')
        except Exception as err:
            logger.error(err, exc_info=True)
