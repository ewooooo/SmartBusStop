
class LED:
    def __init__(self):
        self.nowplay = None
    def SET_LED(self, number):
        if self.nowplay != number:
            self.nowplay = number
            print("LED pirnt : "+number)
    def OFF_LED(self):
        if not self.nowplay:
            self.nowplay = None
            #print("LED off")
