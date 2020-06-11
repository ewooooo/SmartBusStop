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
        self.state = 0

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

    def loopUpdate(self, t):  # busDict update LOOP
        ledState = False
        oneset = False
        startTime = time.time()
        while True:
            if time.time()-startTime > t:

                print("update bus")
                self.stationAPI()

                for bkey in self.busDict.keys():
                    bus = self.busDict.get(bkey)
                    print(bus.busNumber + " : " + bus.plateNo + "  " + bus.location)
                print("=================")

                startTime = time.time()


            playLEDlist = self.main.userBus.getEnterUserBus()
            if not playLEDlist:
                if ledState:
                    self.main.led.OFF_LED()
                    ledState = False
                continue
            else:
                ledState = True
                if len(playLEDlist) == 1:
                    if not oneset:
                        self.main.led.SET_LED(p.busNumber)
                        oneset = True
                else:
                    for p in playLEDlist:
                        self.main.led.SET_LED(p.busNumber)
                        print("LED : " + p.busNumber)
                        time.sleep(3)

            if not self.main.systemState:
                print("endBusUpdate")
                return


    def getBus(self,bus):
        return self.busDict.get(bus)

    def checkBus(self,bus):
        if bus in self.busDict:
            return True
        else :
            return False


# #
# #
# if __name__ == "__main__":
#     #b=StationDict("203000165","1234567890")
#     url = "http://openapi.gbis.go.kr/ws/rest/busarrivalservice/station?serviceKey="
#     url = url + "1234567890" + "&stationId="  # 203000165&
#     url = url + "203000165"
#     response = requests.get(url)
#     # text = response.text
#     text = '''
#     <response>
# <comMsgHeader/>
# <msgHeader>
# <queryTime>2020-06-08 22:32:58.813</queryTime>
# <resultCode>0</resultCode>
# <resultMessage>정상적으로 처리되었습니다.</resultMessage>
# </msgHeader>
# <msgBody>
# <busArrivalList>
# <flag>PASS</flag>
# <locationNo1>3</locationNo1>
# <locationNo2/>
# <lowPlate1>0</lowPlate1>
# <lowPlate2>0</lowPlate2>
# <plateNo1>경기70바2552</plateNo1>
# <plateNo2/>
# <predictTime1>10</predictTime1>
# <predictTime2/>
# <remainSeatCnt1>-1</remainSeatCnt1>
# <remainSeatCnt2>-1</remainSeatCnt2>
# <routeId>200000008</routeId>
# <staOrder>16</staOrder>
# <stationId>203000165</stationId>
# </busArrivalList>
# <busArrivalList>
# <flag>PASS</flag>
# <locationNo1>1</locationNo1>
# <locationNo2>10</locationNo2>
# <lowPlate1>0</lowPlate1>
# <lowPlate2>0</lowPlate2>
# <plateNo1>경기70바5467</plateNo1>
# <plateNo2>경기70바5649</plateNo2>
# <predictTime1>1</predictTime1>
# <predictTime2>21</predictTime2>
# <remainSeatCnt1>13</remainSeatCnt1>
# <remainSeatCnt2>29</remainSeatCnt2>
# <routeId>200000112</routeId>
# <staOrder>56</staOrder>
# <stationId>203000165</stationId>
# </busArrivalList>
# <busArrivalList>
# <flag>PASS</flag>
# <locationNo1>3</locationNo1>
# <locationNo2>7</locationNo2>
# <lowPlate1>0</lowPlate1>
# <lowPlate2>0</lowPlate2>
# <plateNo1>경기70바5477</plateNo1>
# <plateNo2>경기70바3695</plateNo2>
# <predictTime1>5</predictTime1>
# <predictTime2>15</predictTime2>
# <remainSeatCnt1>21</remainSeatCnt1>
# <remainSeatCnt2>31</remainSeatCnt2>
# <routeId>200000119</routeId>
# <staOrder>51</staOrder>
# <stationId>203000165</stationId>
# </busArrivalList>
# <busArrivalList>
# <flag>PASS</flag>
# <locationNo1>2</locationNo1>
# <locationNo2>23</locationNo2>
# <lowPlate1>0</lowPlate1>
# <lowPlate2>1</lowPlate2>
# <plateNo1>경기70바1825</plateNo1>
# <plateNo2>경기70바1474</plateNo2>
# <predictTime1>8</predictTime1>
# <predictTime2>31</predictTime2>
# <remainSeatCnt1>-1</remainSeatCnt1>
# <remainSeatCnt2>-1</remainSeatCnt2>
# <routeId>200000146</routeId>
# <staOrder>56</staOrder>
# <stationId>203000165</stationId>
# </busArrivalList>
# <busArrivalList>
# <flag>PASS</flag>
# <locationNo1>1</locationNo1>
# <locationNo2>12</locationNo2>
# <lowPlate1>0</lowPlate1>
# <lowPlate2>0</lowPlate2>
# <plateNo1>경기70바5703</plateNo1>
# <plateNo2>경기70바5515</plateNo2>
# <predictTime1>14</predictTime1>
# <predictTime2>39</predictTime2>
# <remainSeatCnt1>3</remainSeatCnt1>
# <remainSeatCnt2>0</remainSeatCnt2>
# <routeId>200000110</routeId>
# <staOrder>52</staOrder>
# <stationId>203000165</stationId>
# </busArrivalList>
# <busArrivalList>
# <flag>PASS</flag>
# <locationNo1>3</locationNo1>
# <locationNo2>31</locationNo2>
# <lowPlate1>0</lowPlate1>
# <lowPlate2>0</lowPlate2>
# <plateNo1>경기70바5670</plateNo1>
# <plateNo2>경기70바5567</plateNo2>
# <predictTime1>7</predictTime1>
# <predictTime2>45</predictTime2>
# <remainSeatCnt1>-1</remainSeatCnt1>
# <remainSeatCnt2>-1</remainSeatCnt2>
# <routeId>200000266</routeId>
# <staOrder>54</staOrder>
# <stationId>203000165</stationId>
# </busArrivalList>
# <busArrivalList>
# <flag>PASS</flag>
# <locationNo1>2</locationNo1>
# <locationNo2>15</locationNo2>
# <lowPlate1>0</lowPlate1>
# <lowPlate2>0</lowPlate2>
# <plateNo1>경기70바5610</plateNo1>
# <plateNo2>경기70바5540</plateNo2>
# <predictTime1>20</predictTime1>
# <predictTime2>34</predictTime2>
# <remainSeatCnt1>11</remainSeatCnt1>
# <remainSeatCnt2>26</remainSeatCnt2>
# <routeId>200000205</routeId>
# <staOrder>53</staOrder>
# <stationId>203000165</stationId>
# </busArrivalList>
# <busArrivalList>
# <flag>PASS</flag>
# <locationNo1>2</locationNo1>
# <locationNo2>68</locationNo2>
# <lowPlate1>0</lowPlate1>
# <lowPlate2>0</lowPlate2>
# <plateNo1>경기77바3443</plateNo1>
# <plateNo2>경기77바2040</plateNo2>
# <predictTime1>43</predictTime1>
# <predictTime2>121</predictTime2>
# <remainSeatCnt1>40</remainSeatCnt1>
# <remainSeatCnt2>39</remainSeatCnt2>
# <routeId>234000013</routeId>
# <staOrder>84</staOrder>
# <stationId>203000165</stationId>
# </busArrivalList>
# <busArrivalList>
# <flag>PASS</flag>
# <locationNo1>3</locationNo1>
# <locationNo2>70</locationNo2>
# <lowPlate1>0</lowPlate1>
# <lowPlate2>0</lowPlate2>
# <plateNo1>경기77바2172</plateNo1>
# <plateNo2>경기77바2148</plateNo2>
# <predictTime1>55</predictTime1>
# <predictTime2>109</predictTime2>
# <remainSeatCnt1>44</remainSeatCnt1>
# <remainSeatCnt2>43</remainSeatCnt2>
# <routeId>234000015</routeId>
# <staOrder>106</staOrder>
# <stationId>203000165</stationId>
# </busArrivalList>
# <busArrivalList>
# <flag>PASS</flag>
# <locationNo1>1</locationNo1>
# <locationNo2>21</locationNo2>
# <lowPlate1>0</lowPlate1>
# <lowPlate2>0</lowPlate2>
# <plateNo1>경기77바1614</plateNo1>
# <plateNo2>경기77바1902</plateNo2>
# <predictTime1>7</predictTime1>
# <predictTime2>25</predictTime2>
# <remainSeatCnt1>-1</remainSeatCnt1>
# <remainSeatCnt2>-1</remainSeatCnt2>
# <routeId>234000021</routeId>
# <staOrder>30</staOrder>
# <stationId>203000165</stationId>
# </busArrivalList>
# <busArrivalList>
# <flag>PASS</flag>
# <locationNo1>2</locationNo1>
# <locationNo2>39</locationNo2>
# <lowPlate1>0</lowPlate1>
# <lowPlate2>0</lowPlate2>
# <plateNo1>경기77바1757</plateNo1>
# <plateNo2>경기77바1596</plateNo2>
# <predictTime1>19</predictTime1>
# <predictTime2>52</predictTime2>
# <remainSeatCnt1>-1</remainSeatCnt1>
# <remainSeatCnt2>-1</remainSeatCnt2>
# <routeId>234000024</routeId>
# <staOrder>134</staOrder>
# <stationId>203000165</stationId>
# </busArrivalList>
# <busArrivalList>
# <flag>PASS</flag>
# <locationNo1>1</locationNo1>
# <locationNo2>75</locationNo2>
# <lowPlate1>1</lowPlate1>
# <lowPlate2>1</lowPlate2>
# <plateNo1>경기77바2617</plateNo1>
# <plateNo2>경기77바2524</plateNo2>
# <predictTime1>22</predictTime1>
# <predictTime2>74</predictTime2>
# <remainSeatCnt1>-1</remainSeatCnt1>
# <remainSeatCnt2>-1</remainSeatCnt2>
# <routeId>234000316</routeId>
# <staOrder>94</staOrder>
# <stationId>203000165</stationId>
# </busArrivalList>
# </msgBody>
# </response>'''
#     root = ET.fromstring(text)
