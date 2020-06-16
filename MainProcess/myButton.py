from Main import LoopSystem
import RPi.GPIO as GPIO
import time
class MyButton:
    LONGCLICKTIME = 1
    DOUBLECLICKTIME = 0.7
    ONECLICKTIME = 0.02

    def __init__(self,obj):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)    # set GPIO25 as input (button)  
        GPIO.setup(17, GPIO.OUT)   # set GPIO24 as an output (LED)  

        self.main = obj
        print("makebutton")
        self.count = 0

    def checkButton(self):
        try:
            self.count = 0
            doubleClickCount = 0
            doubleClickON = False
            longlock = False
            while True:
                if GPIO.input(22):
                    GPIO.output(17, 1)
                    if self.count == 0:
                        self.count = time.time_ns()
                        if(doubleClickCount != 0):      #다시눌린 시간을 측정한다.
                            delaytime = (time.time_ns() - doubleClickCount)/1000000000
                            if delaytime <= self.DOUBLECLICKTIME:
                                doubleClickON = True
                    else :
                        if not longlock :
                            delaytime = (time.time_ns() - self.count)/1000000000
                            if delaytime >= self.LONGCLICKTIME:
                                # print(delaytime)
                                self.longClick()
                                doubleClickCount = 0
                                doubleClickON = False
                                longlock = True
                                self.count = 0
                            

                else:
                    GPIO.output(17,0)
                    if longlock :
                        self.count = 0
                        longlock = False
                    if(self.count != 0):
                        delaytime = (time.time_ns() - self.count)/1000000000
                        if delaytime > self.ONECLICKTIME:
                            # print("one" + str(delaytime))
                            if doubleClickON :

                                self.doubleClick()
                                self.count = 0
                                doubleClickON = False
                                doubleClickCount = 0
                                longlock = False
                            else:
                                doubleClickCount = time.time_ns()
                        self.count = 0
                    else :
                        if doubleClickCount != 0:
                            delaytime = (time.time_ns() - doubleClickCount)/1000000000
                            if delaytime > self.DOUBLECLICKTIME:
                                # print("dou" + str(delaytime))
                                self.oneClick()
                                self.count = 0
                                doubleClickCount = 0
                                doubleClickON = False
                                longlock = False

                if not self.main.systemState:
                    print("endbutton")
                    return
        finally :
            pass #GPIO.cleanup()

    def oneClick(self):
        print("oneClick")
        nowbus = self.main.tts.getNowPlayBus()
        if not nowbus:
            self.main.tts.playButtonInfo(self.main.tts.status.error_inf_not)
        else:

            if self.main.userBus.add(nowbus):
                self.main.tts.playButtonInfo(self.main.tts.status.button_2_Push_Succes,nowbus)
            else:
                self.main.tts.playButtonInfo(self.main.tts.status.button_2_Push_Fail,nowbus)

    def doubleClick(self):
        print("double")
        self.main.tts.busStateInfo()
        # # 현재 등록된 버스 번호들

    def longClick(self):
        print("longClick")
        bus = self.main.userBus.recentBus
        if self.main.userBus.delete(bus):
            self.main.tts.playButtonInfo(self.main.tts.status.button_3_Cancel,bus)
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
                        return True
            else:
                GPIO.output(17, 0)


if __name__ == "__main__":
    print("start")

    b= MyButton(None)
    b.checkButton()