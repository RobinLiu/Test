/********************************************************************
	created:	2006/08/06
	filename: 	Main.cpp
	author:		�
                http://www.cppblog.com/converse/

	purpose:	Strategyģʽ�Ĳ��Դ���
*********************************************************************/

#include "Strategy.h"

int main()
{
	Strategy* pStrategy = new ConcreateStrategyA();
	Context*  pContext  = new Context(pStrategy);

	pContext->ContextInterface();

	delete pContext;

	return 0;
}
