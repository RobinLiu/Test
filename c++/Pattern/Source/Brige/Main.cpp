/********************************************************************
	created:	2006/07/20
	filename: 	Main.cpp
	author:		�
                http://www.cppblog.com/converse/

	purpose:	Bridgeģʽ�Ĳ��Դ���
*********************************************************************/

#include "Brige.h"
#include <stdlib.h>
#include <stdio.h>
int main()
{
	ConcreateImplementorA *pImplA = new ConcreateImplementorA();
	Abstraction *pAbstraction1 = new Abstraction(pImplA);
	pAbstraction1->Operation();

	ConcreateImplementorB *pImplB = new ConcreateImplementorB();
	Abstraction *pAbstraction2 = new Abstraction(pImplB);
	pAbstraction2->Operation();

	delete pAbstraction1;
	delete pAbstraction2;

	system("pause");

	return 0;
}