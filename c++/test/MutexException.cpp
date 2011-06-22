/*
 * MutexException.cpp
 *
 *  Created on: 2011-6-21
 *      Author: Elric
 */

#include "MutexException.h"

namespace HAUtils {

MutexException::MutexException(const char* errText) throw():m_reason(errText) {

}

MutexException::~MutexException() throw() {
}

const char* MutexException::what() const throw() {
	return m_reason.c_str();
}

}
