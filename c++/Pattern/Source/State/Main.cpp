/********************************************************************
	created:	2006/08/05
	filename: 	Main.cpp
	author:		�
                http://www.cppblog.com/converse/

	purpose:	Stateģʽ�Ĳ��Դ���
*********************************************************************/

#include "State.h"

int main()
{
	State *pState = new ConcreateStateA();
	Context *pContext = new Context(pState);
	pContext->Request();
	pContext->Request();
	pContext->Request();

	delete pContext;

	return 0;
}