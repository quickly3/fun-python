import pyttsx3
# engine = pyttsx3.init()

# engine.say("军厚 牛逼")
# engine.runAndWait()

# com.apple.speech.synthesis.voice.sin-ji
# com.apple.speech.synthesis.voice.mei-jia
# com.apple.speech.synthesis.voice.ting-ting.premium

engine = pyttsx3.init()
voices = engine.getProperty('voices')


engine.setProperty(
    'voice', "com.apple.speech.synthesis.voice.mei-jia")

rate = engine.getProperty('rate')
engine.setProperty('rate', rate-300)
volume = engine.getProperty('volume')
engine.setProperty('volume', volume+1)
engine.say('''“好了，今天的会就开到这里。散会！”

夏冰满脸崇拜的看着军厚，他认真工作的样子好迷人啊，他穿西服的样子好帅啊！

一想到这是自己的老公就心里美滋滋的。

“在想什么呢？吃饭去！”军厚用极其霸道的口吻说。

“啊，好吧，走吧”

晚上回到家，夏冰故意不理军厚。

回到家的军厚跟在公司的军厚是截然不同的两个人，在公司的军厚霸道冷漠不近人情，回到家之后的军厚像一个温顺的小绵羊。

军厚发现夏冰的异样，“怎么了呢？老婆大人，谁招惹你了呢？”

夏冰愤愤的说，“今天白天在公司有人跟我说话语气不好了呢！”

军厚抿嘴一笑，“我知道了是谁招惹我老婆大人了，我这就去收拾他！”

于是拿着手机翻出自己的照片自言自语道，“以后不要再欺负我老婆大人了听见没有，不然我饶不了你！”

夏冰看到军厚这般傻气，忍不住笑出猪叫。

军厚见状，赶快讨好老婆：“好啦老婆大人，我这不是在公司刚晋升嘛，就要拿出一点领导的架子，求求老婆不要生气了嘛qaq，以后在家你随便处置我，在公司给我留点面子好不好嘛嘤嘤嘤。”

夏冰嘴巴嘟嘟，嘟嘟嘟嘟嘟，故意装作不情愿的样子说好。

军厚不再说话，从口袋默默掏出提前准备好的一个精致的礼物盒子。

夏冰看到礼物两眼放出了七彩光芒：“这是什么？”

军厚调皮的举高手说道，“你猜啊，猜到了就给你。”

夏冰连蹦带跳，撒娇似的说到：“cnm快给我快给我”

军厚趁机一把搂住了夏冰直径59厘米的粗腰，温柔的在她耳边说到，“老婆大人你最好了，知道你最体谅我了。”

说完，直接把盒子塞到夏冰的手里，“好啦，送给你。”

夏冰接过盒子，赫然发现里面躺着一只戒指，于是激动的说到：

“戒指戒指看看我，我的手指在哪里？”

军厚心领神会，单膝跪在250平米的奢华纯木地板上，缓缓说道，“夏冰，嫁给我好不好？”

夏冰听后才明白军厚的意图，流下了激动的色彩斑斓的泪水，说：“我愿意！”

军厚听闻这话说到：“我是问你嫁给我好不好，不是问你愿不愿意，你这样的回答很不严谨。”

夏冰一愣，害羞的说到：“好。这样紧了嘛？”

从此以后，军厚便和夏冰过上了性福快乐的生活。''')
# engine.setProperty('volume', volume+0.5)
# engine.say('非常之牛逼')

engine.runAndWait()

# engine = pyttsx3.init()


# def onStart(name):
#     # print ('starting', name
#     print(1)


# def onWord(name, location, length):
#     # print 'word', name, location, length
#     print(1)


# def onEnd(name, completed):
#     # print 'finishing', name, completed
#     if name == 'fox':
#         engine.say('What a lazy dog!', 'dog')
#     elif name == 'dog':
#         engine.endLoop()


# engine = pyttsx3.init()
# engine.connect('started-utterance', onStart)
# engine.connect('started-word', onWord)
# engine.connect('finished-utterance', onEnd)
# engine.say('The quick brown fox jumped over the lazy dog.', 'fox')
# engine.startLoop()
