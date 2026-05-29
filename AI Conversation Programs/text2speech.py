import pyttsx3

engine = pyttsx3.init()

# 设置语速
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 50)  # 减慢语速

# 设置音量
volume = engine.getProperty('volume')
engine.setProperty('volume', volume + 0.25)  # 增加音量

# 设置声音类型
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 切换到另一种声音

# 从文件读取用户输入的字符串
with open("C:/Users/18660/Desktop/00dkuclass/info104/000final/omajili1.txt", "r", encoding="utf-8") as file:
    text_to_speak = file.read().strip()

# 将字符串转换为语音
engine.say(text_to_speak)
engine.runAndWait()