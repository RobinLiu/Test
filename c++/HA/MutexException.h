/*
 * MutexException.h
 *
 *  Created on: 2011-6-21
 *      Author: Elric
 */

#ifndef MUTEXEXCEPTION_H_
#define MUTEXEXCEPTION_H_

#include <exception>
#include <string>

namespace HAUtils {

class MutexException : public std::exception {
public:
	MutexException(const char* errText) throw() :m_reason(errText) {};
	MutexException(const MutexException& e): std::exception(), m_reason(e.m_reason){}
	MutexException& operator=(MutexException& e){
		m_reason = e.m_reason;
		return *this;
	}
	virtual ~MutexException() throw() {};
	virtual const char* what() const throw() {
	    return m_reason.c_str();
	}
private:
	std::string m_reason;
};

}

#endif /* MUTEXEXCEPTION_H_ */
