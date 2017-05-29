#include "Timer.h"

Timer::Timer() {}
Timer::Timer(unsigned long waitTime) {this->setWait(waitTime);}
Timer::Timer(unsigned long waitTime, bool timerStatus) {this->setWait(waitTime); this->setStatus(timerStatus);}

void Timer::setWait(unsigned long waitTime) {
  this->waitTime = waitTime;
}

void Timer::setStatus(bool timerStatus) {
  this->lastTime = millis();
  this->timerEnabled = timerStatus;
}

bool Timer::isElapsed() {
  unsigned long nowTime = millis();

  if(timerEnabled && nowTime - this->lastTime >= this->waitTime) {
    this->lastTime = nowTime;
    return true;
  } else {return false;}
}

