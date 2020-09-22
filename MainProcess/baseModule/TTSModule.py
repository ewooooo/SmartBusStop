import os
import sys
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

        self.playStop = (False, -1)
        self.playlist = []

        pygame.mixer.init()
       

    def tts_api(self, textdata, mp3FileName):   # mp3 받아오는 파일

        fileName = "sound/" + mp3FileName + ".wav"
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
            self.playlist.append(playName)
        else :
            print("error")


    def __play(self,playName,soundChannel=0):
        sChannel = pygame.mixer.Channel(soundChannel)

        fileName = "sound/" + playName + ".wav"

        playSound=pygame.mixer.Sound(fileName)
        sChannel.play(playSound)

        while sChannel.get_busy() == True:
            continue

    def __playwiat_1min(self,soundChannel=0):

        sChannel = pygame.mixer.Channel(soundChannel)

        fileName = "./wait_1min.wav"

        playSound=pygame.mixer.Sound(fileName)
        sChannel.play(playSound)

        while sChannel.get_busy() == True:
            continue


    def __playSet(self, pList, soundChannel=0):
        for p in pList:
            if p != None:
                self.__play(p,soundChannel=soundChannel)
            if self.playStop[0] and self.playStop[1] == soundChannel:
                return
        self.__playwiat_1min(soundChannel=soundChannel)

    
    def playVoice(self, play1, play2=None, play3=None, play4=None, play5=None, soundChannel=0):
        pList = [play1,play2,play3,play4,play5]
        player_Thread = Thread(target=self.__playSet,args=(pList,soundChannel))  # 재생될때 다른작업과 관련없지 재생되도록
        player_Thread.start()


    def setPlayStop(self,soundChannel=0):
        while self.playStop[0]:
            pass
        self.playStop = (True, soundChannel)
        pygame.mixer.Channel(soundChannel).stop()
        self.playStop = (False,-1)
 
 
    def playLoop(self,soundChannel=0):
        sChannel = pygame.mixer.Channel(soundChannel) # argument must be int
        while True:
            if self.playList:
                self.play(self.playlist[0])
                self.playlist.append(self.playlist[0])
                del self.playList[0]












def thread1():
    tts.playVoice("cancel","arrive",soundChannel=0)
    tts.playVoice("arrive","4000",soundChannel=1)


def thread2():
    pass
    #tts.playSet("cancel","pushbutton","stop",soundChannel=1)



if __name__ == "__main__":

    tts = TTS(keyData.TTS_client_id,keyData.TTS_client_secret)


    button_Thread = Thread(target=thread1)  # 연산 시작
    button_Thread2 = Thread(target=thread2)  # 연산 시작

    button_Thread.start()
    button_Thread2.start()

    button_Thread.join()
    button_Thread2.join()

    # tts.addPlayData("4000번","4000")
    # tts.addPlayData("버스가 잠시후에 도착합니다.","arrive")
    # tts.addPlayData("탑승하고자 하는 버스 번호가 들리면 버튼을 누르세요.","pushbutton")
    # tts.addPlayData("버스가 등록되었습니다. 등록하신 버스가 아니시면 버튼을 눌러주세요","cancel")
    # tts.addPlayData("버스가 진입중입니다.","come")
    # tts.addPlayData("버스가 정차하였습니다. 사고예방을 위해 차량 정차 소리와 문 열림 소리를 반드시 듣고 탑승해주세요", "stop")

#
    # tts.play("4000",1)

    # tts.play("arrive",0)
    # tts.play("4000")

    # tts.play("arrive")
    # tts.playwiat_1min()
    # tts.play("pushbutton")