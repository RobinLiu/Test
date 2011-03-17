/********************************************************************
	created:	2006/08/09
	filename: 	Main.cpp
	author:		�
                http://www.cppblog.com/converse/

	purpose:	Mementoģʽ�Ĳ��Դ���
*********************************************************************/

#include "Memento.h"

int main()
{
	// ����һ��ԭ����
	Originator* pOriginator = new Originator("old state");
	pOriginator->PrintState();

	// ����һ������¼������ԭ������״̬
	Memento *pMemento = pOriginator->CreateMemento();
	
	// ����ԭ������״̬
	pOriginator->SetState("new state");
	pOriginator->PrintState();

	// ͨ������¼��ԭ������״̬��ԭ��֮ǰ��״̬
	pOriginator->RestoreState(pMemento);
	pOriginator->PrintState();

	delete pOriginator;
	delete pMemento;

	return 0;
}
