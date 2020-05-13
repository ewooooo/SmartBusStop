import time
import multiprocessing
import socket


class Button:
    def checkButton(self):
        print("checkButton")

    def oneClick(self):
        print("oneClick")

    def doubleClick(self):
        print("doubleClick")

    def longClick(self):
        print("longClick")
    def wakeUpTest(self):
        print("wakeUp")
        LoopSystem.systemState = True;

class Bus:
    def __init__(self, busNumber, carNumber, state):
        self.busNumber = busNumber
        self.carNumber = carNumber
        self.state = state


class BusList:
    def __init__(self):
        self.busList = []

    def update(self):
        next()  # 기존꺼는 그대로 남기고 중복 제거해야한다.


class UserBusList(BusList): #main button controler
    def update(self):
        next()

    def add(self, bus):
        self.busList.append(bus)

    def delete(self, bus):
        self.busList.remove(bus)

    def state(self):
        if not self.busList:
            return True
        else:
            return False

    def searchBus(self, imgCarNumber):
       for b in self.busList:
           if b.carNumber == imgCarNumber:
               return b
        return None


class TTS:
    nowSpeakBus = None



class LoopSystem:
    button = Button()  # 클래스 변수(static 변수)
    userBusList = UserBusList()
    busList = BusList()
    systemState = False
    def __init__(self,rxtx):
        self.secondProcess = rxtx
    def loopStart(self):
        while (True):
            #시스템 자고 있으면 깨우기(버튼 체크)_버튼 눌리면일어남
            while not self.systemState:
                self.button.wakeUpTest()

            # 멀티 테스킹 필요
            self.userBusList.update()
            self.busList.update()
            if self.userBusList.state():
                print("정보요청")
                if Communication.buffer

class Communication:
    HOST = '192.168.35.163'  # Server IP or Hostname
    PORT = 12345  # Pick an open Port (1000+ recommended), must match the client sport

    buffer = []
    def __init__(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')

        # managing error exception
        try:
            s.bind((self.HOST, self.PORT))
        except socket.error:
            print('Bind failed ')
        s.listen(5)
        print('Socket awaiting messages')
        (self.clientsocket, self.address) = s.accept()
        print('Connected')

    def RecvLoop(self):
        # awaiting for message
        while True:
            data = self.clientsocket.recv(1024)
            print('I sent a message back in response to: ' + data)
            reply = ''
            # process your message
            if data == 'Hello':
                reply = 'Hi, back!'
            elif data == 'This is important':
                reply = 'OK, I have done the important thing you have asked me!'
            # and so on and on until...
            elif data == 'quit':
                self.clientsocket.send('Terminating')
                break
            else:
                reply = 'Unknown command'
            self.clientsocket.send(reply)   # Sending reply
        self.clientsocket.close()           # Close connections

    def Send(self):
        next()
    def checkBuffer(self):
        value = self.buffer
        self.buffer.clear()
        return value


if __name__ == "__main__":
    rxtx = Communication()
    loop = LoopSystem(rxtx)
    loop.loopStart()


    # self 는 this 랑 동일하다.
    # class Student(Person): 상속 방법
    # def __init__(self): 생성자
    # def __del__(self): 소멸자
    # def __repr__(self): 프리팅
    # def __add__(self, other): 덧셈연산
    # def __cmp__(self, other): 비교연산