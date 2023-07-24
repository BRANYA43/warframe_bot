import gettext

import config

trans = gettext.translation('bot', localedir=config.BASE_DIR / './lang', languages=[config.CURRENT_LANG])
trans.install()

get_text = trans.gettext