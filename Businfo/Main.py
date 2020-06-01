from urllib.request import urlopen
import xml.etree.ElementTree as ET
import requests

url = "http://openapi.gbis.go.kr/ws/rest/busarrivalservice/station?serviceKey=1234567890&stationId=203000165&"
response = requests.get(url)
text = response.text
root = ET.fromstring(text)


class bus:
    def __init__(self,routeId,plateNo1,location1):
        self.routeId = routeId
        self.plateNo1 = plateNo1
        self.locationNo1 = location1
busDict= {}
routenamelist = []
for child in root:
    if child.tag != 'msgBody':
        continue
    for kid in child:
        route1 , plate1, location1  = "","",""
        for ac in kid:
            if ac.tag == "routeId": #노선번호
                route1 = ac.text

            if ac.tag == "plateNo1": #먼저 도착하는 버스번호
                plate1 = ac.text

            if ac.tag == "locationNo1": #먼저 도착하는 버스의 남은 정거장
                location1 = ac.text

            # route1 : plate1, location1, plate2, location2
        busDict[route1]= bus(route1,plate1,location1)

print(busDict.keys()) #결과 확인
for a in busDict.keys():            #결과 확인
    b = busDict.get(a)
    # print("버스 번호 :" + b.routeId)
    # print("버스 번호판 : " + b.plateNo1)
    # print("남은 정거장 : " + b.locationNo1)
routenamelist = []
for c in busDict.keys():
    url1 = "http://openapi.gbis.go.kr/ws/rest/busrouteservice/info?serviceKey=1234567890&routeId="
    url2 = url1 + c
    # print(url2)
    responseroute = requests.get(url2)
    textroute = responseroute.text
    rootroute = ET.fromstring(textroute)
    for top in rootroute:
        if top.tag != 'msgBody':
            continue
        for mid in top:
            for bot in mid:
                if bot.tag == "routeName":  # 노선번호
                    routenamelist = bot.text
                    print(routenamelist)

                # 리스트 형태로 값을 받아들여서 리스트 내의 빈칸과 중복값을 제거해주고 딕셔너리리 형태로 완성