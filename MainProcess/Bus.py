from urllib.request import urlopen
import xml.etree.ElementTree as ET
import requests
import time

class Bus:
    def __init__(self, busNumber, routeId, plateNo, location):
        self.busNumber = busNumber  # 버스 번호
        self.routeId = routeId  # 버스 ID
        self.plateNo = plateNo   # 버스 번호판 int
        self.location= location   # 도착정보 (가장빠른 버스 몇정거장 전인지)


    def modifyBus(self, routeId, plateNo, location):
        if self.routeId == routeId:
            self.plateNo = plateNo   # 버스 번호판
            self.location = location    # 도착정보 (가장빠른 버스 몇정거장 전인지)



class StationDict:
    def __init__(self,obj,stationId,serviceKey):
        self.main = obj
        self.serviceKey = serviceKey
        self.stationId =stationId
        self.busDict = {}  # busNumber : Bus
        self.stationAPI()

    def stationAPI(self): #1234567890

        url = "http://openapi.gbis.go.kr/ws/rest/busarrivalservice/station?serviceKey="
        url = url + self.serviceKey + "&stationId=" # 203000165&
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
                    self.addBusAction()
                    # tts 추가해야함
                    self.main.tts.addBusData(bus)

                else:
                    bus = self.busDict.get(routeId)
                    bus.modifyBus(routeId, plateNo, location)
                bufferBusCode.append(routeId)
        for busCode in self.busDict.keys():
            if not busCode in bufferBusCode:
                bus = self.busDict.get(busCode)
                bus.modifyBus(busCode, '-1', '-1')


    def routeAPI(self,routeId):
        url = "http://openapi.gbis.go.kr/ws/rest/busrouteservice/info?serviceKey="
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

    def addBusAction(self):
        pass    # 버스가 추가 될때 액션
            # play 리스트 추가 등

    def loopUpdate(self,t):  # busDict update LOOP
        while True:
            print("update bus")
            self.stationAPI()
            for bkey in self.busDict.keys():
                bus = self.busDict.get(bkey)
                print(bus.busNumber + " : " + bus.plateNo + "  " + bus.location)
            print("=================")
            time.sleep(t) # 90으로 해야함


    def getBus(self,bus):
        return self.busDict.get(bus)

    def checkBus(self,bus):
        if bus in self.busDict:
            return True
        else :
            return False




if __name__ == "__main__":
    b=StationDict("203000165","1234567890")
    for bkey in b.busDict.keys():
        bus = b.busDict.get(bkey)
        print(bus.busNumber + " : "+ bus.plateNo +"  "+bus.location)
    b.loopUpdate(60)

