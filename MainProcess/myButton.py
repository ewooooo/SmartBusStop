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
        # while True:
        #     # self.oneClick()
        #     # time.sleep(2)
        #     # self.doubleClick()
        #     # time.sleep(2)
        #     # self.longClick()
        #     # time.sleep(2)
    
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
                        # if delaytime >= self.LONGCLICKTIME:
                        #     print(delaytime)
                        #     self.longClick()
                        #     if doubleClickON :
                        #         count = 0
                        #         doubleClickCount = 0
                        #         doubleClickON = False
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
        self.main.mysocket.Send("oneClick")

    def doubleClick(self):
        print("doubleClick")
        self.main.mysocket.Send("doubleClick")
    def longClick(self):
        print("longClick")
        self.main.mysocket.Send("longClick")
    def wakeUpTest(self):
        print("wakeUp")
        return True



# if __name__ == "__main__":
#     print("start")

#     b= MyButton()
#     b.checkButton()