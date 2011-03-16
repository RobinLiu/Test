/********************************************************************
    created:    2008/08/01
    filename:     threadmutex.h
    author:        Lichuang
                
    purpose:    线程锁类, 由是否定义宏__USE_THREAD__来决定是否使用该类
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