#include <opencv2/opencv.hpp> // Include 'OpenCV' library.

#include <string>
#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>

#include <iostream>
using namespace cv;
using namespace std;

int main()
{
    tesseract::TessBaseAPI api;
    api.SetPageSegMode(tesseract::PSM_AUTO);                                //segmentation on auto
    api.Init("/usr/local/share/","eng");                                    //path = parent directory of tessdata
    pFile = fopen("home/leejb1217/SmartBusStop/Tesseract Linux/test.jpg");  //Open picture
    PIX* image;                                                             //Image format from leptonica
    image = pixReadStramBmp(pFile);
    fclose(pFile);
    api.SetImage(image);                                                    //Run the OCR
    char* textOutput = new char[512];
    textOutput = api.GetUTF8Text();                                         // Get the text
}