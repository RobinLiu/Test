/********************************************************************
	created:	2006/07/26
	filename: 	Main.cpp
	author:		�
                http://www.cppblog.com/converse/

	purpose:	Proxyģʽ�Ĳ��Դ���
*********************************************************************/

#include "Proxy.h"
#include <stdlib.h>

int main()
{
	Subject* pProxy = new Proxy();
	pProxy->Request();

	delete pProxy;

	system("pause");

	return 0;
}
