
import time
class TTS() :
    def __init__(self,obj):
        self.main = obj
        self.nowPlay = None
        self.playlist = []

    def playTTS(self):

        while True:
            print(self.main.listTest)
            print("playTTS")
            time.sleep(3)
            #if not self.playlist:

