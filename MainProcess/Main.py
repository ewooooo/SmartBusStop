import time
from threading import Thread
# from multiprocessing import Process, Manager
# from multiprocessing.managers import BaseManager

from my_socket import *
from myButton import MyButton
from Bus import BusList
from TTS import *

# class MyManager(BaseManager): pass
#
# def Manager():
#     m = MyManager()
#     m.start()
#     return m
#
# MyManager.register('mySocket',mySocket)
# MyManager.register('MyButton',MyButton)
#

class LoopSystem:

    def __init__(self):
        self.mysocket = mySocket(self)
        self.button = MyButton(self)
        self.bus = BusList()
        self.tts = TTS(self)


        self.systemState = False


        #test
        self.listTest = [0]

        # self.socketManager = Manager()
        # self.mysocket = self.socketManager.mySocket()
        # self.buttonManager = Manager()
        # self.button = self.buttonManager.MyButton()
        # self.busManager = Manager()
        # self.bus = self.busManager.BusList()
        # self.userBusManager = Manager()
        # self.userBus = self.userBusManager.UserBusList()


    def Controll(self):
        while True:
            if self.bus.userState(): #저장된 버스가 있고
                checkBusList = self.bus.enterUserBus()
                if not checkBusList: # 버스 상태가 진입중이면
                    continue
                else:
                    checkBusList # secondprocess한테 1 보내서 영상 내놔라 하고
                                    # 큐에 정보 들어왔으면 체크 해서 tts 조정하고
                                    #
                    print("정보요청")

    def loopStart(self):
        #시스템 자고 있으면 깨우기(버튼 체크)_버튼 눌리면일어남
        while(True):

            # 시스템 자고 있으면 깨우기(버튼 체크)_버튼 눌리면일어남
            while not self.systemState:
                self.systemState = self.button.wakeUpTest()

            socketProcess = Thread(target=self.mysocket.RecvLoop) #메인 통신 시작
            buttonProcess = Thread(target=self.button.checkButton) #버튼 입력 시작
            busUpdateProcess = Thread(target=self.bus.update)
            TTSProcess = Thread(target=self.tts.playTTS)

            socketProcess.start()
            buttonProcess.start()
            busUpdateProcess.start()
            TTSProcess.start()

            socketProcess.join()
            buttonProcess.join()
            busUpdateProcess.join()
            TTSProcess.join()

            self.systemState = False

            
        


if __name__ == "__main__":
    print("Start")

    loop = LoopSystem()
    loop.loopStart()

