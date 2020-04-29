#include <opencv2/opencv.hpp> // Include 'OpenCV' library.

#include <string>
#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>

#include <iostream>
using namespace cv;
using namespace std;


int main()
{
	
	Mat test = imread("./test.jpg");
		
	Mat GaussIMG;
	Mat Ggrays;
	cvtColor(test, GaussIMG, COLOR_BGR2GRAY);
	Mat test1;
	cvtColor(GaussIMG,Ggrays,COLOR_GRAY2BGR);
	GaussianBlur(Ggrays, test1, Size(5, 5), 0);	
	imshow("tset",test1);
	
	

	string outText;
	tesseract::TessBaseAPI *ocr = new tesseract::TessBaseAPI();

	ocr->Init(NULL, "kor", tesseract::OEM_LSTM_ONLY);
	ocr->SetPageSegMode(tesseract::PSM_AUTO);

	ocr->SetImage(test1.data, test1.cols, test1.rows, 3, test1.step);
	outText = string(ocr->GetUTF8Text());
	cout << outText;
	ocr->End();

	waitKey();
	return 0;
}
