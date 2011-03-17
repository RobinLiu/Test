/********************************************************************
	created:	2006/07/20
	filename: 	Observer.h
	author:		�
                http://www.cppblog.com/converse/

	purpose:	Observerģʽ����ʾ����
*********************************************************************/

#ifndef OBSERVER_H
#define OBSERVER_H

#include <list>

typedef int STATE;

class Observer;

// Subject�������,ֻ��Ҫ֪��Observer����������Ϳ�����
class Subject
{
public:
	Subject() : m_nSubjectState(-1){}
	virtual ~Subject();

	void Notify();							// ֪ͨ����ı�״̬
	void Attach(Observer *pObserver);		// ��������
	void Detach(Observer *pObserver);		// ɾ������

	// �麯��,�ṩĬ�ϵ�ʵ��,����������Լ�ʵ�������ǻ����ʵ��
	virtual void	SetState(STATE nState);	// ����״̬
	virtual STATE	GetState();		// �õ�״̬

protected:
	STATE m_nSubjectState;					// ģ�Ᵽ��Subject״̬�ı���
	std::list<Observer*>	m_ListObserver;	// ����Observerָ�������
};

// Observer�������
class Observer
{
public:
	Observer() : m_nObserverState(-1){}
	virtual ~Observer(){}

	// ���麯��,��������������в�ͬ��ʵ��
	// ֪ͨObserver״̬�����˱仯
	virtual void Update(Subject* pSubject) = 0;

protected:
	STATE m_nObserverState;					// ģ�Ᵽ��Observer״̬�ı���
};

// ConcreateSubject��,������Subject��
class ConcreateSubject
	: public Subject
{
public:
	ConcreateSubject() : Subject(){}
	virtual ~ConcreateSubject(){}

	// �������Լ�ʵ�������ǻ����ʵ��
	virtual void	SetState(STATE nState);	// ����״̬
	virtual STATE	GetState();		// �õ�״̬

};

// ConcreateObserver��������Observer
class ConcreateObserver
	: public Observer
{
public:
	ConcreateObserver() : Observer(){}
	virtual ~ConcreateObserver(){}

	// �麯��,ʵ�ֻ����ṩ�Ľӿ�
	virtual void Update(Subject* pSubject);
};

#endif
