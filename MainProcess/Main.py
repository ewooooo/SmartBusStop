import time
from threading import Thread
# from multiprocessing import Process, Manager
# from multiprocessing.managers import BaseManager

from my_socket import *
from myButton import *
#from Bus import BusList
#from TTS import *

class status:
    status_1_ActivateCamera = '1'
    status_0_EndCamera = '0'
    status_2_BusWaiting = '2'
    status_3_BusStop = '3'


class LoopSystem:

    def __init__(self):
        self.mysocket = mySocket()
        self.button = MyButton(self)
        #self.bus = BusList(self)
        #self.tts = TTS(self)

        self.systemState = False    # 시스템 상태(default : 대기)

        self.stateBusStop = 0
        #test
        self.listTest = []

        # self.socketManager = Manager()
        # self.mysocket = self.socketManager.mySocket()
        # self.buttonManager = Manager()
        # self.button = self.buttonManager.MyButton()
        # self.busManager = Manager()
        # self.bus = self.busManager.BusList()
        # self.userBusManager = Manager()
        # self.userBus = self.userBusManager.UserBusList()


    def Control(self):
        while True:
            # self.listTest.append("Control")
            # time.sleep(1)

            if self.bus.userState(): #저장된 버스가 있고
                checkBusList = self.bus.enterUserBus()
                if not checkBusList: # 버스 상태가 진입중인 요소가 없으면
                    continue
                else:
                    if stateBusStop == status.status_0_EndCamera:
                        self.mysocket.Send(status.status_1_ActivateCamera)
                        stateBusStop == status.status_1_ActivateCamera

                    if mySocket.checkRecvBuffer():
                        carNumberCV=self.mysocket.RecvCheckOut()
                        for checkBus in checkBusList
                            if checkBus == carNumberCV:
                                #tts 진입 정보 수정
                                stateBusStop =
                    
                    
                    
                            


                        
                    # secondprocess한테 1 보내서 영상 내놔라 하고
                    # 큐에 정보 들어왔으면 체크 해서 tts 조정하고
                    # 큐에 보내기(1);

                    # 보내고서 대기상태는 1
                    # 큐에 들어왔으니 번호판 대조해봐라 0
                    # 정차한 차량있으니 검사해서 바꿔바라 2 (이방법은 opencv 에서 검출범위네 누적을 이용하여 확인하고)
                    # 다른 숫자는 error 모든 정보 초기화하고 시스템 종료 안내 하고 수면상태로 만듬.

                    # 시각장애인이 버스에 탑승하여 큐에서 버스 번호를 내보내는 조건은 버스가 정차했는지 안내하는것이다.
                    # 따라서 영상에서 버스가 대조 됬음에도 차량정차 시그널은 없다면 시간 카운팅해서 도착했거나 정차하지 않고 떠났을 수도 있다고 안내해주고 다음 버스 정차 스케줄도 안내해준다.

                    # 처음에 대조한 버스가 있다그러면 지금부터는 무한 루프돌려서 상태유지 시켜야된다
                    # 즉 대조된 버스가 왔는지 지나갔는지 판별하는게 중요
                    # 근데 그러면 연달아 오는 다른 버스를 타는 뒷 시각장애인 있다고하면 안됨.
                    
                   
                    print("정보요청")

    def loopStart(self):

        while True:
            # 시스템 자고 있으면 깨우기(버튼 체크)_버튼 눌리면일어남
            while not self.systemState:
                self.systemState = self.button.wakeUpTest()

            socket_Thread = Thread(target=self.mysocket.RecvLoop)   # 메인 통신 시작
            button_Thread = Thread(target=self.button.checkButton)  # 버튼 입력 시작
            # busUpdate_Thread = Thread(target=self.bus.update)       # 버스 정보 갱신 시작
            # TTS_Thread = Thread(target=self.tts.playTTS)            # 음성 안내 시작
            # Control_Thread = Thread(target=self.Control)          # 연산 시작

            socket_Thread.start()
            button_Thread.start()
            # busUpdate_Thread.start()
            # TTS_Thread.start()
            # Control_Thread.start()

            socket_Thread.join()
            button_Thread.join()
            # busUpdate_Thread.join()
            # TTS_Thread.join()
            # Control_Thread.join()

            self.systemState = False





if __name__ == "__main__":
    print("Start")

    loop = LoopSystem()
    loop.loopStart()

