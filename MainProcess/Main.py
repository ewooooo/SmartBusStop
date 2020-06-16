import time
from threading import Thread

from my_socket import *
from myButton import *
from Bus import *
from TTS import *
from LED import *
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
        bus_before_4_station = "bus_before_4_station"
        bus_before_5_station = "bus_before_5_station"
        bus_before_6_station = "bus_before_6_station"
        bus_before_7_station = "bus_before_7_station"
        bus_before_8_station = "bus_before_8_station"
        bus_before_9_station = "bus_before_9_station"
        bus_before_10_station = "bus_before_10_station"

        bus_no_stop = "bus_no_stop"
        error_bus_not = "error_bus_not"
        error_inf_not = "error_inf_not"
        end_program = "end_program"

    def __init__(self, obj,client_id, client_secret):
        self.main = obj
        self.nowPlay = None
        self.playInfo = None
        self.playInfoBus = None
        self.busStatePlay = False
        self.busStopCommand = False
        self.StopBus =None
        self.endState = False
        TTS.__init__(self, client_id, client_secret)



        # 대기모드 해제
        self.tts_api("탑승하고자 하는 버스 번호가 들리면 버튼을 누르세요", self.status.button_1_Info)
        # 버스 등록
        self.tts_api("버스가 등록되었습니다. 등록하신 버스가 아니시면 버튼을 길게 눌러주시고 등록된 버스를 확인하려면 버튼을 두번 누르세요!", self.status.button_2_Push_Succes)    # + 버스번호
        self.tts_api("버스가 이미등록되어있습니다.", self.status.button_2_Push_Fail)     # + 버스번호
        self.tts_api("현재 등록할수 있는 버스가 없습니다.", self.status.error_inf_not)
        # 버스 등록 0취소
        self.tts_api("최근 등록한 버스가 취소되었습니다", self.status.button_3_Cancel)
        self.tts_api("취소할 버스가 없습니다", self.status.button_3_Cancel_Fail)
        # 등록된 버스 조회
        self.tts_api("버스가 등록되어있습니다", self.status.bus_state)     # + 버스번호
        self.tts_api("현재 등록된 버스가 없습니다.", self.status.bus_state_error)
        # 버스 상태 안내
        self.tts_api("버스가  한정거장 전에 있습니다", self.status.bus_before_1_station)          # + 버스번호
        self.tts_api("버스가  두정거장 전에 있습니다", self.status.bus_before_2_station)          # + 버스번호
        self.tts_api("버스가  세정거장 전에 있습니다", self.status.bus_before_3_station)          # + 버스번호
        self.tts_api("버스가  네정거장 전에 있습니다", self.status.bus_before_4_station)          # + 버스번호
        self.tts_api("버스가  다섯정거장 전에 있습니다", self.status.bus_before_5_station)        # + 버스번호
        self.tts_api("버스가  여섯정거장 전에 있습니다", self.status.bus_before_6_station)        # + 버스번호
        self.tts_api("버스가  일곱정거장 전에 있습니다", self.status.bus_before_7_station)        # + 버스번호
        self.tts_api("버스가  여덟정거장 전에 있습니다", self.status.bus_before_8_station)        # + 버스번호
        self.tts_api("버스가  아홉정거장 전에 있습니다", self.status.bus_before_9_station)        # + 버스번호
        self.tts_api("버스가  열정거장 전에 있습니다", self.status.bus_before_10_station)         # + 버스번호
        # 영상으로 버스를 인식했을때
        self.tts_api("버스가 잠시후에 도착합니다", self.status.bus_arrive)      # + 버스번호
        # 영상으로 버스 정차를 인식했을때
        self.tts_api("버스가 정차했습니다. 다시 한번 버스정차소리와 문열림 소리를 듣고 안전에 유의하여 탑승하시기 바랍니다.", self.status.bus_stop)     # + 버스번호
        # 버스 정차를 인식하지 못했거나 버스가 정차하지 않았을 경우
        self.tts_api("버스 정차를 파악할 수 없습니다. 정차하지 않았거나 식별하지 못한 경우일 수 있으니 확인후 탑승 부탁드립니다. 다시 안내를 받으려면 해당 번호가 나오는 시점에 버튼을 눌러주세요", self.status.bus_no_stop)     # + 버스번호

        #대기 모드로 전환
        self.tts_api("이후 등록된 버스가 없어 대기모드로 전환합니다.", self.status.end_program)


    def busPlay(self, bus):
        busState = int(bus.location)
        print(bus.busNumber+" : "+str(busState))
        if busState == 1:
            self.play(bus.busNumber)
            self.play(self.status.bus_before_1_station)
            self.playwiat_1min()
            if self.playStop:
                self.playStop = False
                time.sleep(1)
        elif busState == 2:
            self.play(bus.busNumber)
            self.play(self.status.bus_before_2_station)
            self.playwiat_1min()
            if self.playStop:
                self.playStop = False
                time.sleep(1)
        elif busState == 3:
            self.play(bus.busNumber)
            self.play(self.status.bus_before_3_station)
            self.playwiat_1min()
            if self.playStop:
                self.playStop = False
                time.sleep(1)
        elif busState == 4:
            self.play(bus.busNumber)
            self.play(self.status.bus_before_4_station)
            self.playwiat_1min()
            if self.playStop:
                self.playStop = False
                time.sleep(1)
        elif busState == 5:
            self.play(bus.busNumber)
            self.play(self.status.bus_before_5_station)
            self.playwiat_1min()
            if self.playStop:
                self.playStop = False
                time.sleep(1)
        elif busState == 6:
            self.play(bus.busNumber)
            self.play(self.status.bus_before_6_station)
            self.playwiat_1min()
            if self.playStop:
                self.playStop = False
                time.sleep(1)
        elif busState == 7:
            self.play(bus.busNumber)
            self.play(self.status.bus_before_7_station)
            self.playwiat_1min()
            if self.playStop:
                self.playStop = False
                time.sleep(1)
        elif busState == 8:
            self.play(bus.busNumber)
            self.play(self.status.bus_before_8_station)
            self.playwiat_1min()
            if self.playStop:
                self.playStop = False
                time.sleep(1)
        elif busState == 9:
            self.play(bus.busNumber)
            self.play(self.status.bus_before_9_station)
            self.playwiat_1min()
            if self.playStop:
                self.playStop = False
                time.sleep(1)
        elif busState == 10:
            self.play(bus.busNumber)
            self.play(self.status.bus_before_10_station)
            self.playwiat_1min()
            if self.playStop:
                self.playStop = False
                time.sleep(1)


    def playLoop(self):

        while True: #버튼 안내메시지 출력
            if not self.main.systemState:
                print("endTTS")
                return
            if bool(self.playInfo) or bool(self.playInfoBus):
                if bool(self.playInfoBus):
                    self.play(self.playInfoBus.busNumber)
                playInfo = self.playInfo
                self.playInfo = None
                self.playInfoBus = None
                self.play(playInfo)
                self.playwiat_1min()

                if self.playStop:
                    self.playStop = False
                    time.sleep(1)

            elif self.busStopCommand:
                self.busStopPlay(self.StopBus)
                self.busStopCommand = False
                self.StopBus = None

            elif self.busStatePlay: #등록된 버스 전보 보기
                if not self.main.userBus.userBusList:
                    self.play(self.status.bus_state_error)
                else:
                    for key in self.main.userBus.userBusList.keys():
                        bus = self.main.userBus.userBusList.get(key)
                        self.play(bus.busNumber)
                    self.play(self.status.bus_state)
                    self.playwiat_1min()
                self.busStatePlay = False
                if self.playStop:
                    self.playStop = False
                    time.sleep(1)

            else:
                if bool(self.playlist):

                    self.playlist.append(self.playlist[0])
                    del self.playlist[0]
                    if int(self.playlist[0].location) <= 10 and self.playlist[0].state ==0:
                        self.nowPlay = self.playlist[0]
                        self.busPlay(self.playlist[0])






    def addBusData(self, bus):  # 버스 추가 될때 실행되야함.
        if self.tts_api(bus.busNumber + "번", bus.busNumber):
            self.playlist.append(bus)
        else:
            print("error")

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
        self.main.systemState = False
        self.setPlayStop()
        self.play(self.status.error_bus_not)

    def busStopInfo(self,bus,state):
        if state == -1: #진입중이다
            self.busStopCommand = True
            self.StopBus = bus
            self.setPlayStop()
        elif state == -2: #정차했다
            bus.state = 0
            self.busStopCommand = True
            self.StopBus = bus
            self.setPlayStop()

        elif state == -3: #지나갔다
            bus.state = 0
            self.busStopCommand = True
            self.StopBus = bus
            self.setPlayStop()
            bus.state = 0

    def busStopPlay(self,bus):
        busState = bus.state
        if busState == -1:
            self.play(bus.busNumber)
            self.play(self.status.bus_arrive)
            self.playwiat_1min()
            if self.playStop:
                self.playStop = False
                time.sleep(1)
        elif busState == -2: # 여기 수정하면 control 도 수정해야함
            self.play(bus.busNumber)
            self.play(self.status.bus_stop)
            self.playwiat_1min()
            bus.state = 0
            if self.playStop:
                self.playStop = False
                time.sleep(1)
        elif busState == -3:
            self.play(bus.busNumber)
            self.play(self.status.bus_no_stop)
            self.playwiat_1min()
            bus.state = 0
            if self.playStop:
                self.playStop = False
                time.sleep(1)
        if self.endState:
            self.play(self.status.end_program)
            self.main.systemState = False
            return

    def ENDPROGRAM(self):
        self.endState = True

