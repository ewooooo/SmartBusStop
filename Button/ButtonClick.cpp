#include <wiringPi.h>
#include <iostream>
#include <ctime>

using namespace std;

#define LONGCLICKTIME 1
#define DOUBLECLICKTIME 0.5
#define ONECLICKTIME 0.05
int main (void)
{

  wiringPiSetup () ;
  pinMode (3, INPUT);
  pinMode (0, OUTPUT) ;
  pinMode (2, INPUT);
  pullUpDnControl (2, PUD_UP);
  pullUpDnControl (3, PUD_DOWN);
  clock_t count = 0, doubleClickCount = 0;
  bool doubleClickON = false;
  for (;;)
  {
    if (digitalRead(3) || digitalRead(2)) {
      digitalWrite (0, LOW);
      if (count == 0) {
        count = clock();
        if (doubleClickCount) {
          double delaytime = (double)(clock() - doubleClickCount) / 1000000;
          if (delaytime <= DOUBLECLICKTIME) {
            doubleClickON = true;
          }
        }
      }

    } else {
      digitalWrite (0,  HIGH) ;
      if (count) {
        double delaytime = (double)(clock() - count)/ 1000000; //1000000clock = 1s
        if (delaytime >= LONGCLICKTIME) {
          cout << delaytime<<endl;
          cout << "longclick" << endl;
          if (doubleClickON) {
            doubleClickCount = 0;
            doubleClickON = false;
          }
        } else if(delaytime > ONECLICKTIME ){
          if (doubleClickON) {
            cout << "doubleclick" << endl;
            doubleClickON = false;
            doubleClickCount = 0;
          } else {
            doubleClickCount = clock();
          }
        }
        count = 0;
      } else {
        if (doubleClickCount) {
          double delaytime = (double)(clock() - doubleClickCount)/ 1000000 ;
          if (delaytime > DOUBLECLICKTIME) {
            cout << "oneclick" << endl;
            doubleClickCount = 0;
            doubleClickON = false;
          }
        }
      }
    }


  }
  return 0 ;
}