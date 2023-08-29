import gettext

import settings

trans = gettext.translation('messages', localedir=settings.BASE_DIR / './locales', languages=[settings.LANG])
trans.install()

get_text = trans.gettext
