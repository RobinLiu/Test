/********************************************************************
	created:	2006/07/20
	filename: 	Main.cpp
	author:		�
                http://www.cppblog.com/converse/

	purpose:	Decoratorģʽ�Ĳ��Դ���
*********************************************************************/

#include "Decorator.h"
#include <stdlib.h>

int main()
{
	// ��ʼ��һ��Component����
	Component* pComponent = new ConcreateComponent();
	// �������Component����ȥ��ʼ��һ��Decorator����,
	// �����Ϳ���Ϊ���Component����̬���ְ��
	Decorator* pDecorator = new ConcreateDecorator(pComponent);

	pDecorator->Operation();

	delete pDecorator;

	system("pause");

	return 0;
}
