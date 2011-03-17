/********************************************************************
	created:	2006/07/20
	filename: 	Prototype.h
	author:		�
                http://www.cppblog.com/converse/

	purpose:	Prototypeģʽ����ʾ����
*********************************************************************/

#ifndef PROTOTYPE_H
#define PROTOTYPE_H

// �������,����ԭ�͵Ļ���,�ṩClone�ӿں���
class Prototype
{
public:
	Prototype(){}
	virtual ~Prototype(){}

	virtual Prototype* Clone() = 0;
};

// ������Prototype,ʵ��Clone����
class ConcreatePrototype1
	: public Prototype
{
public:
	ConcreatePrototype1();
	ConcreatePrototype1(const ConcreatePrototype1&);
	virtual ~ConcreatePrototype1();

	virtual Prototype* Clone();
};

// ������Prototype,ʵ��Clone����
class ConcreatePrototype2
	: public Prototype
{
public:
	ConcreatePrototype2();
	ConcreatePrototype2(const ConcreatePrototype2&);
	virtual ~ConcreatePrototype2();

	virtual Prototype* Clone();
};

#endif