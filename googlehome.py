
import pychromecast
from gtts_token import gtts_token
import urllib.parse
import sys

class voice_cast:
    def __init__(self):
        self.chromecasts =  pychromecast.get_chromecasts()
        self.cast = self.chromecasts[0]
    
    def get_volume(self):
        return self.cast.status[2]

    def set_volume(self,volume):
        self.cast.set_volume(volume)
        return print(f"set volume {volume}")

    def play_text(self,text, lang='ja'):
        token = gtts_token.Token()
        tk = token.calculate_token(text)

        payload = {
            'ie' : 'UTF-8',
            'q' : text,
            'tl' : lang,
            'total' : 1,
            'idx' : 0,
            'textlen' : len(text),
            'tk' : tk,
            'client' : 't',
            'ttsspeed' : 1.0
        }

        params = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote)
        url = 'https://translate.google.com/translate_tts?{}'.format(params)

        self.cast.wait()
        mc = self.cast.media_controller
        mc.play_media(url, 'audio/mp3')

if __name__=="__main__":
    voice_cast().play_text("あいうえお")