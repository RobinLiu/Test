/********************************************************************
    created:    2008/08/01
    filename:     threadmutex.h
    author:        Lichuang
                
    purpose:    �߳�����, ���Ƿ����__USE_THREAD__�������Ƿ�ʹ�ø���
*********************************************************************/

#ifndef __THREAD_MUTEX_H__
#define __THREAD_MUTEX_H__

#ifdef __USE_THREAD__
    #include <pthread.h>
    
    #define THREAD_LOCK(tThreadMutex)     tThreadMutex.Lock()
    #define THREAD_UNLOCK(tThreadMutex)   tThreadMutex.UnLock()
#else
    #define THREAD_LOCK(tThreadMutex)     
    #define THREAD_UNLOCK(tThreadMutex)   
#endif

class CThreadMutex
{
public:
    CThreadMutex();
    ~CThreadMutex();
    int Lock();
    int UnLock();

private:
#ifdef __USE_THREAD__
    pthread_mutex_t  m_tThreadMutex;
#endif
};

#endif /* __THREAD_MUTEX_H__ */