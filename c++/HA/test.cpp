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

HAUtils::Mutex theMutex;
using namespace std;
int main(int argc, char* argv[]) {
    google::InitGoogleLogging(argv[0]);
    {HAUtils::MutexHolder mh(theMutex);}
    return 0;
}
