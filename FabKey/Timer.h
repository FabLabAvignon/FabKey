#pragma once

#define TIMER_DEFAULT 500

/* Include Arduino core libs */
#include <Arduino.h>

class Timer {
  public:
    Timer();
    Timer(unsigned long);
    Timer(unsigned long, bool);

    void setStatus(bool);
    
    void setWait(unsigned long);
    bool isElapsed();
    
  private:
    unsigned long lastTime = 0;
    unsigned long waitTime = TIMER_DEFAULT;

    bool timerEnabled = true;
};

