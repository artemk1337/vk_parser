import vk_api
import configparser
import logging
import os


LOG_FILENAME = 'logs/vk_parser.txt'
os.makedirs(os.path.dirname(LOG_FILENAME), exist_ok=True)
logging.basicConfig(filename=LOG_FILENAME)
logging.getLogger("vk_parser")


cfg = configparser.ConfigParser()
cfg.read('vk_parser.conf')


if 'auth_account' in cfg:
    login = cfg['auth_account']['login']
    password = cfg['auth_account']['passowrd']

    VK_SESSION = vk_api.VkApi(login, password)
    VK_SESSION.auth()
    TOOLS = vk_api.VkTools(VK_SESSION)

elif 'auth_bot' in cfg:
    app_id = int(cfg['auth_bot']['id'])
    secret_key = cfg['auth_bot']['secret_key']
    token = cfg['auth_bot']['service_key']

    VK_SESSION = vk_api.VkApi(app_id=app_id, client_secret=secret_key, token=token)
    TOOLS = vk_api.VkTools(VK_SESSION)

# common
ITER_MAX_BUFFER = cfg['parser']['iter_max_objects']

# photo
PHOTO_MAX_SHIFT_TIME = int(cfg['parser']['photo_max_shift_time'])

