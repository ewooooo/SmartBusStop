from Main import LoopSystem
import RPi.GPIO as GPIO
import time

class MyButton:
    LONGCLICKTIME = 1
    DOUBLECLICKTIME = 0.5
    ONECLICKTIME = 0.05

    def __init__(self,obj):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)    # set GPIO25 as input (button)  
        GPIO.setup(17, GPIO.OUT)   # set GPIO24 as an output (LED)  

        self.main = obj
        print("makebutton")

    def checkButton(self):
        try:
            count =0
            doubleClickCount = 0
            doubleClickON = False
            longlock = False
            while True:
                if GPIO.input(22):
                    GPIO.output(17, 1)
                    if count == 0:
                        count = time.time_ns()
                        if(doubleClickCount != 0):
                            delaytime = (time.time_ns() - doubleClickCount)/1000000000
                            if delaytime <= self.DOUBLECLICKTIME:
                                doubleClickON = True
                    else :
                        if not longlock :
                            delaytime = (time.time_ns() - count)/1000000000
                            if delaytime >= self.LONGCLICKTIME:
                                print(delaytime)
                                self.longClick()
                                doubleClickCount = 0
                                doubleClickON = False
                                longlock = True
                            

                else:
                    GPIO.output(17,0)
                    if longlock :
                        count = 0
                        longlock = False
                    if(count != 0):
                        delaytime = (time.time_ns() - count)/1000000000
                        if delaytime > self.ONECLICKTIME:
                            if doubleClickON :
                                print(delaytime)
                                self.doubleClick()
                                count = 0
                                doubleClickON = False
                                doubleClickCount = 0
                            else:
                                doubleClickCount = time.time_ns()
                        count = 0
                    else :
                        if doubleClickCount != 0:
                            delaytime = (time.time_ns() - doubleClickCount)/1000000000
                            if delaytime > self.DOUBLECLICKTIME:
                                print(delaytime)
                                self.oneClick()
                                count = 0
                                doubleClickCount = 0
                                doubleClickON = False
        finally :
            GPIO.cleanup()

    def oneClick(self):
        print("oneClick")
        if self.main.userBus.add(self.main.tts.getNowPlayRout()):
            self.main.tts.playButtonInfo(self.main.tts.status.button_2_Push_Succes)
        else:
            self.main.tts.playButtonInfo(self.main.tts.status.button_2_Push_Fail)

    def doubleClick(self):
        self.main.tts.playButtonInfo(self.main.tts.status.button_3_Cancel_Fail)

    def longClick(self):
        print("longClick")
        if self.main.userBus.delete():
            self.main.tts.playButtonInfo(self.main.tts.status.button_3_Cancel)
        else:
            self.main.tts.playButtonInfo(self.main.tts.status.button_3_Cancel_Fail)

    def wakeUpTest(self):
        print("wakeUp")
        count = 0
        while True:
            if GPIO.input(22):
                GPIO.output(17, 1)
                if count == 0:
                    count = time.time_ns()
                else:
                    delaytime = (time.time_ns() - count) / 1000000000
                    if delaytime > self.ONECLICKTIME:
                        break
            else:
                GPIO.output(17, 0)


# if __name__ == "__main__":
#     print("start")

#     b= MyButton()
#     b.checkButton()