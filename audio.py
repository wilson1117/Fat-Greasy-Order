from gtts import gTTS      # Google TTS
from pygame import mixer   # 自動播放
import tempfile            # 暫時檔
import time                # 時間
import speech_recognition as sr

# TTS
def TTS(sentence,lang,loops=1):
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts=gTTS(text=sentence, lang=lang)
        tts.save('{}.mp3'.format(fp.name))
        mixer.init()
        mixer.music.load('{}.mp3'.format(fp.name))
        mixer.music.play()

# STT
def STT(e):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        print("請點餐～")
        audio = r.listen(source)

    try:
        print("你說的是：")
        print(r.recognize_google(audio, language="zh-TW"))
    except sr.UnknownValueError:
        print("抱歉，請再說一次")
    except sr.RequestError as e:
        print("請求錯誤")

