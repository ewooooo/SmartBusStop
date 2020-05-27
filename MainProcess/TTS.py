
import time
class TTS() :
    def __init__(self,obj):
        print("makeTTS")
        self.main = obj
        self.nowPlay = None
        self.playlist = []

    def playTTS(self):
        while True:
            print("playTTS : ")
            print(self.main.listTest)
            del self.main.listTest[:]
            time.sleep(3)

            #if not self.playlist:

