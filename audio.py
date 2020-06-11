from gtts import gTTS      # Google TTS
from pygame import mixer   # 自動播放
import tempfile            # 暫時檔
import time                # 時間

# TTS
def TTS(sentence,lang,loops=1):
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts=gTTS(text=sentence, lang=lang)
        tts.save('{}.mp3'.format(fp.name))
        mixer.init()
        mixer.music.load('{}.mp3'.format(fp.name))
        mixer.music.play()

TTS('喵喵小雞雞','zh-TW')
time.sleep(5)
TTS('我是大屌','zh-TW')
time.sleep(5)

