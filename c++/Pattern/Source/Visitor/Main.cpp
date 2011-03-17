/********************************************************************
	created:	2006/08/09
	filename: 	Main.cpp
	author:		�
                http://www.cppblog.com/converse/

	purpose:	Visitorģʽ�Ĳ��Դ���
*********************************************************************/

#include "Visitor.h"

int main()
{
	Visitor *pVisitorA = new ConcreateVisitorA();
	Element *pElement  = new ConcreateElementA();

	pElement->Accept(*pVisitorA);

	delete pElement;
	delete pVisitorA;

	return 0;
}
