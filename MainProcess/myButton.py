
import time
#from baseModule.ButtonModule import BaseButton


# class MyButton(BaseButton):
    # def __init__(self,obj):
    #     BaseButton.__init__()
    #     self.main = obj

######################test#############
class MyButton:
    def __init__(self,obj):
        self.main = obj
    def checkButton(self):
        while True:
            if self.EndCondition():
                return
            
            time.sleep(10)
            self.oneClick()
            time.sleep(10)
            self.longClick()
    def wakeUpTest(self):
        return True
#########################################



    def EndCondition(self):
        if not self.main.systemState:
            print("endBusUpdate")
            return True
        return False

    def oneClick(self):
        print("oneClick")
        self.main.control.SelectBus()
    def longClick(self):
        print("longClick")
        self.main.control.CancelBus()
       





if __name__ == "__main__":
    print("start")
    b= MyButton()
    b.checkButton()