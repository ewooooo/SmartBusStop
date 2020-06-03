import time
from threading import Thread
# from multiprocessing import Process, Manager
# from multiprocessing.managers import BaseManager

from my_socket import *
#from myButton import *
from Bus import *
from TTS import *

import keyData


class busPlayList(TTS):


    class status:
        # 상태 파일 네임
        button_1_Info = "button_1_Info"
        button_2_Push_Succes = "button_2_Push_Succes"
        button_2_Push_Fail = "button_2_Push_Fail"
        button_3_Cancel = "button_3_Cancel"
        button_3_Cancel_Fail = "button_3_Cancel_Fail"
        button_4_doubleClick = "button_4_doubleClick"
        bus_arrive = "bus_arrive"
        bus_before_1_station = "bus_before_1_station"
        bus_before_2_station = "bus_before_2_station"
        bus_before_3_station = "bus_before_3_station"

    def __init__(self,client_id, client_secret):
        self.nowPlay = None
        TTS.__init__(self,client_id, client_secret)
        # self.tts_api("탑승하고자 하는 버스 번호가 들리면 버튼을 누르세요", self.status.button_1_Info)
        # self.tts_api("버스가 등록되었습니다. 등록하신 버스가 아니시면 버튼을 길게 눌러주세요", self.status.button_2_Push_Succes)
        # self.tts_api("버스가 이미등록되어있습니다.", self.status.button_2_Push_Fail)
        # self.tts_api("버스가 취소되었습니다", self.status.button_3_Cancel)
        # self.tts_api("취소할 버스가 없습니다", self.status.button_3_Cancel_Fail)
        # self.tts_api("버튼을 한번만 눌러주세요", self.status.button_4_doubleClick)
        # self.tts_api("버스가 잠시후에 도착합니다", self.status.bus_arrive)
        # self.tts_api("버스가  한정거장 전에 있습니다", self.status.bus_before_1_station)
        # self.tts_api("버스가  두정거장 전에 있습니다", self.status.bus_before_2_station)
        # self.tts_api("버스가  세정거장 전에 있습니다", self.status.bus_before_3_station)

    def busPlay(self, bus):
        busState = int(bus.location)
        if busState == 1:
            self.play(bus.busNumber)
            self.play(self.status.bus_before_1_station)
        elif busState == 2:
            self.play(bus.busNumber)
            self.play(self.status.bus_before_2_station)
        elif busState == 3:
            self.play(bus.busNumber)
            self.play(self.status.bus_before_3_station)
        elif busState == 0:
            self.play(bus.busNumber)
            self.play(self.status.bus_arrive)

    def playLoop(self):
        while True:
            if bool(self.playlist):
                self.nowPlay = self.playlist[0]
                self.busPlay(self.playlist[0])
                self.playlist.append(self.playlist[0])
                del self.playlist[0]

    def addBusData(self, bus): # 버스 추가 될때 실행되야함.
        if self.tts_api(bus.busNumber+"번",bus.busNumber):
            self.playlist.append(bus)
        else :
            print("error")
        pass

    def priorityBUS(self,bus):
        self.playlist.remove(bus)
        self.playlist.insert(1, bus)

    def getNowPlayRout(self):
        return self.nowPlay.busNumber

    def playButtonInfo(self,state,bus):
        bus.busNumber
        if state == self.status.button_2_Push_Succes:
            pass
        elif state == self.status.button_2_Push_Fail:
            pass
        elif state == self.status.button_3_Cancel:
            pass
        elif state == self.status.button_3_Cancel_Fail:
            pass
        elif state == self.status.button_4_doubleClick:
            pass

    def playStartInfo(self):
        self.play(self.status.button_1_Info)

    def arriveBus(self):
        self.playlist.remove(bus)
        self.playlist.insert(1, bus)




class UserBus:
    def __init__(self):
        self.userBusList = {}
        self.recentBus = None

    def add(self, bus):  # userbus add
        if not bus:
            self.recentBus = bus
            self.userBusList[bus.routeId] = bus
            return True
        else:
            return False

    def delete(self):  # userbus del
        if self.recentBus in self.userBusList:
            del self.userBusList[self.recentBus]
            return True
        else:
            return False


    def getEnterUserBus(self):
        # carNumber in userBusList 요소가 있는지 확인 T/F
        userbusEnter = []
        for key in self.userBusList.keys():
            bus = self.userBusList.get(key)
            if int(bus.location) == 1:
                userbusEnter.append(bus)
        return userbusEnter

    def checkBus(self):
        if not self.userBusList:
            return False # 비어있으면
        else:
            return True

