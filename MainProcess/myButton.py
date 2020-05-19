#from Main import LoopSystem
import time

class MyButton:
    def __init__(self, obj):
        self.main = obj
        print("makebutton")
    def checkButton(self):
        i = 1
        while True:
            self.main.listTest.append(i)
            i = i + 1
            time.sleep(1)
            #print("checkButton")

    def oneClick(self):
        #현재재생중 버스 번호 받아 userbuslist에 저장
        print("oneClick")

    def doubleClick(self):

        print("doubleClick")

    def longClick(self):
        print("longClick")
    def wakeUpTest(self):
        print("wakeUp")
        return True