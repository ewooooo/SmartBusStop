import xml.etree.ElementTree as ET
import requests
import time

class Bus:
    def __init__(self, busNumber, routeId, plateNo, location):
        self.busNumber = busNumber  # 버스 번호
        self.routeId = routeId  # 버스 ID
        self.plateNo = plateNo   # 버스 번호판 int
        self.location= location   # 도착정보 (가장빠른 버스 몇정거장 전인지)
        self.state = 0

    def modifyBus(self, routeId, plateNo, location):
        if self.routeId == routeId:
            self.plateNo = plateNo   # 버스 번호판
            self.location = location    # 도착정보 (가장빠른 버스 몇정거장 전인지)

    def __str__(self):
        return self.busNumber + "번, location: " + self.location +" state : " + str(self.state)


class BaseStationDict:
    def __init__(self,stationId,serviceKey,url='http://openapi.gbis.go.kr/ws/rest'):
        self.serviceKey = serviceKey
        self.stationId =stationId
        self.urls = url
        self.busDict = {}  # busNumber : Bus
        self.stationAPI()

    def stationAPI(self): #1234567890

        url = self.urls + "/busarrivalservice/station?serviceKey="
        url = url + self.serviceKey + "&stationId="
        url = url + self.stationId
        response = requests.get(url)
        text = response.text
        root = ET.fromstring(text)

        bufferBusCode = []
        for child in root:
            if child.tag != 'msgBody':
                continue
            for kid in child:
                routeId, plateNo, location = "", "", ""
                for ac in kid:
                    if ac.tag == "routeId":  # 노선번호
                        routeId = ac.text

                    if ac.tag == "plateNo1":  # 먼저 도착하는 버스번호
                        plateNo = ac.text

                    if ac.tag == "locationNo1":  # 먼저 도착하는 버스의 남은 정거장
                        location = ac.text

                    # route1 : plate1, location1, plate2, location2
                if not routeId in self.busDict:
                    busNumber = self.routeAPI(routeId)
                    bus = Bus(busNumber, routeId, plateNo, location)
                    self.busDict[routeId] = bus
                    self.addBusAction(bus)

                else:
                    bus = self.busDict.get(routeId)
                    bus.modifyBus(routeId, plateNo, location)
                bufferBusCode.append(routeId)
        for busCode in self.busDict.keys():
            if not busCode in bufferBusCode:
                bus = self.busDict.get(busCode)
                bus.modifyBus(busCode, '-1', '-1')

    def routeAPI(self,routeId):
        url = self.urls + "/busrouteservice/info?serviceKey="
        url = url + self.serviceKey + "&routeId="
        url = url + routeId
        response = requests.get(url)
        text = response.text
        root = ET.fromstring(text)
        for top in root:
            if top.tag != 'msgBody':
                continue
            for mid in top:
                for bot in mid:
                    if bot.tag == "routeName":  # 노선번호
                        return bot.text

    def addBusAction(self,bus): #기존에 없던 버스가 추가되었을때 실행할 액션
        print("add bus : "+bus.busNumber)

    def updateDataCheck(self):  #한 업데이트 사이클이 끝난후 업데이트된 데이터를 가지고 할 액션
        self.printBusList()
        print("update Complate")

    def EndCondition(self):     #loopUpdate를 종료할 조건
        return False

    def printBusList(self):
        for bkey in self.busDict.keys():
            bus = self.busDict.get(bkey)
            print(bus.busNumber + " : " + bus.plateNo + "  " + bus.location)

    def loopUpdate(self, t):  # busDict update LOOP
        ledState = False
        startTime = time.time()
        while True:
            if self.EndCondition():
                return

            if time.time()-startTime > t:
                print("update bus")
                self.stationAPI()
                self.updateDataCheck()

                startTime = time.time()

    def getBus(self,bus):   # busDict return
        return self.busDict.get(bus)

    def checkBus(self,bus): # 해당 버스 routeID를 받아 버스가 있는지 확인
        if bus in self.busDict:
            return True
        else :
            return False


if __name__ == "__main__":
    b = BaseStationDict("203000165","1234567890",'http://127.0.0.1')
    b.loopUpdate(3)
