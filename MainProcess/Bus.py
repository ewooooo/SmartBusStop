import time
from baseModule.BusModule import BaseStationDict

class StationDict(BaseStationDict):
    def __init__(self,obj,stationId,serviceKey):
        self.main = obj
        BaseStationDict.__init__(self,stationId,serviceKey)

    def addBusAction(self,bus):
        self.main.tts.addBusData(bus)
    
    def EndCondition(self):
        if not self.main.systemState:
            print("endBusUpdate")
            return True
        return False
    
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
            ################# LED Loop ########################
            playLEDlist = self.main.userBus.getEnterUserBus()
            if not playLEDlist:
                if ledState:
                    self.main.led.OFF_LED()
                    ledState = False
                continue
            else:
                ledState = True
                if len(playLEDlist) == 1:
                    self.main.led.SET_LED(playLEDlist[0].busNumber)
                else:
                    for p in playLEDlist:
                        self.main.led.SET_LED(p.busNumber)
                        print("LED : " + p.busNumber)
                        time.sleep(3)
            ###################################################

if __name__ == "__main__":
    b=StationDict(1,"203000165","1234567890")
    b.loopUpdate(3)
    # url = "http://openapi.gbis.go.kr/ws/rest/busarrivalservice/station?serviceKey="
    # url = url + "1234567890" + "&stationId="  # 203000165&
    # url = url + "203000165"
    # response = requests.get(url)
    # # text = response.text
    # root = ET.fromstring(text)
