/********************************************************************
	created:	2006/07/20
	filename: 	Composite.h
	author:		�
                http://www.cppblog.com/converse/

	purpose:	Compositeģʽ����ʾ����
*********************************************************************/

#ifndef COMPOSITE_H
#define COMPOSITE_H

#include <list>

// ����еĳ������
class Component
{
public:
	Component(){}
	virtual ~Component(){}

	// ���麯��,ֻ�ṩ�ӿ�,û��Ĭ�ϵ�ʵ��
	virtual void Operation() = 0;

	// �麯��,�ṩ�ӿ�,��Ĭ�ϵ�ʵ�־���ʲô������
	virtual void Add(Component* pChild);
	virtual void Remove(Component* pChild);
	virtual Component* GetChild(int nIndex);
};

// ������Component,�����е�Ҷ������Ļ���
class Leaf
	: public Component
{
public:
	Leaf(){}
	virtual ~Leaf(){}

	virtual void Operation();
};

// ������Component,�����еĺ����Ӽ�������Ļ���
class Composite
	: public Component
{
public:
	Composite(){}
	virtual ~Composite();

	virtual void Operation();

	virtual void Add(Component* pChild);
	virtual void Remove(Component* pChild);
	virtual Component* GetChild(int nIndex);

private:
	// ����list����ȥ���������
	std::list<Component*>	m_ListOfComponent;
};

#endif