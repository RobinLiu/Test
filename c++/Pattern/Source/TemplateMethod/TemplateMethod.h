/********************************************************************
	created:	2006/07/20
	filename: 	TemplateMethod.h
	author:		�
                http://www.cppblog.com/converse/

	purpose:	TemplateMethodģʽ����ʾ����
*********************************************************************/

// �������,�����㷨������
class AbstractClass
{
public:
	AbstractClass(){}
	virtual ~AbstractClass(){}

	// ��������ж������㷨������
	void TemplateMethod();

protected:
	// ���麯��,��������ʵ��֮
	virtual void PrimitiveOperation1() = 0;
	virtual void PrimitiveOperation2() = 0;
};

// �̳���AbstractClass,ʵ���㷨
class ConcreateClass
	: public AbstractClass
{
public:
	ConcreateClass(){}
	virtual ~ConcreateClass(){}

protected:
	virtual void PrimitiveOperation1();
	virtual void PrimitiveOperation2();
};
