import cv2
import numpy as np
from PIL import Image
import pytesseract
import re
import math

class busCarNumberDetect:
    def __init__(self,camName):
        self.__cap = cv2.VideoCapture(camName)
        if not self.__cap.isOpened():
            print("cap openc error")
            exit()

        #print('width: {}, height : {}, frame : {}'.format(w,h,f))
        w = int(self.__cap.get(3))
        h = int(self.__cap.get(4))
        f = int(self.__cap.get(5))
        #fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        #self.__outVideo = cv2.VideoWriter('output.avi', fourcc, f, (w,h))


        self.__net = cv2.dnn.readNet("obj_60000.weights", "obj.cfg")
        self.__classes = []
        with open("obj.names", "r") as f:
            self.__classes = [line.strip() for line in f.readlines()]
        layer_names = self.__net.getLayerNames()
        self.__output_layers = [layer_names[i[0] - 1] for i in self.__net.getUnconnectedOutLayers()]
    
    def __dnn_detect(self,img):
            height, width, channels = img.shape

            # Detecting objects
            blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            self.__net.setInput(blob)
            outs = self.__net.forward(self.__output_layers)

            class_ids = []
            confidences = []
            boxes = []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    if class_id != 7: ## only bus number 
                        continue
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        
                        # Object detected
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        # 좌표
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        
                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
    
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            return boxes, indexes,class_ids

    def __OCR(self,inputImg):
        
        gray = cv2.cvtColor(inputImg, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 700, 350, apertureSize = 5, L2gradient = True)
        cv2.imshow("canny",canny)
        lines = cv2.HoughLinesP(canny, 1, np.pi / 180, 50, minLineLength = 3, maxLineGap = 150)
        angle = 0
        maxdim = 0
        if not (lines is None):
            for i in lines:
                xdim = i[0][2] - i[0][0]
                ydim = i[0][3] - i[0][1]
                iangle = math.atan2(ydim, xdim)*180/np.pi
                dim = math.sqrt((xdim * xdim) + (ydim * ydim))
                if abs(angle) < 40 and maxdim < dim:
                    maxdim = dim
                    angle =iangle
                    
        roih, roiw, roic = inputImg.shape
        matrix = cv2.getRotationMatrix2D((roiw/2, roih/2), angle, 1)
        roi = cv2.warpAffine(inputImg, matrix, (roiw, roih))
        cv2.imshow("tessroi",roi)     
        r = pytesseract.image_to_string(roi, lang='Hangul')
        return r
        

    def detect(self):
        
        ret, img = self.__cap.read()
        if not ret:
            print("ret error")
            return
        
        height, width, channels = img.shape

        boxes,indexes,class_ids= self.__dnn_detect(img)


        font = cv2.FONT_HERSHEY_PLAIN
        resultNumberList = []
        for i in range(len(boxes)):
            if i in indexes:

                x, y, w, h = boxes[i]

                label = str(self.__classes[class_ids[i]])

                    
                paddingx = -int(w * 0.05)
                paddingy = int(h * 0.1)
                px1 = x - paddingx*2 if x-paddingx >= 0 else 0
                px2 = x + w + paddingx if x + w + paddingx <= width else width
                py1 = y - paddingy if y-paddingy >= 0 else 0
                py2 = y + h + paddingy if y+h+paddingy <= height else height
                    
                roi = img[py1:py2, px1:px2]

                r = self.__OCR(roi)

                rNumberlist= re.findall("\d+",r)
                carnum = ""
                for num in rNumberlist:
                    if len(num) >= 4:
                        carnum=num[-4:]

                resultNumberList.append(carnum)

                cv2.imshow('roi',roi)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0,0,255), 2)
                cv2.putText(img, label+"  "+carnum, (x, y + 30), font, 3, (0,0,255), 3)

        cv2.imshow("Image", img)
        #self.__outVideo.write(img)
        print(resultNumberList)
        return resultNumberList
    def End(self):
        self.__cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    s=busCarNumberDetect(0)
    while True:
        print(s.detect())

        if cv2.waitKey(1) > 0:
            s.End()
            break


