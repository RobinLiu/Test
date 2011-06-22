/*
 * TimerManager.h
 *
 *  Created on: 2011-6-22
 *      Author: Elric
 */

#ifndef TIMERMANAGER_H_
#define TIMERMANAGER_H_

namespace TimeLib {
/*
static HAUtils::Mutex managerMutex;

class TimerManager : public HAUtils::HAThread {
public:
    TimerManager();
    virtual ~TimerManager();
    static TimerManager* getInstance(unsigned int heapSize = 500,
            unsigned int allocationThreshold = 2,
            bool preallocate = true);

    int registerTimeout(int delay, TimeoutHandler* th, bool ignoreState = false);
    int registerTimeout(struct timeval& tv, TimeoutHandler* th, bool ignoreState = false);

    void cancelTimeout(int timerId, TimeValue* timevalue = 0);
    TimerValue trigeringTime(int timerId);

private:
    TimerManager(const TimerManager&);
    TimerManager& operator=(const TimerManager&);

    virtual void run (void);
    int handleTimeout (void);
    void waitForTimeoutEvents (void);
    int dispatchTimeoutEvents (void);
    void select (int width,
                fd_set* rfds,
                fd_set* wfds,
                fd_set* efds,
                const TimeValue* timeout);


    static TimerManager* instance;
    enum TimerState {TERMINATE = 0, ACTIVE, INACTIVE};
    TimerState state;
    TimerHeap* timerQueue;
};
*/
}

#endif /* TIMERMANAGER_H_ */
