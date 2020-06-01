from urllib.request import urlopen
import xml.etree.ElementTree as ET
import requests

url = "http://openapi.gbis.go.kr/ws/rest/busarrivalservice/station?serviceKey=1234567890&stationId=203000165&"
response = requests.get(url)
text = response.text
root = ET.fromstring(text)

route1 = ''
route1list = []
plate1 = ''
plate1list = []
plate2 = ''
plate2list = []
for child in root:
    # print(child.tag, child.attrib)
    for kid in child:
        # print(kid.tag, kid.attrib)
        for ac in kid:
            for routeId in ac.iter('routeId'):
                route1 = routeId.text

            for plateNo1 in ac.iter('plateNo1'):
                plate1 = plateNo1.text

            for plateNo2 in ac.iter('plateNo2'):
                plate2 = plateNo2.text

            route1list.append(route1)
            plate1list.append(plate1)
            plate2list.append(plate2)
route1list = ' '.join(route1list).split()
# plate1list = ' '.join(plate1list).split()
# plate2list = ' '.join(plate2list).split()

route1list = list(set(route1list))
plate1list = list(set(plate1list))
plate2list = list(set(plate2list))


print(route1list)
print(plate1list)
print(plate2list)
# total = {route1list: (plate1list, plate2list)}
# print(total.items())


            # 리스트 형태로 값을 받아들여서 리스트 내의 빈칸과 중복값을 제거해주고 딕셔너리리 형태로 완성