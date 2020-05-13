import time
from threading import Thread
from multiprocessing import Process, Queue
from my_socket import *
#from Button import *


class LoopSystem:
    
    #button = Button()  # 클래스 변수(static 변수)
    #busList = BusList()
    #userBusList = UserBusList()
    #tts = TTS()
    
    systemState = False
    


    # def __init__(self):
    #     next()

    # def Controll(self):
    #     if self.userBusList.state():
    #             print("정보요청")
    #             if Communication.buffer

    def loopStart(self):
        #시스템 자고 있으면 깨우기(버튼 체크)_버튼 눌리면일어남
        while(True):
            print("test1")
            # while not self.systemState:
            #     self.button.wakeUpTest()

            # th0 = Thread(target=Button.checkButton(), args=()) #버튼 입력 시작
            # th3 = Thread(target=self.Controll())
            
            # socketThtread.start()
            # socketThtread.join()

            



if __name__ == "__main__":
    mysocket = mySocket()#소켓 연결
    loop = LoopSystem()   

    socketThtread = Thread(target=mysocket.RecvLoop(), args=()) #메인 통신 시작
    LoopThtread = Thread(target=loop.loopStart(), args=()) #통신시작

    socketThtread.start()
    LoopThtread.start()
    socketThtread.join()
    LoopThtread.join()