//============================================================================
// Name        : test.cpp
// Author      :
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include "MutexHolder.h"
#include <iostream>

HAUtils::Mutex theMutex;
using namespace std;
int main(void) {
	{HAUtils::MutexHolder mh(theMutex);}
}