class status:
    status_1_ActivateCamera = '1'
    status_0_EndCamera = '0'
    status_2_BusWaiting = '2'
    status_3_BusStop = '3'
    status_5_checkState = '5'


class LoopSystem:
    def __init__(self):
        self.kySocket = mySocket(keyData.HOST,keyData.PORT)
        # self.button = MyButton(self)

        self.tts = busPlayList(keyData.TTS_client_id, keyData.TTS_client_secret)
        self.bus = StationDict(self,keyData.stationNumber,keyData.serviceKey) # 순서 중요 tts -> bus

        self.userBus = UserBus()

        self.systemState = False    # 시스템 상태(default : 대기)


    def Control(self):
        arriveCheckBus = None
        stationState = status.status_0_EndCamera
        while True:

            if self.userBus.checkBus(): #저장된 버스가 있고
                checkBusList = self.userBus.getEnterUserBus()
                if not checkBusList: # 버스 상태가 진입중인 요소가 없으면
                    continue
                else:
                    if stationState == status.status_0_EndCamera:
                        if self.kySocket.Send_Recv(status.status_1_ActivateCamera)[0] == status.status_1_ActivateCamera:
                            stationState = status.status_1_ActivateCamera
                        else:
                            self.kySocket.Send_Recv(status.status_1_ActivateCamera)
                            stationState = status.status_1_ActivateCamera

                    elif stationState == status.status_1_ActivateCamera:
                        response = self.kySocket.Send_Recv(status.status_5_checkState)
                        if response[0] == status.status_5_checkState:
                            for bus in checkBusList:
                                if response[1] == '0':
                                if bus.location == response[2]:
                                    #tts 진입 정보 수정
                                    self.tts.priorityBUS(bus)
                                    stationState = status.status_2_BusWaiting
                                    arriveCheckBus = bus
                                    if self.kySocket.Send_Recv(status.status_2_BusWaiting)[0] == status.status_2_BusWaiting:
                                        stationState = status.status_2_BusWaiting
                                    else:
                                        self.kySocket.Send_Recv(status.status_2_BusWaiting)
                                        stationState = status.status_2_BusWaiting

                    elif stationState == status.status_2_BusWaiting:
                        response = self.kySocket.Send_Recv(status.status_5_checkState)
                        if response[0] == status.status_5_checkState:
                            if response[1] == '-1':
                                if response[2] == arriveCheckBus.busNumber:
                                    arriveCheckBus.station = '0'
                                    del self.userBus.userBusList[arriveCheckBus.routeId]
                                    arriveCheckBus = None
                                    stationState == status.status_3_BusStop
                    elif stationState == status.status_3_BusStop:
                        arriveCheckBus = None
                        if self.kySocket.Send_Recv(status.status_3_BusStop)[0] == status.status_3_BusStop:
                            stationState = status.status_1_ActivateCamera
                        else:
                            self.kySocket.Send_Recv(status.status_3_BusStop)
                            stationState = status.status_1_ActivateCamera
            else :
                if stationState == status.status_3_BusStop:
                    arriveCheckBus = None
                    if self.kySocket.Send_Recv(status.status_0_EndCamera)[0] == status.status_0_EndCamera:
                        stationState = status.status_0_EndCamera
                    else:
                        self.kySocket.Send_Recv(status.status_0_EndCamera)
                        stationState = status.status_0_EndCamera


    def loopStart(self):

        while True:
            # 시스템 자고 있으면 깨우기(버튼 체크)_버튼 눌리면일어남
            while not self.systemState:
                #self.systemState = self.button.wakeUpTest()
                break
            self.tts.playStartInfo()

            #socket_Thread = Thread(target=self.kySocket.RecvLoop)   # 메인 통신 시작
            # button_Thread = Thread(target=self.button.checkButton)  # 버튼 입력 시작
            busUpdate_Thread = Thread(target=self.bus.loopUpdate, args=(keyData.updateCycle,))       # 버스 정보 갱신 시작
            TTS_Thread = Thread(target=self.tts.playLoop)            # 음성 안내 시작
            Control_Thread = Thread(target=self.Control)          # 연산 시작

            #socket_Thread.start()
            #button_Thread.start()
            busUpdate_Thread.start()
            TTS_Thread.start()
            Control_Thread.start()

            #socket_Thread.join()
            #button_Thread.join()
            busUpdate_Thread.join()
            TTS_Thread.join()
            Control_Thread.join()

            self.systemState = False





if __name__ == "__main__":
    print("Start")

    loop = LoopSystem()
    loop.loopStart()

