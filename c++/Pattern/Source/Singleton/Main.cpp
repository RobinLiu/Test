/********************************************************************
	created:	2006/07/20
	filename: 	Main.cpp
	author:		�
                http://www.cppblog.com/converse/

	purpose:	Singletonģʽ�Ĳ��Դ���
*********************************************************************/

#include "Singleton.h"
#include <stdlib.h>

int main()
{
	// ���ó�ʼ�������Ϳ��Է�����
	Singleton::GetInstancePtr()->Test();
	Singleton::GetInstance().Test();

	system("pause");

	return 0;
}