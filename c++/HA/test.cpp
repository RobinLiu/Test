//============================================================================
// Name        : test.cpp
// Author      :
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include "MutexHolder.h"
#include <iostream>
#include <unistd.h>
#include "glog/logging.h"
#include "HAThread.h"
#include "TimerManager.h"
#include "TimeoutHandler.h"

class testThread : public HAUtils::HAThread {
public:
    void run(){
        while(1) {
            LOG(INFO)<<"I'm thread"<<pthread_self();
            sleep(1);
        }
    }
};

class tmh : public TimeLib::TimeoutHandler {
    void handleTimeout(int tid) {
        LOG(INFO)<<"handleTimeout in children class";
    }
};

HAUtils::Mutex theMutex;
using namespace std;
int main(int argc, char* argv[]) {
    google::InitGoogleLogging(argv[0]);
    TimeLib::TimerManager* timerMgr = TimeLib::TimerManager::getInstance();
    tmh tm;
    {HAUtils::MutexHolder mh(theMutex);}
    testThread* a = new testThread();
    testThread* b = new testThread();
    a->start();
    b->start();
	
	while(1) {
	sleep(1);
	}
    return 0;
}
