import argparse
import time
from threading import Thread, Semaphore

from my_socket import mySocket
from busPlayList import busPlayList
from Bus import StationDict

from myButton import MyButton
from LED import LED
# from testCode.TestNoButton import MyButton
# from testCode.TestNoLED import LED
import keyData

class UserBus:

    def __init__(self):
        self.userBusList = []
        self.userBusList_play = []
        self.recentBus = None
        self.userSemaphore = Semaphore(1)
    def reset(self):
        self.userBusList = []
        self.userBusList_play = []
        self.recentBus = None

    def add(self, bus):  # userbus add
        if not bus in self.userBusList :
            self.recentBus = bus
            self.userSemaphore.acquire()
            self.userBusList.append(bus)
            self.userBusList_play.append(bus)
            self.userSemaphore.release()
            self.checkupdate()
            return True
        else:
            self.checkupdate()
            return False

    def cancel(self):  # userbus del
        
        self.userSemaphore.acquire()
        if bool(self.userBusList) and bool(self.recentBus):
            bus = None
            if self.recentBus in self.userBusList:
                bus = self.recentBus
                self.userBusList.remove(self.recentBus)
                self.userBusList_play.remove(self.recentBus)
            if bool(self.userBusList):
                self.recentBus = self.userBusList[-1]
            else:
                self.recentBus = None
            self.userSemaphore.release()
            self.checkupdate()
            return bus
        else:
            self.recentBus = None
            self.userSemaphore.release()
            self.checkupdate()
            return None

    def endDelete(self, bus):
        print("endDelete : " + bus.busNumber)
        self.userSemaphore.acquire()
        if bus in self.userBusList:
            self.userBusList.remove(bus)
            self.userBusList_play.remove(bus)
            self.userSemaphore.release()
            self.checkupdate()
            return True
        self.userSemaphore.release()
        self.checkupdate()
        return False

    def nextBus(self):
        self.userSemaphore.acquire()
        nextbus = None
        if bool(self.userBusList_play):
            if int(self.userBusList_play[0].location) == 1:
                nextbus = self.userBusList_play[0]
            self.userBusList_play.append(self.userBusList_play[0])
            del self.userBusList_play[0]
        self.userSemaphore.release()
        return nextbus

    def checkBus(self, bus):
        if bus in self.userBusList:
            return True
        else :
            return False
    def checkupdate(self):
        self.userSemaphore.acquire()
        print("="*25)
        count = 1
        for bus in self.userBusList_play:
            print(str(count) + bus.busNumber)
            count = count + 1
        print("="*25)
        self.userSemaphore.release()
    
class Control:
    def __init__(self,main):
        self.TTS = main.tts
        self.userBus = main.userBus
        self.main = main
        self.__playListSemaphore = Semaphore(1)       #멀티쓰레드로 인해 playlist 동시접근 에러를 방지하기 위한 세마포어
        self.playlist = []    #세마포어로 충돌 해결
        self.TTS.SetChannelVolume(-0.5,soundChannel=1)
   
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
                self.TTS.playVoice(self.playlist[0].busNumber,self.TTS.status.button_2_Push_Succes,"현재",'c'+self.playlist[0].location,self.TTS.status.bus_before_station,soundChannel=1)
                print("버스 등록 : " +str(self.playlist[0].busNumber))
            else:
                self.TTS.playVoice(self.TTS.status.button_2_Push_Fail,"현재",'c'+self.playlist[0].location,self.TTS.status.bus_before_station,soundChannel=1)
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
        if self.main.systemState :
            self.main.systemState = False
            self.TTS.setPlayStop(0)
            self.TTS.setPlayStop(1)
            self.TTS.playVoice(voice,self.TTS.status.end_program)

    def CamCheckBus(self,busCarNumber):
        if busCarNumber != None:
            b=self.main.bus.CampareCarNumber(busCarNumber)
            
            if bool(b):
                self.TTS.playVoice(self.TTS.status.bus_stop,b.busNumber,"입니다")
            
                print("버스 도착 : " + str(b.busNumber) )

                if self.userBus.checkBus(b):
                    busDel_Thread = Thread(target=self.enterBusDelete,args=(b,))  # LED를 위해 조금 기다렸다가 삭제
                    busDel_Thread.start()

                
    def enterBusDelete(self,b):
        print("버스 진입 음성출력 성공 : "+b.busNumber)
        time.sleep(5)
        self.userBus.endDelete(b)

        #if not self.userBus.nextBus():
        #    self.SystemEnd(self.TTS.status.error_bus_not)



    def LEDLoop(self):
        while True:
            if not self.main.systemState:
                print("EndLEDLoop")
                return
            bus = self.userBus.nextBus()
            
            if bus :
                self.main.led.SET_LED(bus.busNumber)
                time.sleep(2)
            else :
                self.main.led.OFF_LED()
            
            if self.main.bus.checkState():
                self.SystemEnd(self.TTS.status.error_bus_not)
         





class LoopSystem:

    def __init__(self,args):
        
        self.kySocket = mySocket(self,args.socket_ip,args.socket_port) #arg port 넣기
        self.button = MyButton(self)
        self.tts = busPlayList(keyData.TTS_client_id, keyData.TTS_client_secret)
        self.userBus = UserBus()
        self.control = Control(self)
        self.bus = StationDict(self, args.stationID, keyData.serviceKey, args.url)  # 순서 중요 tts -> userBus-> control -> bus
        self.led = LED()
        
        self.updateCycle = args.updateCycle
    
        self.systemState = False  # 시스템 상태(default : 대기)

    def loopStart(self):
        try :

            while True:
                # 시스템 자고 있으면 깨우기(버튼 체크)_버튼 눌리면일어남
                while not self.systemState:
                    self.systemState = self.button.wakeUpTest()

                self.tts.playVoice(self.tts.status.button_1_Info,soundChannel=0)
                self.tts.setPlayStop(1)
                
                while self.tts.getChannelState()[0] or self.tts.getChannelState()[1]:
                    pass

                self.userBus.reset()
                self.bus.reset()

                button_Thread = Thread(target=self.button.checkButton)  # 버튼 입력 시작
                busUpdate_Thread = Thread(target=self.bus.loopUpdate, args=(self.updateCycle,))  # 버스 정보 갱신 시작
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
                
                self.led.OFF_LED()
                print("sleepSystem")
                self.systemState = False

        except(KeyboardInterrupt, SystemExit):
            print("keyboardInterrupt")
            self.systemState = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('socket_ip', help='sub process ip')
    parser.add_argument('socket_port', help='sub process port',type=int)
    parser.add_argument('--url', help='bus info api url')
    parser.add_argument('--stationID', help='stationID, default=> keDate.py', default='203000165')
    parser.add_argument('--updateCycle', help='bus info update cycle time', default=10)
    args = parser.parse_args()
    
    
    loop = LoopSystem(args)
    loop.loopStart()
