#include <wiringPi.h>
#include <iostream>
#include <ctime>

int main (void)
{
  wiringPiSetup () ;
  pinMode (3, INPUT);
  pinMode (0, OUTPUT) ;
  pinMode (2, INPUT);
  pullUpDnControl (2, PUD_UP);
  pullUpDnControl (3, PUD_DOWN);
  clock_t count = 0;
  for (;;)
  {

    if (digitalRead(3) || digitalRead(2)) {
      digitalWrite (0, HIGH);
      if (count == 0) {
        count = clock();
      }
    } else {
      digitalWrite (0,  LOW) ;
      count = 0;
    }
    
    if (count != 0) {
      double delaytime =(double)(clock() - count); //1000000clock = 1s
      if(delaytime*1000000 > 2){
        std::cout << "set" << std::endl;
        count = 0;
      }
    }
  }
  return 0 ;
}