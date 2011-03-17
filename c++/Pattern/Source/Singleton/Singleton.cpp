/********************************************************************
	created:	2006/07/20
	filename: 	Singleton.cpp
	author:		�
                http://www.cppblog.com/converse/

	purpose:	Singletonģʽ����ʾ����
*********************************************************************/

#include "Singleton.h"
#include <iostream>

// ��ľ�̬��Ա����Ҫ����������ж���
Singleton* Singleton::m_pStatic = NULL;

Singleton* Singleton::GetInstancePtr()
{
	if (NULL == m_pStatic)
	{
		m_pStatic = new Singleton();
	}

	return m_pStatic;
}

Singleton Singleton::GetInstance()
{
	return *GetInstancePtr();
}

void Singleton::Test()
{
	std::cout << "Test!\n";
}