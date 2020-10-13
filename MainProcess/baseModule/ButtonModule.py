import RPi.GPIO as GPIO
import time
class BaseButton:
    LONGCLICKTIME = 0.6
    ONECLICKTIME = 0.3

    ButtonPin = 17

    DT = 22         #// 로터리 엔코더의 DT를 연결한 핀
    CLK = 27        #// 로터리 엔코더의 CLK를 연결한 핀 A
   
    oldCLK = 0  #// CLK 핀의 값을 저장하는 변수
    oldDT = 0  # // DT 핀의 값을 저장하는 변수
  
    outTime = 0.1


    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
        GPIO.setup(self.CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)    
        GPIO.setup(self.DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)     
        self.direct = 0
        self.rotaryCount = 0

    def checkButton(self):
        try:
            count = 0
            longlock = False

            while True:
                if not GPIO.input(self.ButtonPin):
         
                    if count == 0:
                        count = time.time_ns()
                    else :
                        if not longlock :
                            delaytime = (time.time_ns() - count)/1000000000
                            if delaytime >= self.LONGCLICKTIME:
                                self.longClick()
                                longlock = True
                                count = 0
                                time.sleep(0.5)

                else:
                    if longlock :
                        count = 0
                        longlock = False
                    else :
                        if count != 0:
                            delaytime = (time.time_ns() - count)/1000000000
                            if delaytime > self.ONECLICKTIME:
                                self.oneClick()
                                count = 0
                                longlock = False
                                time.sleep(0.5)
                self.rotaryCheck()
                if self.EndCondition():
                    return
        finally:
            pass #GPIO.cleanup()

    def rotaryCheck(self):
        
        newCLK = GPIO.input(self.CLK)
        newDT = GPIO.input(self.DT)
        out = 0
        if newCLK != self.oldCLK or newDT != self.oldDT:
            if self.oldCLK == 0 and newCLK == 1:
                self.direct = self.oldDT * 2 - 1
                self.rotaryCount = time.time_ns()
            
            if self.rotaryCount != 0 :
                delaytime = (time.time_ns() - self.rotaryCount)/1000000000
                if delaytime >= self.outTime :
                    out = self.direct
                    self.direct = 0
                    self.rotaryCount = 0
                    

        self.oldCLK = newCLK
        self.oldDT = newDT
        if out !=0:
            self.rotaryAction(out)

    def EndCondition(self):
        return False

    def oneClick(self):
        print("oneClick")

    def longClick(self):
        print("longClick")

    def rotaryAction(self,value):
        print("rotary" + str(value))

    def wakeUpTest(self):
        print("wakeUp")
        count = 0
        while True:
            if not GPIO.input(self.ButtonPin):
                if count == 0:
                    count = time.time_ns()
                else:
                    delaytime = (time.time_ns() - count) / 1000000000
                    if delaytime > self.ONECLICKTIME:
                        return True



if __name__ == "__main__":
    print("start")

    b= BaseButton()
    b.checkButton()



