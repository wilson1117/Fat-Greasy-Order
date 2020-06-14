from gtts import gTTS      # Google TTS
from pygame import mixer   # 自動播放
import tempfile            # 暫時檔
import time                # 時間
import speech_recognition as sr
import socketio
import time
import re

# TTS
mixer.init()
mixer.set_num_channels(1)
response_queue = []


def TTS(sentence, lang, loops=1):
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts = gTTS(text=sentence, lang=lang)
        tts.save('{}.mp3'.format(fp.name))
        mixer.music.load('{}.mp3'.format(fp.name))
        mixer.music.play()
        while mixer.music.get_busy():
            continue

# STT


def STT():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)

    try:
        return r.recognize_google(audio, language="zh-TW")
    except sr.UnknownValueError:
        print("抱歉，請再說一次")
    except sr.RequestError:
        print("請求錯誤")
    return False


digit = {'一': 1, '兩': 2, '二': 2, '三': 3, '四': 4,
         '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '零': 0}


def zh2an(matchobj):
    text = matchobj.group(0)
    ans = 0
    while(len(text)):
        buffer = text[:1]
        text = text[1:]
        if len(text):
            unit = text[:1]
            text = text[1:]
            if buffer == "零":
                continue
            elif unit == "萬":
                ans += digit[buffer] * 10000
            elif unit == "千":
                ans += digit[buffer] * 1000
            elif unit == "百":
                ans += digit[buffer] * 100
            elif unit == "十":
                ans += digit[buffer] * 10
        else:
            ans += digit[buffer]
    return str(ans)


socket = socketio.Client()

speech = False


@socket.on("bot_uttered")
def bot_uttered(data):
    global response_queue
    global speech
    print(data["text"])
    response_queue.append(data["text"])
    speech = False


socket.connect("http://localhost:5005")

print("Server ready~")
while True:
    while speech or len(response_queue):
        if len(response_queue):
            TTS(response_queue[0], "zh-TW")
            response_queue = response_queue[1:]
            while mixer.music.get_busy():
                continue
    print("recording")
    message = STT()
    if message:
        message = re.sub(
            r'([\u5341\u767E\u5343\u842C\u4E00\u5169\u4E8C\u4E09\u56DB\u4E94\u516D\u4E03\u516B\u4E5D\u96F6]+)', zh2an, message)
        print(message)
        socket.emit("user_uttered", {"message": message})
        speech = True
        time.sleep(2)
