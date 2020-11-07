import os
import sys

project_dir=os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(project_dir)
import pygame
import urllib.request
import keyData
from threading import Thread



class TTS() :
    def __init__(self, client_id, client_secret):

        url = "https://naveropenapi.apigw.ntruss.com/voice/v1/tts"
        self.request = urllib.request.Request(url)
        self.request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
        self.request.add_header("X-NCP-APIGW-API-KEY", client_secret)

        self.playStop = (False, -1)         #Stop 또한 한개 메소드로 두채널 관리하기 위함
        self.play_state = [False, False]    #채널 상태 체크
     
        pygame.mixer.init()
       

    def tts_api(self, textdata, mp3FileName):   # mp3 받아오는 파일

        fileName =project_dir+ "/sound/" + mp3FileName + ".wav"
        data = "speaker=mijin&format=wav&speed=2&text=" + textdata

        response = urllib.request.urlopen(self.request, data=data.encode('utf-8'))

        rescode = response.getcode()
        if (rescode == 200):

            response_body = response.read()
            with open(fileName, 'wb') as f:
                f.write(response_body)
            return True

        else:
            print("Error Code:" + rescode)
            return False


    def addPlayData(self, textdata,playName):
        if self.tts_api(textdata,playName):
            return True
        else :
            return False


    def __play(self,playName,soundChannel=0):
        sChannel = pygame.mixer.Channel(soundChannel)

        fileName = project_dir+ "/sound/" + playName + ".wav"

        playSound=pygame.mixer.Sound(fileName)
        sChannel.play(playSound)

        while sChannel.get_busy() == True:
            continue

    def __playwiat_1min(self,soundChannel=0):

        sChannel = pygame.mixer.Channel(soundChannel)

        fileName = project_dir+ "/baseModule/wait_1min.wav"

        playSound=pygame.mixer.Sound(fileName)
        sChannel.play(playSound)

        while sChannel.get_busy() == True:
            continue


    def __playSet(self, pList, soundChannel=0):
        self.setPlayStop(soundChannel)
        
        while self.play_state[soundChannel] :   # 다음꺼를 실행하기전에 이전 음성 완전히 종료되길 기다림
            pass
        self.play_state[soundChannel] = True    # 실행 상태 전이

        for p in pList:
            if p != None:
                self.__play(p,soundChannel=soundChannel)

            if self.playStop[0] and self.playStop[1] == soundChannel:   # 중지요청에 따른 종료
                break
        self.play_state[soundChannel] = False   # 종료되면 상태 해제

    
    def playVoice(self, play1, play2=None, play3=None, play4=None, play5=None,play6=None,play7=None,play8=None,play9=None,play10=None, soundChannel=0):
        pList = [play1,play2,play3,play4,play5,play6,play7,play8,play9,play10]
        player_Thread = Thread(target=self.__playSet,args=(pList,soundChannel))  # 재생될때 다른작업과 관련없지 재생되도록
        player_Thread.start()


    def setPlayStop(self,soundChannel=0):
        while self.playStop[0]:     #두 채널를 한개에 매소드로 동시에 처리하기 위함 세마포어같은거
            pass
        self.playStop = (True, soundChannel)        # 재생 정지 요청
        pygame.mixer.Channel(soundChannel).stop()   # pygame 재생 정지

        while self.play_state[soundChannel] :       # 완전히 재생이 정지되면 변수 초기화
            pass
        self.playStop = (False,-1)
 






if __name__ == "__main__":
    tts = TTS(keyData.TTS_client_id,keyData.TTS_client_secret)
    tts.addPlayData("4000번","4000")
    tts.addPlayData("버스가 잠시후에 도착합니다.","arrive")
    tts.addPlayData("탑승하고자 하는 버스 번호가 들리면 버튼을 누르세요.","pushbutton")
    tts.addPlayData("버스가 등록되었습니다. 등록하신 버스가 아니시면 버튼을 눌러주세요","cancel")

    def thread1():
        tts.playVoice("4000","arrive",soundChannel=0)
        #tts.playVoice("","",soundChannel=1)

    def thread2():
        tts.playVoice("pushbutton","4000","cancel","4000","4000","4000","4000","4000","4000","4000",soundChannel=1)

    button_Thread = Thread(target=thread1)  # 연산 시작
    button_Thread2 = Thread(target=thread2)  # 연산 시작
    button_Thread.start()
    button_Thread2.start()
    button_Thread.join()
    button_Thread2.join()
