/********************************************************************
	created:	2006/07/20
	filename: 	Main.cpp
	author:		�
                http://www.cppblog.com/converse/

	purpose:	Adapterģʽ�Ĳ��Դ���
*********************************************************************/

#include "Adapter.h"
#include <stdlib.h>

int main()
{
	Adaptee *pAdaptee = new Adaptee;
	Target *pTarget = new Adapter(pAdaptee);
	pTarget->Request();

	delete pTarget;

	system("pause");

	return 0;
}