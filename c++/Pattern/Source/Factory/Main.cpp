/********************************************************************
	created:	2006/06/30
	filename: 	Main.cpp
	author:		�
                http://www.cppblog.com/converse/

	purpose:	����Factoryģʽ�Ĵ���
*********************************************************************/

#include "Factory.h"
#include <stdlib.h>

int main(int argc,char* argv[])
{
	Creator *p = new ConcreateCreator();
	p->AnOperation();

	delete p;

	system("pause");

	return 0;
}


