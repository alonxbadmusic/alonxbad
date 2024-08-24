from Aloxbad.core.bot import Aviax
from Aloxbad.core.dir import dirr
from Aloxbad.core.git import git
from Aloxbad.core.userbot import Userbot
from Aloxbad.misc import dbb, heroku

from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = Aviax()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
