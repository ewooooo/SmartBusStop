import os
import sys
import pygame
import urllib.request
import time
import keyData
class TTS() :
    def __init__(self, client_id, client_secret):
        self.playlist = []
        pygame.mixer.init()

        url = "https://naveropenapi.apigw.ntruss.com/voice/v1/tts"
        self.request = urllib.request.Request(url)
        self.request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
        self.request.add_header("X-NCP-APIGW-API-KEY", client_secret)

        self.playStop = False
    def tts_api(self, textdata, mp3FileName):   # mp3 받아오는 파일

        fileName = "sound/" + mp3FileName + ".mp3"
        data = "speaker=mijin&speed=2&text=" + textdata

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

    def play(self,playName):
        fileName = "sound/"+playName + ".mp3"

        pygame.mixer.music.load(fileName)
        pygame.mixer.music.play()
        if self.playStop:
            return
        while pygame.mixer.music.get_busy() == True:
            if self.playStop:
                return
            continue

    def setPlayStop(self):
        self.playStop = True

    def addPlayData(self, textdata,playName):
        if self.tts_api(textdata,playName):
            self.playlist.append(playName)
        else :
            print("error")

    def playLoop(self):
        while True:
            if self.playList:
                self.play(self.playlist[0])
                self.playlist.append(self.playlist[0])
                del self.playList[0]






if __name__ == "__main__":

    tts = TTS(keyData.TTS_client_id,keyData.TTS_client_secret)
    tts.addPlayData("4000번","4000")
    tts.addPlayData("버스가 잠시후에 도착합니다.","arrive")
    tts.addPlayData("탑승하고자 하는 버스 번호가 들리면 버튼을 누르세요.","pushbutton")
    tts.addPlayData("버스가 등록되었습니다. 등록하신 버스가 아니시면 버튼을 눌러주세요","cancel")
    tts.addPlayData("버스가 진입중입니다.","come")
    tts.addPlayData("버스가 정차하였습니다. 사고예방을 위해 차량 정차 소리와 문 열림 소리를 반드시 듣고 탑승해주세요", "stop")

#
    tts.play("4000")

    tts.play("arrive")
    tts.play("4000")

    tts.play("arrive")
#     tts.play("pushbutton")