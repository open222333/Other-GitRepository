from configparser import ConfigParser
import os


config = ConfigParser()
config.read(os.path.join('conf', 'git_config.ini'), encoding='utf-8')
USERNAME = config.get('GIT', 'USERNAME')
PASSWORD = config.get('GIT', 'PASSWORD')
DIR_PATH = config.get('GIT', 'DIR_PATH', fallback='repo')
GITDOMAIN = config.get('GIT', 'GITDOMAIN', fallback='github.com')
# 設定紀錄log等級 DEBUG,INFO,WARNING,ERROR,CRITICAL 預設WARNING
LOG_LEVEL = config.get('GIT', 'LOG_LEVEL', fallback='WARNING')
NAME = config.get('GIT', 'NAME', fallback=None)
EMAIL = config.get('GIT', 'EMAIL', fallback=None)
