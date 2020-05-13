
        

        
class Bus:
    def __init__(self, busNumber, carNumber, state):
        self.busNumber = busNumber
        self.carNumber = carNumber
        self.state = state

class BusList:
    def __init__(self):
        self.busList = []

    def update(self):
        next()  # 기존꺼는 그대로 남기고 중복 제거해야한다..

class UserBusList(BusList): #main button controler
    
    def update(self):
        next()

    def add(self, bus):
        self.busList.append(bus)

    def delete(self, bus):
        self.busList.remove(bus)

    def state(self):
        if not self.busList:
            return True
        else:
            return False

    def searchBus(self, imgCarNumber):
       for b in self.busList:
           if b.carNumber == imgCarNumber:
               return b
        return None