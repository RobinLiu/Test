/*
 * TimerManager.cpp
 *
 *  Created on: 2011-6-22
 *      Author: Elric
 */

#include "TimerManager.h"

namespace TimeLib {
/*
TimerManager* ManagerInstance = 0;

TimerManager* TimerManager::getInstance(unsigned int heapSize,
                                        unsigned int allocationThreshold,
                                        bool preallocate) {

    if (((int) allocationThreshold <= 1) ||
            ((int) (heapSize - allocationThreshold) <= 1)) {
        throw InitializationFailure("invalid parameters", __FILE__, __LINE__);
    }

    if (ManagerInstance == NULL) {
        HAUtils::MutexHolder mh(::managerMutex);
        if (ManagerInstance == NULL) {
            ManagerInstance = new TimerManager(heapSize, allocationThreshold,
                    preallocate);
            ManagerInstance->start();
        }

        ManagerInstance->waitUntilActive();
    }

    //ISSU change start
    // ManagerInstance->waitUntilActive();
    //ISSU change end
    return ManagerInstance;
}
TimerManager::TimerManager(unsigned int heapSize,
                           unsigned int allocationThreshold,
                           bool preallocate):
                           HAUtils::HAThread(true), state(INACTIVE) {
    try {
        // Create a timer heap object.
        timerQueue = new TimerHeap(heapSize, allocationThreshold, preallocate);

        // Create a pair of read/write fds.
        this->pipe();
    } catch (SystemException&) {
        std::cout << "SystemException" << std::endl;
        delete timerQueue;
        throw;
    }
}

TimerManager::~TimerManager() {
    // Terminate timer thread if it is still active.
    if (state == ACTIVE) {
        state = TERMINATE;
        fdWrite();
    }

    // Delete the timer heap which was created in the constructor.
    delete timerQueue;

    // Close the fd pair.
    ::close(fd[0]);
    ::close(fd[1]);
}
*/
}
