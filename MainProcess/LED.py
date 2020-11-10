from baseModule.LEDModule import baseLED

class LED(baseLED):
    def __init__(self):
        baseLED.__init__(self,"./baseModule/")
        self.nowplay = None
    def SET_LED(self, number):
        if self.nowplay != number:
            super().SET_LED(number)
            self.nowplay = number
            print("LED pirnt : "+number)
    def OFF_LED(self):
        if not self.nowplay:
            super().OFF_LED()
            self.nowplay = None
            #print("LED off")
