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
  int count = 0;
  for (;;)
  {

    if (digitalRead(3) || digitalRead(2)) {
      digitalWrite (0, HIGH);
      if (count == 0) {
        count = time(0) % 60;
      }
    } else {
      digitalWrite (0,  LOW) ;
      count = 0;
    }
    
    if (count != 0) {
      int delaytime = time(0) % 60 - count;
      if (delaytime < 0) {
        count = count + 60;
      }
      if(delaytime > 3){
        std::cout << "set" << std::endl;
        count = 0;
      }
      

    }
  }
  return 0 ;
}