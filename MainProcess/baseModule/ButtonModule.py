import RPi.GPIO as GPIO
import time
class BaseButton:
    LONGCLICKTIME = 0.8
    DOUBLECLICKTIME = 0.7
    ONECLICKTIME = 0.02

    ButtonPin = 22
    ButtonLEDPin = 17

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)    # set GPIO25 as input (button)  
        GPIO.setup(self.ButtonLEDPin, GPIO.OUT)   # set GPIO24 as an output (LED)  
    
    def checkButton(self):
        try:
            count = 0
            longlock = False

            while True:
                if GPIO.input(self.ButtonPin):
                    GPIO.output(self.ButtonLEDPin, 1)
                    if count == 0:
                        count = time.time_ns()
                    else :
                        if not longlock :
                            delaytime = (time.time_ns() - count)/1000000000
                            if delaytime >= self.LONGCLICKTIME:
                                self.longClick()
                                longlock = True
                                count = 0

                else:
                    GPIO.output(self.ButtonLEDPin,0)
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
                if self.EndCondition():
                    return
        finally:
            pass #GPIO.cleanup()

    def EndCondition(self):
        return False

    def oneClick(self):
        print("oneClick")

    def longClick(self):
        print("longClick")

    def wakeUpTest(self):
        print("wakeUp")
        count = 0
        while True:
            if GPIO.input(self.ButtonPin):
                GPIO.output(self.ButtonLEDPin, 1)
                if count == 0:
                    count = time.time_ns()
                else:
                    delaytime = (time.time_ns() - count) / 1000000000
                    if delaytime > self.ONECLICKTIME:
                        return True
            else:
                GPIO.output(self.ButtonLEDPin, 0)


if __name__ == "__main__":
    print("start")

    b= MyButton()
    b.checkButton()