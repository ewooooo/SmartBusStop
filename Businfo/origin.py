from urllib.request import urlopen
import xml.etree.ElementTree as ET
import requests

url = "http://openapi.gbis.go.kr/ws/rest/busarrivalservice/station?serviceKey=1234567890&stationId=200000078&"
response = requests.get(url)
text = response.text
root = ET.fromstring(text)

for child in root:
    # print(child.tag, child.attrib)
    for kid in child:
        # print(kid.tag, kid.attrib)
        for ac in kid:
            # print(type(ac.tag))
            # print(type(ac.text))
            # print(ac.tag+ac.text)
            for routeId in ac.iter('routeId'):
                route1 = routeId.text
                # print(routeId.text)
            for plateNo1 in ac.iter('PlateNo1'):
                plate1 = plateNo1.text
                # plateNo1.text
                # print(plateNo1.text)
            for plateNo2 in ac.iter('plateNo2'):
                plate2 = plateNo2.text
                # plateNo2.text
                # print(plateNo2.text)
            total = {route1:(plate1,plate2)}
            print(total.items())