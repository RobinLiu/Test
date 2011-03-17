/********************************************************************
	created:	2006/07/21
	filename: 	Main.cpp
	author:		�
                http://www.cppblog.com/converse/

	purpose:	Observerģʽ�Ĳ��Դ���
*********************************************************************/

#include "Observer.h"
#include <iostream>

int main()
{
	Observer *p1 = new ConcreateObserver;
	Observer *p2 = new ConcreateObserver;

	Subject* p = new ConcreateSubject;
	p->Attach(p1);
	p->Attach(p2);
	p->SetState(4);
	p->Notify();

	p->Detach(p1);
	p->SetState(10);
	p->Notify();

	delete p;

	system("pause");

	return 0;
}