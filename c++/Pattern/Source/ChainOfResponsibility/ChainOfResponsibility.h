/********************************************************************
	created:	2006/07/20
	filename: 	ChainOfResponsibility.h
	author:		�
                http://www.cppblog.com/converse/

	purpose:	ChainOfResponsibilityģʽ����ʾ����
*********************************************************************/

#ifndef CHAINOFRESPONSIBILITY_H
#define CHAINOFRESPONSIBILITY_H

#include <stdio.h>

// �������,����һ����������Ľӿ�
class Handler
{
public:
	Handler(Handler *pSuccessor = NULL);
	virtual ~Handler();

	// ���麯��,��������ʵ��
	virtual void HandleRequset() = 0;

protected:
	Handler* m_pSuccessor;
};

class ConcreateHandler1
	: public Handler
{
public:
	ConcreateHandler1(Handler *pSuccessor = NULL) : Handler(pSuccessor){}
	virtual ~ConcreateHandler1(){}

	virtual void HandleRequset();
};

class ConcreateHandler2
	: public Handler
{
public:
	ConcreateHandler2(Handler *pSuccessor = NULL) : Handler(pSuccessor){}
	virtual ~ConcreateHandler2(){}

	virtual void HandleRequset();
};

#endif
