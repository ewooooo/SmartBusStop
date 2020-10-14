
import time
from baseModule.ButtonModule import BaseButton


class MyButton(BaseButton):
    def __init__(self,obj):
        BaseButton.__init__(self)
        self.main = obj

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
       
    def rotaryAction(self,value):
        if value == 1:
            self.main.control.nextBus()
        elif value == -1:
            self.main.control.beforeBus()




if __name__ == "__main__":
    print("start")
    b= MyButton()
    b.checkButton()