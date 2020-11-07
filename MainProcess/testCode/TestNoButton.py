import time
class MyButton:
    def __init__(self,obj):
        self.main = obj

    def checkButton(self):
        while True:
            if not self.main.systemState:
                    return
            time.sleep(10)
            self.oneClick()
            time.sleep(5)
            self.oneClick()
            time.sleep(5)
            self.longClick()
            time.sleep(3)
            self.rotaryAction(1)
            time.sleep(3)
            self.oneClick()
            time.sleep(30)

    def oneClick(self):
        print("oneClick")
        self.main.control.SelectBus()
    def longClick(self):
        print("longClick")
        self.main.control.CancelBus()
    def rotaryAction(self,value):
        if value == 1:
            self.main.control.nextBus()
        elif value == -1:
            self.main.control.beforeBus()
    def wakeUpTest(self):
        return True
