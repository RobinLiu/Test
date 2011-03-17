/********************************************************************
	created:	2006/07/19
	filename: 	Main.cpp
	author:		�
                http://www.cppblog.com/converse/

	purpose:	AbstractFactory�Ĳ��Դ���
*********************************************************************/

#include "AbstractFactory.h"
#include <stdlib.h>

int main()
{
	// ������ƷA�ĵ�һ��ʵ��
	ConcreateFactory1 *pFactory1 = new ConcreateFactory1;
	AbstractProductA *pProductA = pFactory1->CreateProductA();

	// ������ƷB�ĵڶ���ʵ��
	ConcreateFactory2 *pFactory2 = new ConcreateFactory2;
	AbstractProductB *pProductB = pFactory2->CreateProductB();

	delete pFactory1;
	delete pProductA;
	delete pFactory2;
	delete pProductB;

	system("pause");

	return 0;
}