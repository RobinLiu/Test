/********************************************************************
	created:	2006/07/20
	filename: 	Main.cpp
	author:		�
                http://www.cppblog.com/converse/

	purpose:	TemplateMethodģʽ�Ĳ��Դ���
*********************************************************************/

#include "TemplateMethod.h"
#include <stdlib.h>

int main()
{
	AbstractClass* pConcreateClass = new ConcreateClass;
	pConcreateClass->TemplateMethod();

	delete pConcreateClass;

	system("pause");

	return 0;
}
