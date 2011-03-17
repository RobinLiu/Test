/********************************************************************
	created:	2006/07/20
	filename: 	Adapter.h
	author:		�
                http://www.cppblog.com/converse/

	purpose:	Adapterģʽ����ʾ����
*********************************************************************/

#ifndef ADAPTER_H
#define ADAPTER_H

// ��Ҫ��Adapt����
class Target
{
public:
	Target(){}
	virtual ~Target() {}

	virtual void Request() = 0;
};

// �뱻Adapt�����ṩ�����ݽӿڵ���
class Adaptee
{
public:
	Adaptee(){}
	~Adaptee(){}
	void SpecialRequest();
};

// ����Adapt����,���þۺ�ԭ�нӿ���ķ�ʽ
class Adapter
	: public Target
{
public:
	Adapter(Adaptee* pAdaptee);
	virtual ~Adapter();

	virtual void Request();

private:
	Adaptee* m_pAdptee;
};

#endif