class UserBus:
    def __init__(self):
        self.userBusList = {}
        self.recentBus = None

    def add(self, bus):  # userbus add
        if not bus.routeId in self.userBusList and int(bus.location) <= 10:
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
        while True:
            try:
                userbusEnter = []
                if bool(self.userBusList):
                    keys = self.userBusList.keys()
                    for key in keys:
                        bus = self.userBusList.get(key)
                        if bool(bus):
                            if int(bus.location) == 1:
                                userbusEnter.append(bus)
                    return userbusEnter
                else:
                    return None
            except:
                print("errortest")
                continue

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

    def __init__(self):

        self.kySocket = mySocket(keyData.HOST,keyData.PORT)
        self.button = MyButton(self)

        self.tts = busPlayList(self, keyData.TTS_client_id, keyData.TTS_client_secret)
        self.bus = StationDict(self, keyData.stationNumber, keyData.serviceKey)  # 순서 중요 tts -> bus
        self.led = LED()
        self.userBus = UserBus()

        self.systemState = False  # 시스템 상태(default : 대기)

    def Control(self):

        stationState = status.status_0_EndCamera
        cycleNumer = 0
        while True:
            if self.bus.kaCount != cycleNumer:
                cycleNumer = self.bus.kaCount
                recvBuffer = self.kySocket.Send_Recv(str(cycleNumer+3))
                if recvBuffer[0] != status.status_reset:
                    print("통신 실패")

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
                while True:
                    try:
                        if bool(self.userBus.userBusList):
                            keys = self.userBus.userBusList.keys()
                            for bkey in keys:
                                bus =self.userBus.userBusList.get(bkey)
                                if bus.state != 0:
                                    if bus.location != 1:
                                        bus.state = -3
                                        self.tts.busStopInfo(bus, -3)
                                        self.userBus.endDelete(bus)
                                        print("Test3")
                                        if self.userBus.checkBus():
                                            stationState = status.status_1_ActivateCamera
                                        else:
                                            self.tts.ENDPROGRAM()
                        break
                    except:
                        print("errortest")
                        continue

                checkBusList = self.userBus.getEnterUserBus()
                if bool(checkBusList):  # 버스 상태가 진입중인 요소가 없으면
                    # 카메라가 작동하지 않는 상태라면 영상을 켜서 정보를 달라고한다.
                    if stationState == status.status_0_EndCamera or stationState == status.status_1_ActivateCamera:
                        recvBuffer = self.kySocket.Send_Recv(stationState)

                        if recvBuffer[0] == status.status_1_ActivateCamera:
                            stationState = status.status_1_ActivateCamera

                            if recvBuffer[1] != None:
                                for bus in checkBusList:
                                    print("Test1")
                                    print(recvBuffer)
                                    print(bus.plateNo[len(bus.plateNo) - 4:])
                                    if bus.plateNo[len(bus.plateNo) - 4:] == recvBuffer[1]:
                                        # tts 진입 정보 수정
                                        bus.state = -1  # 진입중 기다리자
                                        self.tts.busStopInfo(bus, -1)
                                        stationState = status.status_2_BusWaiting
                                        break
                        else:
                            print("통신실패")


                    elif stationState == status.status_2_BusWaiting:
                        recvBuffer = self.kySocket.Send_Recv(stationState)
                        if recvBuffer[
                            0] == status.status_2_BusWaiting:  # [2, (0_버스 발견못함 1_버스 발견됨 2_버스 정차함 -1_대기 시간초과(버싀나감)), 버스번호]
                            if recvBuffer[1] == '0':
                                continue
                            elif recvBuffer[1] == '1':
                                for bus in checkBusList:
                                    if bus.plateNo[len(bus.plateNo) - 4:] == recvBuffer[2]:
                                        # tts 진입 정보 수정
                                        bus.state = -1  # 진입중 기다리자
                                        self.tts.busStopInfo(bus, -1)
                                        stationState = status.status_2_BusWaiting
                                        break
                            elif recvBuffer[1] == '2':
                                for bus in checkBusList:
                                    if bus.plateNo[len(bus.plateNo) - 4:] == recvBuffer[2]:
                                        bus.state = -2
                                        self.tts.busStopInfo(bus, -2)
                                        self.userBus.endDelete(bus)
                                        print("Test2")
                                        if self.userBus.checkBus():
                                            stationState = status.status_1_ActivateCamera
                                        else:
                                            self.tts.ENDPROGRAM()

                            elif recvBuffer[1] == '-1':
                                for bus in checkBusList:
                                    if bus.plateNo[len(bus.plateNo) - 4:] == recvBuffer[2]:
                                        bus.state = -3
                                        self.tts.busStopInfo(bus, -3)
                                        self.userBus.endDelete(bus)
                                        print("Test3")
                                        if self.userBus.checkBus():
                                            stationState = status.status_1_ActivateCamera
                                        else:
                                            self.tts.ENDPROGRAM()
                            else:
                                print("통신실패1")
                        else:
                            print("통신실패1")
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
