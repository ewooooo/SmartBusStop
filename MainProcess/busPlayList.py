import keyData

from threading import Thread

from baseModule.TTSModule import TTS

class busPlayList(TTS):

    def __init__(self,client_id, client_secret):
        TTS.__init__(self, client_id, client_secret)
        self.__defaultVoiceMake()

    class status:
        # 대기모드 해제
        button_1_Info = "button_1_Info"
        # 버스 등록
        button_2_Push_Succes = "button_2_Push_Succes"
        button_2_Push_Fail = "button_2_Push_Fail"
        # 버스 등록 취소
        button_3_Cancel = "button_3_Cancel"
        button_3_Cancel_Fail = "button_3_Cancel_Fail"
        # 버스 상태 안내
        bus_before_station = "bus_before_station"
        bus_before_number = ["한","두","세","네","다섯","여섯","일곱","여덟","아홉","열"]
        
        bus_arrive = "bus_arrive"
        bus_stop ="bus_stop"
        #안내 버스 없음
        error_station_info = "error_station_info"
        error_bus_not ="error_bus_not"
        #대기 모드로 전환
        end_program = "end_program"
        #추가 접미사들
        tts_conneter= ["현재","입니다"]
        
    def __defaultVoiceMake(self):
        
        # 대기모드 해제
        self.tts_api("손잡이를 돌려 탑승하려는 버스를 선택하고 버튼을 누르면 버스기사에게 전달하여 탑승을 도와드립니다",self.status.button_1_Info)
        self.tts_api( "버스가 등록되었습니다. 등록하신 버스가 아니시면 버튼을 길게 눌러주세요",self.status.button_2_Push_Succes)
        self.tts_api("버스가 이미등록되어있습니다.",self.status.button_2_Push_Fail)
        self.tts_api("버스가 등록취소되었습니다",self.status.button_3_Cancel)
        self.tts_api( "취소할 버스가 없습니다. 손잡이를 돌려 버스를 선택하고 버튼을 눌러 등록해주세요.",self.status.button_3_Cancel_Fail)
        self.tts_api("정거장 전에 있습니다",self.status.bus_before_station)
        self.tts_api("버스가 잠시후에 도착합니다",self.status.bus_arrive)
        self.tts_api("현재 정류장에 진입하는 버스는 ",self.status.bus_stop)
        self.tts_api("현재 정류장 정보가 없습니다. 관리자에게 문의해주세요.",self.status.error_station_info)
        self.tts_api("현재 운행중인 버스가 없습니다.",self.status.error_bus_not)
        self.tts_api("대기모드로 전환합니다.",self.status.end_program)
        c = 0
        for n in self.status.bus_before_number: #10까지 숫자
            self.tts_api(n,'c'+str(c))
            c = c+1
        for n in range(20):
            self.tts_api(str(c),'c'+str(c)) #11~30 숫자
            c = c+1
        for n in self.status.tts_conneter: #추가접미사
            self.tts_api(n,n)
            
    def addBusData(self, bus):  # 버스 추가 될때 실행되야함.
        if self.tts_api(bus.busNumber + "번", bus.busNumber):
            return True
        else:
            return False

 
 



if __name__ == "__main__":
    
    def thread1():
        tts.playVoice(tts.status.bus_stop,"29","입니다",soundChannel=0)
        #tts.playVoice(,"8",soundChannel=1)

    def thread2():
        tts.playVoice(tts.status.button_1_Info,"1","2","1","2","3","1","2","3",soundChannel=1)

    tts = busPlayList(keyData.TTS_client_id,keyData.TTS_client_secret)
    button_Thread = Thread(target=thread1)  # 연산 시작
    button_Thread2 = Thread(target=thread2)  # 연산 시작
    button_Thread.start()
    button_Thread2.start()
    button_Thread.join()
    button_Thread2.join()