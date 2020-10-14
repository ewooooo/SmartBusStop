from threading import Thread, Semaphore

from my_socket import mySocket
from busPlayList import busPlayList
from Bus import StationDict

from myButton import MyButton
from LED import LED
import keyData

class UserBus:

    def __init__(self):
        self.userBusList = []
        self.recentBus = None
        self.userSemaphore = Semaphore(1)
    def reset(self):
        self.userBusList = []
        self.recentBus = None

    def add(self, bus):  # userbus add
        if not bus.routeId in self.userBusList :
            self.recentBus = bus
            self.userSemaphore.acquire()
            self.userBusList.append(bus)
            self.userSemaphore.release()
            return True
        else:
            return False

    def cancel(self):  # userbus del
        self.userSemaphore.acquire()
        if self.recentBus != None:
            returnData = self.recentBus
            self.userBusList.remove(self.recentBus)
            self.recentBus = None
            self.userSemaphore.release()
            return returnData
        else:
            self.userSemaphore.release()
            return None

    def endDelete(self, bus):
        self.userSemaphore.acquire()
        if self.userBusList.remove(bus):
            self.userSemaphore.release()
            return True
        else:
            self.userSemaphore.release()
            return False

    def nextBus(self):
        self.userSemaphore.acquire()
        nextbus = None
        if bool(self.userBusList):
            if int(self.userBusList[0].location) <= 1:
                nextbus = self.userBusList[0]
            self.userBusList.append(self.userBusList[0])
            del self.userBusList[0]
        self.userSemaphore.release()
        return nextbus
            
class Control:
    def __init__(self,main):
        self.TTS = main.tts
        self.userBus = main.userBus
        self.main = main
        self.__playListSemaphore = Semaphore(1)       #멀티쓰레드로 인해 playlist 동시접근 에러를 방지하기 위한 세마포어
        self.playlist = []    #세마포어로 충돌 해결
        self.LEDPlayList = []
    
    def reset(self):
        self.LEDPlayList = []

    def addBusData(self, bus): 
        self.__playListSemaphore.acquire()
        self.playlist.append(bus)
        self.__playListSemaphore.release()

    def nextBus(self):
        self.__playListSemaphore.acquire()
        if bool(self.playlist):
            self.playlist.append(self.playlist[0])
            del self.playlist[0]
            self.TTS.playVoice(self.playlist[0].busNumber,soundChannel=1)
            print(self.playlist[0].busNumber)
        else:
            self.TTS.playVoice(self.TTS.status.error_station_info,soundChannel=1)
        self.__playListSemaphore.release()

    def beforeBus(self):
        self.__playListSemaphore.acquire()
        if bool(self.playlist):
            self.playlist.insert(0,self.playlist[-1])
            del self.playlist[-1]
            self.TTS.playVoice(self.playlist[0].busNumber,soundChannel=1)
            print(self.playlist[0].busNumber)
        else:
            self.TTS.playVoice(self.TTS.status.error_station_info,soundChannel=1)
        self.__playListSemaphore.release()

    def SelectBus(self):
        self.__playListSemaphore.acquire()
        if bool(self.playlist):
            if self.userBus.add(self.playlist[0]):
                self.TTS.playVoice(self.playlist[0].busNumber,self.TTS.status.button_2_Push_Succes,"현재",self.playlist[0].location,self.TTS.status.bus_before_station,soundChannel=1)
                print("버스 등록 : " +str(self.playlist[0].busNumber))
            else:
                self.TTS.playVoice(self.TTS.status.button_2_Push_Fail,"현재",self.playlist[0].location,self.TTS.status.bus_before_station,soundChannel=1)
        else :
            self.main.tts.playVoice(self.main.tts.status.error_station_info,soundChannel=1)
            print("이미 등록 : " +str(self.playlist[0].busNumber))
        self.__playListSemaphore.release()

    def CancelBus(self):
        bus = self.userBus.cancel()
        if not bus:
            self.TTS.playVoice(self.TTS.status.button_3_Cancel_Fail,soundChannel=1)
            print("삭제 실패")
        else:
            self.TTS.playVoice(bus.busNumber,self.TTS.status.button_3_Cancel,soundChannel=1)
            print("버스 삭제 : " + bus.busNumber)


    def SystemEnd(self,voice=None):
        self.main.systemState = False
        self.TTS.setPlayStop(0)
        self.TTS.setPlayStop(1)
        self.TTS.playVoice(voice,self.TTS.status.end_program)
        return

    def CamCheckBus(self,busCarNumber):
        if busCarNumber != None:
            b=self.main.bus.CampareCarNumber(busCarNumber)
            if bool(b):
                self.TTS.playVoice(self.TTS.status.bus_stop,b.busNumber,"입니다")
                print("버스 도칙" +str(b.busNumber))

    def LEDLoop(self):
        while True:
            if not self.main.systemState:
                print("EndLEDLoop")
                return
            bus = self.userBus.nextBus()
            if bus :
                if bus not in self.LEDPlayList:
                    self.LEDPlayList.append(bus)
                self.main.led.SET_LED(bus.busNumber)
                time.sleep(3)
            else :
                self.main.led.OFF_LED()
            
            if self.main.bus.checkState():
                self.SystemEnd(self.TTS.status.error_bus_not)


    def checkdel(self):
        if bool(self.LEDPlayList) :
            for b in self.LEDPlayList:
                if b.location > 1:
                    if self.userBus.endDelete(b):
                        self.LEDPlayList.remove(b)


class LoopSystem:

    def __init__(self):
        
        self.kySocket = mySocket(self,keyData.HOST,keyData.PORT)
        self.button = MyButton(self)
        self.tts = busPlayList(keyData.TTS_client_id, keyData.TTS_client_secret)
        self.userBus = UserBus()
        self.control = Control(self)
        self.bus = StationDict(self, keyData.stationNumber, keyData.serviceKey)  # 순서 중요 tts -> userBus-> control -> bus
        self.led = LED()
        
        

        self.systemState = False  # 시스템 상태(default : 대기)

    def loopStart(self):

        while True:
            # 시스템 자고 있으면 깨우기(버튼 체크)_버튼 눌리면일어남
            while not self.systemState:
                self.systemState = self.button.wakeUpTest()
            self.tts.playVoice(self.tts.status.button_1_Info)

            self.userBus.reset()
            self.control.reset()

            button_Thread = Thread(target=self.button.checkButton)  # 버튼 입력 시작
            busUpdate_Thread = Thread(target=self.bus.loopUpdate, args=(20,))  # 버스 정보 갱신 시작
            LED_Thread = Thread(target=self.control.LEDLoop)  # 음성 안내 시작
            Socket_Thread = Thread(target=self.kySocket.loopSocket)  # 연산 시작
            print("System Start")
            button_Thread.start()
            busUpdate_Thread.start()
            LED_Thread.start()
            Socket_Thread.start()

            button_Thread.join()
            busUpdate_Thread.join()
            LED_Thread.join()
            Socket_Thread.join()
            
            self.systemState = False


if __name__ == "__main__":
    loop = LoopSystem()
    loop.loopStart()
