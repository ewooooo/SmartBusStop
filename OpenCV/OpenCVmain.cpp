#include <opencv2/opencv.hpp> // Include 'OpenCV' library.
////#include <opencv2/core.hpp>
////#include <opencv2/highgui/highgui.hpp>
//#include <algorithm>// min() max();
//#include <iostream>
//#include <cstdlib>
//using namespace cv;
//using namespace std;
//
//int main()
//{
//	Mat inputimage, grayscale, image3, drawing; // Make images.
//	double maxratio = 0.9, minratio = 0.25, alpha = 0, beta = 500;
//
//
//	cv::VideoCapture cap("C:\\\\\\\\Users\\\\\\\\이경신\\\\\\\\kyonggi.ac.kr\\\\\\\\이재빈 - 2020-1 프로젝트\\\\\\\\관련 자료\\\\\\\\버스영상\\\\\\\\1.mp4");
//	if (!cap.isOpened()) {
//		cerr << "에러 - 카메라를 열 수 없습니다.\\\\n";
//		return -1;
//	}
//	while (1)
//	{
//		// 카메라로부터 캡쳐한 영상을 frame에 저장합니다.
//		cap.read(inputimage);
//		if (inputimage.empty()) {
//			cerr << "빈 영상이 캡쳐되었습니다.\\\\n";
//			break;
//		}
//
//		Rect ROIRect(0, inputimage.rows/2, inputimage.cols, inputimage.rows/2); //x,y,w,h
//		Mat	image = inputimage(ROIRect);
//
//
//		//imshow("Original", image);
//		Mat imagedebuger = image.clone();
//
//		cvtColor(image, grayscale, COLOR_BGR2GRAY);  //  Convert to gray image.COLOR_BGR2GRAY
//		//imshow("Original->Gray", grayscale);
//
//
//		Size userSize = Size(3, 3);
//		Mat imgTopHat, imgBlackHat;
//		morphologyEx(grayscale, imgTopHat, MORPH_TOPHAT, getStructuringElement(MORPH_ELLIPSE, userSize));
//		morphologyEx(grayscale, imgBlackHat, MORPH_BLACKHAT, getStructuringElement(MORPH_ELLIPSE, userSize));
//
//		Mat imgGrayscalePlusTopHat;
//		add(grayscale, imgTopHat, imgGrayscalePlusTopHat);
//		Mat morphoImage;
//		subtract(imgGrayscalePlusTopHat, imgBlackHat, morphoImage);
//
//		Mat GaussImage;
//		GaussianBlur(morphoImage, GaussImage, Size(5, 5), 0);
//
//		Mat CannyImage;
//		Canny(GaussImage, CannyImage, 100, 300, 3);  //  Getting edges by Canny algorithm.
//		//imshow("Original->Gray->Canny", CannyImage);
//
//
//		//  Finding contours.
//		vector<vector<Point> > contours;  //  Vectors for 'findContours' function.
//		vector<Vec4i> hierarchy;
//		findContours(CannyImage, contours, hierarchy, RETR_LIST, CHAIN_APPROX_SIMPLE, Point());
//
//
//		vector<Rect> rect_list(contours.size());
//		//vector<momoRect> rect_list(contours.size());
//		int rectindex = 0;
//		RNG rng(12345);
//		Mat drawing = Mat::zeros(image.size(), CV_8UC3);
//		for (int idx = 0; idx < contours.size(); idx++) {
//
//			Scalar color = Scalar(rng.uniform(0, 255), rng.uniform(0, 255), rng.uniform(0, 255));
//			drawContours(drawing, contours, idx, color, 2, 8, hierarchy, 0, Point());
//
//			Rect rect = boundingRect(contours[idx]);
//
//			double ratio = (double)rect.width / rect.height;
//
//			if ((ratio >= minratio) && (ratio <= maxratio) && (rect.height >= alpha) && (rect.height <= beta)) {
//				Rect newrect(rect);
//				//momoRect newrect(rect);
//				rect_list[rectindex] = newrect;
//				rectindex++;
//				//rectangle(imagedebuger, Point(rect.br().x - rect.width, rect.br().y - rect.height), rect.br(), Scalar(0, 255, 0), 1);
//			}
//
//		}
//
//		rect_list.resize(rectindex);  //  Resize refinery rectangle array.
//
//		//imshow("drawContours", drawing);
//		imshow("imagedebuger", imagedebuger);
//
//
//
//		vector<Rect> opRectList;
//		for (int idx = 0; idx < rect_list.size(); idx++) {
//
//			for (int idx2 = 0; idx2 < rect_list.size(); idx2++) {
//				if (rect_list[idx] == rect_list[idx2] || rect_list[idx].x >= rect_list[idx2].x)
//					continue;
//
//				double gap = rect_list[idx].x + rect_list[idx].width - rect_list[idx2].x;
//
//				if (abs(gap) < max(rect_list[idx].height*0.2, (double)10)) {
//
//					//오버랩인지 판단.
//					if (gap > rect_list[idx].width*0.15) {
//						continue;
//					}
//
//					double diffup = abs(rect_list[idx].tl().y - rect_list[idx2].tl().y);
//					double diffdn = abs(rect_list[idx].br().y - rect_list[idx2].br().y);
//
//					if (diffup < max(rect_list[idx].height*0.3, (double)10) && diffdn < max(rect_list[idx].height*0.3, (double)10)) {
//						double Rgap = rect_list[idx].br().x - rect_list[idx2].br().x;
//						double Lgap = rect_list[idx2].x - rect_list[idx].x;
//						double Tgap = rect_list[idx2].y - rect_list[idx].y;
//						double Bgap = rect_list[idx].br().y - rect_list[idx2].br().y;
//
//						if (!(Rgap >= 0 && Lgap >= 0 && Tgap >= 0 && Bgap >= 0)) {
//
//							//rect_list[idx].addRect_list(&rect_list[idx2]);
//							Scalar color = Scalar(rng.uniform(0, 255), rng.uniform(0, 255), rng.uniform(0, 255));
//							line(imagedebuger, Point(rect_list[idx].x + rect_list[idx].width / 2, rect_list[idx].y + rect_list[idx].height / 2),
//								Point(rect_list[idx2].x + rect_list[idx2].width / 2, rect_list[idx2].y + rect_list[idx2].height / 2), color, 2);
//
//							if (opRectList.empty()) {
//								opRectList.push_back(rect_list[idx]);
//								opRectList.push_back(rect_list[idx2]);
//							}
//							else {
//								int test1 = 0, test2 = 0;
//								for (int i = 0; i < opRectList.size(); i++) {
//									if (test1 == 0 && opRectList[i] == rect_list[idx]) {
//										test1 = 1;
//									}
//									if (test2 == 0 && opRectList[i] == rect_list[idx2]) {
//										test2 = 1;
//									}
//									if (test1 == 1 && test2 == 1) {
//										break;
//									}
//								}
//								if (test1 == 0)
//									opRectList.push_back(rect_list[idx]);
//								if (test2 == 0)
//									opRectList.push_back(rect_list[idx2]);
//							}
//
//						}
//					}
//				}
//			}
//		}
//
//
//
//		for (int a = opRectList.size() - 1; a > 0; a--) {
//			for (int j = 0; j < a; j++) {
//				if (opRectList[j].tl().x > opRectList[j + 1].tl().x) {
//
//					Rect temp_rect = opRectList[j];
//
//					opRectList[j] = opRectList[j + 1];
//
//					opRectList[j + 1] = temp_rect;
//
//				}
//			}
//		}
//
//
//
//		vector<vector<Rect>> resultGroupList;
//		vector<Rect> fiartGroup;
//		if (opRectList.size() == 0)
//			continue;
//
//		fiartGroup.push_back(opRectList[0]);
//		resultGroupList.push_back(fiartGroup);
//
//
//		for (int idx = 0; idx < opRectList.size(); idx++) {
//			rectangle(imagedebuger, opRectList[idx].tl(), opRectList[idx].br(), Scalar(idx * 3, 0, idx * 5), 1);
//			int test = 0;
//			for (int i = 0; i < resultGroupList.size(); i++) {
//
//				Rect testRect = resultGroupList[i].back();
//
//				double gap = testRect.x + testRect.width - opRectList[idx].x;
//				if (abs(gap) < max(testRect.height*0.2, (double)10)) {
//
//					//오버랩인지 판단.
//					if (gap > testRect.width*0.15) {
//						continue;
//					}
//
//					double diffup = abs(testRect.tl().y - opRectList[idx].tl().y);
//					double diffdn = abs(testRect.br().y - opRectList[idx].br().y);
//
//					if (diffup < max(testRect.height*0.3, (double)10) && diffdn < max(testRect.height*0.3, (double)10)) {
//
//						if (!(testRect.br().x - opRectList[idx].br().x >= 0 && opRectList[idx].x - testRect.x >= 0 &&
//							opRectList[idx].y - testRect.y >= 0 && testRect.br().y - opRectList[idx].br().y >= 0)) {
//
//							resultGroupList[i].push_back(opRectList[idx]);
//
//							test = 1;
//						}
//					}
//				}
//			}
//			if (test == 0) {
//				vector<Rect> newGroup;
//				newGroup.push_back(opRectList[idx]);
//				resultGroupList.push_back(newGroup);
//			}
//		}
//		vector <Rect> GroupList;
//		for (int i = 0; i < resultGroupList.size(); i++) {
//			if (resultGroupList[i].size() < 4 || resultGroupList[i].size() > 12)
//				continue;
//			for (int j = 1; j < resultGroupList.size(); j++) {
//				if (resultGroupList[j].size() < 4 || resultGroupList[j].size() > 12)
//					continue;
//
//				Rect upBoundingRect(Point(resultGroupList[i][0].tl().x, resultGroupList[i][0].tl().y < resultGroupList[i].back().tl().y ? resultGroupList[i][0].tl().y : resultGroupList[i].back().tl().y),
//					Point(resultGroupList[i].back().br().x, resultGroupList[i][0].br().y > resultGroupList[i].back().br().y ? resultGroupList[i][0].br().y : resultGroupList[i].back().br().y));
//				Rect downBoundingRect(Point(resultGroupList[j][0].tl().x, resultGroupList[j][0].tl().y < resultGroupList[j].back().tl().y ? resultGroupList[j][0].tl().y : resultGroupList[j].back().tl().y),
//					Point(resultGroupList[j].back().br().x, resultGroupList[j][0].br().y > resultGroupList[j].back().br().y ? resultGroupList[j][0].br().y : resultGroupList[j].back().br().y));
//
//				if (upBoundingRect.y > downBoundingRect.y) { //i는 위여야 한다 아니면 끝
//					continue;
//				}
//				double gap2 = upBoundingRect.br().y - downBoundingRect.tl().y;
//				if (gap2 > upBoundingRect.height*0.15) {
//					continue;
//				}
//				double wg = (downBoundingRect.br().x - downBoundingRect.tl().x);
//				double xgap = (upBoundingRect.x - downBoundingRect.x);
//				int rectCount = resultGroupList[j].size();
//				if (xgap >= (wg / rectCount) && xgap <= 3 * (wg / rectCount)) { //논문(7)이고 
//					double ht = upBoundingRect.height;
//					double ygap = downBoundingRect.tl().y - upBoundingRect.br().y;
//					if (ygap <= ht * 0.2) {//논문(8)이면 두줄번호판
//
//						Rect boundingRect2(Point(upBoundingRect.x < downBoundingRect.x ? upBoundingRect.x : downBoundingRect.x,
//							upBoundingRect.y < downBoundingRect.y ? upBoundingRect.y : downBoundingRect.y),
//							Point(upBoundingRect.br().x < downBoundingRect.br().x ? downBoundingRect.br().x : upBoundingRect.br().x,
//								upBoundingRect.br().y < downBoundingRect.br().y ? downBoundingRect.br().y : upBoundingRect.br().y));
//
//						GroupList.push_back(boundingRect2);
//					}
//				}
//
//
//			}
//		}
//
//		for (int idx = 0; idx < GroupList.size(); idx++) {
//			rectangle(imagedebuger, GroupList[idx].tl(), GroupList[idx].br(), Scalar(0, 0, 255), 3);
//		}
//
//		imshow("imagedebuger", imagedebuger);
//
//
//		//		// ESC 키를 입력하면 루프가 종료됩니다.
//		if (cv::waitKey(25) >= 0)
//			break;
//	}
//	return 0;
//}


// 경신이 바보


using namespace std;


int main() {
	string a = "test";

	cout << a << endl;
}
