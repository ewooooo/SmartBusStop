import RPi.GPIO as GPIO
import time 


encoderCount = 0

class inputDevice:
    DT = 22         #// 로터리 엔코더의 DT를 연결한 핀
    CLK = 27        #// 로터리 엔코더의 CLK를 연결한 핀 A
   
    oldCLK = 0  #// CLK 핀의 값을 저장하는 변수
    oldDT = 0  # // DT 핀의 값을 저장하는 변수
  
    outTime = 0.1

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)    
        GPIO.setup(self.DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)     
        self.direct = 0
        self.count = 0

    def rotaryCheck(self):
        
        newCLK = GPIO.input(self.CLK)
        newDT = GPIO.input(self.DT)
        out = 0
        if newCLK != self.oldCLK or newDT != self.oldDT:
            if self.oldCLK == 0 and newCLK == 1:
                self.direct = self.oldDT * 2 - 1
                self.count = time.time_ns()
            
            if self.count != 0 :
                delaytime = (time.time_ns() - self.count)/1000000000
                if delaytime >= self.outTime :
                    out = self.direct
                    self.direct = 0
                    self.count = 0
                    

        self.oldCLK = newCLK
        self.oldDT = newDT
        if out !=0:
            self.rotaryAction(out)

    def rotaryAction(self,value):
        global encoderCount
        encoderCount = encoderCount + value
        print(encoderCount)
        
    def checkButton(self):
        try:
            while True:
                self.rotaryCheck()

        finally:
            GPIO.cleanup()

if __name__ == "__main__":
    a = inputDevice()
    a.checkButton()


