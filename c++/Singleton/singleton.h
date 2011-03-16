/********************************************************************
    created:    2008/08/01
    filename:     singleton.h
    author:        Lichuang
                
    purpose:    实现单件模式的虚拟基类, 其它需要实现为singleton的类可以
                继承自这个类
                支持多线程, 采用智能指针实现自动回收内存
*********************************************************************/

#ifndef __SINGLETON_H__
#define __SINGLETON_H__

#include <memory>
#include "threadmutex.h"

using namespace std;

#define DECLARE_SINGLETON_CLASS( type ) \
        friend class auto_ptr< type >;  \
        friend class CSingleton< type >;

template <class T>
class CSingleton
{
public:
    static T* GetInstance();

protected:
    CSingleton()
    {
    }
    virtual ~CSingleton()
    {
    }

protected:    
    friend class auto_ptr<CSingleton>;

    static auto_ptr<T> m_pInstance;
    static CThreadMutex m_tThreadMutex;
};

template <class T>
auto_ptr<T> CSingleton<T>::m_pInstance;

template <class T>
CThreadMutex CSingleton<T>::m_tThreadMutex;

template <class T>
inline T* CSingleton<T>::GetInstance()
{
    if (0 == m_pInstance.get())
    {
        THREAD_LOCK(m_tThreadMutex);
        if (0 == m_pInstance.get())
        {
            m_pInstance.reset(::new T);
        }
        THREAD_UNLOCK(m_tThreadMutex);
    }

    return m_pInstance.get();
}

#endif /* __SINGLETON_H__ */