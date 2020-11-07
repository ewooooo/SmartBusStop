import time
from baseModule.BusModule import BaseStationDict

class StationDict(BaseStationDict):
    def __init__(self,obj,stationId,serviceKey,urls):
        self.main = obj
        if not urls:
            BaseStationDict.__init__(self,stationId,serviceKey)
        else:
            BaseStationDict.__init__(self,stationId,serviceKey,urls)
        self.nowBusLP = ""

    def reset(self):
        self.nowBusLP = ""

    def addBusAction(self,bus):
        self.main.tts.addBusData(bus)
        self.main.control.addBusData(bus)
    
    def EndCondition(self):
        if not self.main.systemState:
            print("endBusUpdate")
            return True
        return False
    
    def updateDataCheck(self):  
        self.printBusList()
        self.main.control.checkdel()
        print("update Complate")

    def CampareCarNumber(self,CarNumber):
        for b in self.busDict.keys():
            bus = self.busDict.get(b)
            if self.nowBusLP != bus.plateNo and bus.plateNo[len(bus.plateNo) - 4:] == CarNumber:
                self.nowBusLP = bus.plateNo #방금 인식한 버스를 중복으로 음성안내하지 않기 위해서!
                return bus

        return None
   
    def checkState(self):
        result = True
        if not self.busDict :
            return result
        for bus in self.busDict.keys():
            b = self.busDict.get(bus)
            if b.location != '-1':
                result = False
        return result

if __name__ == "__main__":
    b=StationDict(1,"203000165","1234567890")
    b.loopUpdate(3)
