import time


class Bus:
    def __init__(self, busNumber, carNumber, state):
        self.busNumber = busNumber
        self.carNumber = carNumber
        self.state = state

    def modifyBus(self, carNumber, state):
        self.carNumber = carNumber
        self.state = state


class BusList:
    def __init__(self):
        self.busDic = {}  # busNumber : Bus
        self.userBusList = {}
        self.enterBus = []

        #test  bus 객체 생성은 한번만
        bus1 = Bus('10', '10가4511', '진입')
        bus2 = Bus('20', '50나2323', '3전')
        self.busDic[bus1.busNumber] = bus1
        self.busDic[bus2.busNumber] = bus2
        self.enterBus[bus1.busNumber] = bus1
        #test

    def update(self):  # busDic update
        # 기존꺼는 그대로 남기고 중복 제거해야한다..
        print("busUpdate")
        b = ['10', '20']
        self.enterBus.clear()
        for a in b:
            bus = self.busDic.get(a)
            bus.modifyBus('변경', '진입')
            if bus.state == '진입':
                self.enterBus[bus.busNumber] = bus
        time.sleep(3)

    def add(self, busNumber):  # userbus add
        bus = self.busDic.get(busNumber)
        if not bus:
            self.userBusList[busNumber] = bus
            return True
        else:
            return False

    def delete(self, busNumber):  # userbus del
        if busNumber in self.userBusList:
            del self.userBusList[busNumber]
            return True
        else:
            return False

    def userState(self):  # userstate
        if not self.userBusList:
            return False # 비어있으면
        else:
            return True

    def enterUserBus(self):
        # carNumber in userBusList 요소가 있는지 확인 T/F
        userbusEnter = []
        for key in self.userBusList.keys():
            if key in self.enterBus:
                userbusEnter.append(key)
        return userbusEnter
