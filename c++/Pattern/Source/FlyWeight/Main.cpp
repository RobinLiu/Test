/********************************************************************
	created:	2006/07/26
	filename: 	Main.cpp
	author:		�
                http://www.cppblog.com/converse/

	purpose:	FlyWeightģʽ�Ĳ��Դ���
*********************************************************************/

#include "FlyWeight.h"

int main()
{
	FlyweightFactory flyweightfactory;
	flyweightfactory.GetFlyweight("hello");
	flyweightfactory.GetFlyweight("world");
	flyweightfactory.GetFlyweight("hello");

	system("pause");
	return 0;
}
