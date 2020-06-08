import time
from threading import Thread

from my_socket import *
from myButton import *
from Bus import *
from TTS import *

import keyData

#===========test=======
from OpenCV_Socket import ServerSocket
#========================

class busPlayList(TTS):
    class status:
        # 상태 파일 네임
        button_1_Info = "button_1_Info"
        button_2_Push_Succes = "button_2_Push_Succes"
        button_2_Push_Fail = "button_2_Push_Fail"
        button_3_Cancel = "button_3_Cancel"
        button_3_Cancel_Fail = "button_3_Cancel_Fail"
        bus_state = "bus_state"
        bus_state_error = "bus_state_error"
        bus_arrive = "bus_arrive"
        bus_stop = "bus_stop"
        bus_before_1_station = "bus_before_1_station"
        bus_before_2_station = "bus_before_2_station"
        bus_before_3_station = "bus_before_3_station"
        bus_no_stop = "bus_no_stop"
        error_bus_not = "error_bus_not"
        error_inf_not = "error_inf_not"

    def __init__(self, obj,client_id, client_secret):
        self.main = obj
        self.nowPlay = None
        self.playInfo = None
        self.playInfoBus = None
        self.busStatePlay = False
        TTS.__init__(self, client_id, client_secret)
        self.tts_api("탑승하고자 하는 버스 번호가 들리면 안내가 모두 끝난 후 버튼을 누르세요", self.status.button_1_Info)
        self.tts_api("버스가 등록되었습니다. 등록하신 버스가 아니시면 버튼을 길게 눌러주시고 등록된 버스를 확인하려면 버튼을 두번 누르세요!", self.status.button_2_Push_Succes)
        self.tts_api("버스가 이미등록되어있습니다.", self.status.button_2_Push_Fail)
        self.tts_api("최근 등록한 버스가 취소되었습니다", self.status.button_3_Cancel)
        self.tts_api("버스가 등록되어있습니다", self.status.bus_state)
        self.tts_api("현재 등록된 버스가 없습니다.", self.status.bus_state_error)
        self.tts_api("취소할 버스가 없습니다", self.status.button_3_Cancel_Fail)
        self.tts_api("버스가 잠시후에 도착합니다", self.status.bus_arrive)
        self.tts_api("버스가 정차했습니다. 다시 한번 버스정차소리와 문열림 소리를 듣고 안전에 유의하여 탑승하시기 바랍니다.", self.status.bus_stop)
        self.tts_api("버스가  한정거장 전에 있습니다   ", self.status.bus_before_1_station)
        self.tts_api("버스가  두정거장 전에 있습니다   ", self.status.bus_before_2_station)
        self.tts_api("버스가  세정거장 전에 있습니다   ", self.status.bus_before_3_station)
        self.tts_api("버스 정차를 파악할 수 없습니다. 정차하지 않았거나 식별하지 못한 경우일 수 있으니 확인후 탑승 부탁드립니다. 다시 안내를 받으려면 해당 번호가 나오는 시점에 버튼을 눌러주세요", self.status.bus_no_stop)
        self.tts_api("현재 조회할수 있는 버스 정보가 없습니다.", self.status.error_bus_not)
        self.tts_api("현재 등록할수 있는 버스가 없습니다.", self.status.error_inf_not)
    def busPlay(self, bus):
        busState = int(bus.location)
        print(bus.busNumber+" : "+str(busState))
        if busState == 1:
            self.play(bus.busNumber)
            self.play(self.status.bus_before_1_station)
            if self.playStop:
                self.playStop = False
                time.sleep(1)
        elif busState == 2:
            self.play(bus.busNumber)
            self.play(self.status.bus_before_2_station)
            if self.playStop:
                self.playStop = False
                time.sleep(1)
        elif busState == 3:
            self.play(bus.busNumber)
            self.play(self.status.bus_before_3_station)
            if self.playStop:
                self.playStop = False
                time.sleep(1)
        elif busState == 0:
            self.play(bus.busNumber)
            self.play(self.status.bus_arrive)
            if self.playStop:
                self.playStop = False
                time.sleep(1)
        elif busState == -2: # 여기 수정하면 control 도 수정해야함
            self.play(bus.busNumber)
            self.play(self.status.bus_stop)
            bus.location = -1
            if self.playStop:
                self.playStop = False
        elif busState == -3:
            self.play(bus.busNumber)
            self.play(self.status.bus_no_stop)
            bus.location = -1
            if self.playStop:
                self.playStop = False
                time.sleep(1)

    def playLoop(self):
        while True:

            if bool(self.playInfo) or bool(self.playInfoBus):
                if bool(self.playInfoBus):
                    self.play(self.playInfoBus.busNumber)
                self.playInfo = None
                self.playInfoBus = None
                self.play(self.playInfo)
                if self.playStop:
                    self.playStop = False
                    time.sleep(1)

            elif self.busStatePlay:
                if not self.main.userBus.userBusList:
                    self.play(self.status.bus_state_error)
                else:
                    for key in self.main.userBus.userBusList.keys():
                        bus = self.main.userBus.userBusList.get(key)
                        self.play(bus.busNumber)
                    self.play(self.status.bus_state)
                self.busStatePlay = False
                if self.playStop:
                    self.playStop = False
                    time.sleep(1)

            else:
                if bool(self.playlist):

                    self.playlist.append(self.playlist[0])
                    del self.playlist[0]
                    if int(self.playlist[0].location) <= 3 and int(self.playlist[0].location) >= -3:
                        self.busPlay(self.playlist[0])
                        self.nowPlay = self.playlist[0]

            if not self.main.systemState:
                print("endTTS")
                return

    def addBusData(self, bus):  # 버스 추가 될때 실행되야함.
        if self.tts_api(bus.busNumber + "번", bus.busNumber):
            self.playlist.append(bus)
        else:
            print("error")
        pass

    def priorityBUS(self, bus):
        self.playlist.remove(bus)
        self.playlist.insert(1, bus)

    def getNowPlayBus(self):
        return self.nowPlay

    def playButtonInfo(self, state, bus=None):

        if state == self.status.button_2_Push_Succes:
            self.playInfoBus = bus
            self.playInfo = self.status.button_2_Push_Succes
            self.setPlayStop()
        elif state == self.status.button_2_Push_Fail:
            self.playInfoBus = bus
            self.playInfo = self.status.button_2_Push_Fail
            self.setPlayStop()
        elif state == self.status.button_3_Cancel:
            self.playInfo = self.status.button_3_Cancel
            self.setPlayStop()
        elif state == self.status.button_3_Cancel_Fail:
            self.playInfo = self.status.button_3_Cancel_Fail
            self.setPlayStop()
        elif state == self.status.error_inf_not:
            self.playInfo = self.status.error_inf_not
            self.setPlayStop()


    def busStateInfo(self):
        self.busStatePlay = True
        self.setPlayStop()

    def playStartInfo(self):
        self.play(self.status.button_1_Info)
    def errorNotBusInfo(self):
        self.play(self.status.error_bus_not)

