/********************************************************************
	created:	2006/07/20
	filename: 	Main.cpp
	author:		�
                http://www.cppblog.com/converse/

	purpose:	ChainOfResponsibilityģʽ�Ĳ��Դ���
*********************************************************************/

#include "ChainOfResponsibility.h"
#include <stdlib.h>

int main()
{
	Handler *p1 = new ConcreateHandler1();
	Handler *p2 = new ConcreateHandler2(p1);

	p2->HandleRequset();

	delete p2;

	system("pause");

	return 0;
}