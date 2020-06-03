
import os
import sys
import pygame
import urllib.request
import time


class TTS() :
    def __init__(self, client_id, client_secret):
        # print("makeTTS")
        # self.main = obj
        self.nowPlay = None
        self.playlist = []
        pygame.mixer.init()

        url = "https://naveropenapi.apigw.ntruss.com/voice/v1/tts"
        self.request = urllib.request.Request(url)
        self.request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
        self.request.add_header("X-NCP-APIGW-API-KEY", client_secret)

    def tts_api(self, textdata, mp3FileName):

        fileName = "sound/" + mp3FileName + ".mp3"
        data = "speaker=mijin&speed=1&text=" + textdata

        response = urllib.request.urlopen(self.request, data=data.encode('utf-8'))

        rescode = response.getcode()
        if (rescode == 200):

            response_body = response.read()
            with open(fileName, 'wb') as f:
                f.write(response_body)
        else:
            print("Error Code:" + rescode)

    def play(self,busNumber, busState):
        self.nowPlay = busNumber
        fileName = "sound/"+busNumber + ".mp3"

        pygame.mixer.music.load(fileName)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue

        fileName = "sound/"+busState + ".mp3"

        pygame.mixer.music.load(fileName)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue

        print("test")

    def playState(slef,playSound):

        fileName = "sound/"+playSound + ".mp3"

        pygame.mixer.music.load(fileName)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue

    def updatePlayList(self):
        self.playlist

    def playLoop(self):
        while True:
            if self.playList:
                self.play()


            #print("playTTS : ")
            #print(self.main.listTest)
            #del self.main.listTest[:]
            #time.sleep(3)




#
# if __name__ == "__main__":
#     tts = TTS("id","secret")
#     tts.tts_api("4000번","4000")
#     tts.tts_api("버스가 잠시후에 도착합니다","arrive")
#     tts.tts_api("탑승하고자 하는 버스 번호가 들리면 버튼을 누르세요.","pushbutton")
#     tts.tts_api("버스가 등록되었습니다. 등록하신 버스가 아니시면 버튼을 눌러주세요","cancel")
#     tts.tts_api("버스가 진입중입니다.","come")
#     tts.tts_api("버스가 정차하였습니다. 사고예방을 위해 차량 정차 소리와 문 열림 소리를 반드시 듣고 탑승해주세요", "stop")
#
#     tts.play("4000","arrive")
#     tts.playState("pushbutton")