class UserBus:
    def __init__(self):
        self.userBusList = {}
        self.recentBus = None

    def add(self, bus):  # userbus add
        if not bus.routeId in self.userBusList and int(bus.location) <= 3 and int(bus.location) >= -3:
            self.recentBus = bus.routeId
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
    def endDelete(self, bus):
        del self.userBusList[bus.routeId]

    def getEnterUserBus(self):
        # carNumber in userBusList 요소가 있는지 확인 T/F
        if not self.userBusList:
            return None
        userbusEnter = []
        for key in self.userBusList.keys():
            bus = self.userBusList.get(key)
            if int(bus.location) == 1:
                userbusEnter.append(bus)
        return userbusEnter

    def checkBus(self):
        if not self.userBusList:
            return False  # 비어있으면
        else:
            return True


class status:
    status_1_ActivateCamera = '1'
    status_0_EndCamera = '0'
    status_2_BusWaiting = '2'
    status_3_BusStop = '3'
    status_reset = '-1'


class LoopSystem:
    #============test=================
    class Button:
        def __init__(self, obj):
            self.main = obj
            print("makebutton")

        def checkButton(self):
            while True:
                time.sleep(5)
                print("checkButton")
                #self.main.tts.playButtonInfo(self.main.tts.status.button_3_Cancel)
                #self.main.tts.playButtonInfo(self.main.tts.status.button_3_Cancel_Fail)
                #self.main.systemState = False

                print("oneClick")
                nowbus = self.main.tts.getNowPlayBus()
                if not nowbus:
                    self.main.tts.playButtonInfo(self.main.tts.status.error_inf_not)
                else:
                    if self.main.userBus.add(nowbus):
                        self.main.tts.playButtonInfo(self.main.tts.status.button_2_Push_Succes, nowbus)
                    else:
                        self.main.tts.playButtonInfo(self.main.tts.status.button_2_Push_Fail, nowbus)

                if not self.main.systemState:
                    return

                time.sleep(5)
                print("longClick")
                if self.main.userBus.delete():
                    self.main.tts.playButtonInfo(self.main.tts.status.button_3_Cancel)
                else:
                    self.main.tts.playButtonInfo(self.main.tts.status.button_3_Cancel_Fail)
                time.sleep(5)
                print("oneClick")
                nowbus = self.main.tts.getNowPlayBus()
                if self.main.userBus.add(nowbus):
                    self.main.tts.playButtonInfo(self.main.tts.status.button_2_Push_Succes, nowbus)
                else:
                    self.main.tts.playButtonInfo(self.main.tts.status.button_2_Push_Fail, nowbus)
                time.sleep(5)
                self.main.tts.busStateInfo()


        def wakeUpTest(self):
            return True

    # ============test=================
    def __init__(self):
        # #######test#######
        self.kySocket = ServerSocket()
        #
        # self.button = self.Button(self)
        # ################

        #self.kySocket = mySocket(keyData.HOST,keyData.PORT)
        self.button = MyButton(self)

        self.tts = busPlayList(self, keyData.TTS_client_id, keyData.TTS_client_secret)
        self.bus = StationDict(self, keyData.stationNumber, keyData.serviceKey)  # 순서 중요 tts -> bus

        self.userBus = UserBus()

        self.systemState = False  # 시스템 상태(default : 대기)

    def Control(self):

        stationState = status.status_0_EndCamera
        recvBuffer = None
        waitBusBuffer = []
        while True:
            EndTest = True
            if bool(self.bus.busDict):
                for bkey in self.bus.busDict.keys():
                    bus = self.bus.busDict.get(bkey)
                    if bus.plateNo != '-1':
                        EndTest = False
                        break
            if EndTest:
                self.systemState = False
                time.sleep(1) #tts 꺼지길 기다리기
                self.tts.errorNotBusInfo()
                return



            if self.userBus.checkBus():  # 저장된 버스가 있고
                checkBusList = self.userBus.getEnterUserBus()
                if not checkBusList:  # 버스 상태가 진입중인 요소가 없으면
                    #영상처리 프로세서 초기화 및 연결상태점검
                    recvBuffer = self.kySocket.Send_Recv(status.status_reset)
                    if recvBuffer[0] != status.status_reset:
                        print("통신 실패")
                    continue
                else:
                    # 카메라가 작동하지 않는 상태라면 영상을 켜서 정보를 달라고한다.
                    if stationState == status.status_0_EndCamera or stationState == status.status_1_ActivateCamera:
                        recvBuffer = self.kySocket.Send_Recv(stationState)
                        print(recvBuffer)
                        if recvBuffer[0] == status.status_1_ActivateCamera:
                            stationState = status.status_1_ActivateCamera
                            if recvBuffer[1] != None:
                                for bus in checkBusList:
                                    if bus.location == recvBuffer[1]:
                                        # tts 진입 정보 수정
                                        self.tts.priorityBUS(bus)
                                        waitBusBuffer.append(bus)
                                        stationState = status.status_2_BusWaiting
                                        break;
                        else:
                            print("통신실패")


                    elif stationState == status.status_2_BusWaiting:
                        recvBuffer = self.kySocket.Send_Recv(stationState)
                        if recvBuffer[0] == status.status_2_BusWaiting:     # [2, (0_버스 발견못함 1_버스 발견됨 2_버스 정차함 -1_대기 시간초과(버싀나감)), 버스번호]
                            if recvBuffer[1] == '0':
                                continue
                            elif recvBuffer[1] == '1':
                                for bus in checkBusList:
                                    if bus in waitBusBuffer:
                                        continue
                                    if bus.location == recvBuffer[2]:
                                        # tts 진입 정보 수정
                                        bus.location = -2
                                        self.tts.priorityBUS(bus)
                                        waitBusBuffer.append(bus)
                                        stationState = status.status_2_BusWaiting
                                        break;
                            elif recvBuffer[1] =='2':
                                for bus in waitBusBuffer:
                                    if bus.location == recvBuffer[2]:
                                        bus.location = -3
                                        self.tts.priorityBUS(bus)
                                        waitBusBuffer.remove(bus)
                                        self.userBus.endDelete(bus)
                                        if not waitBusBuffer:
                                            if self.userBus.checkBus():
                                                stationState = status.status_1_ActivateCamera
                                            else:
                                                self.systemState = False
                                                return

                            elif recvBuffer[1] =='-1':
                                for bus in waitBusBuffer:
                                    if bus.location == recvBuffer[2]:
                                        bus.location = -2
                                        self.tts.priorityBUS(bus)
                                        waitBusBuffer.remove(bus)
                                        self.userBus.endDelete(bus)
                                        if not waitBusBuffer:
                                            if self.userBus.checkBus():
                                                stationState = status.status_1_ActivateCamera
                                            else:
                                                self.systemState = False
                                                return
                        else:
                            print("통신실패")
            if not self.systemState:
                return



    def loopStart(self):

        while True:
            # 시스템 자고 있으면 깨우기(버튼 체크)_버튼 눌리면일어남
            while not self.systemState:
                self.systemState = self.button.wakeUpTest()
            self.tts.playStartInfo()

            button_Thread = Thread(target=self.button.checkButton)  # 버튼 입력 시작
            busUpdate_Thread = Thread(target=self.bus.loopUpdate, args=(keyData.updateCycle,))  # 버스 정보 갱신 시작
            TTS_Thread = Thread(target=self.tts.playLoop)  # 음성 안내 시작
            Control_Thread = Thread(target=self.Control)  # 연산 시작

            button_Thread.start()
            busUpdate_Thread.start()
            TTS_Thread.start()
            Control_Thread.start()

            button_Thread.join()
            busUpdate_Thread.join()
            TTS_Thread.join()
            Control_Thread.join()

            self.systemState = False
            print("endProcess")


if __name__ == "__main__":
    print("Start")

    loop = LoopSystem()
    loop.loopStart()
