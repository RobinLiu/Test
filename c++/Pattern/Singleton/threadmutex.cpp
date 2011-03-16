/********************************************************************
    created:    2008/08/01
    filename:     threadmutex.h
    author:        Lichuang
                
    purpose:    �߳�����, ���Ƿ����__USE_THREAD__�������Ƿ�ʹ�ø�
                �߳�����
*********************************************************************/

#include "threadmutex.h"

#ifdef __USE_THREAD__

CThreadMutex::CThreadMutex()
{        
    ::pthread_mutex_init(&m_tThreadMutex, NULL);
}

CThreadMutex::~CThreadMutex()
{  
    ::pthread_mutex_destroy(&m_tThreadMutex);
}

int CThreadMutex::Lock()
{
    return ::pthread_mutex_lock(&m_tThreadMutex);
}

int CThreadMutex::UnLock()
{
    return ::pthread_mutex_unlock(&m_tThreadMutex);
}

#else

CThreadMutex::CThreadMutex()
{        
}

CThreadMutex::~CThreadMutex()
{  
}

int CThreadMutex::Lock()
{
    return 0;
}

int CThreadMutex::UnLock()
{
    return 0;
}

#endif