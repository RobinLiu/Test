/********************************************************************
	created:	2006/07/26
	filename: 	Proxy.h
	author:		�
                http://www.cppblog.com/converse/

	purpose:	Proxyģʽ����ʾ����
*********************************************************************/

#ifndef PROXY_H
#define PROXY_H

// ������Proxy��RealSubject�Ĺ��нӿ�,
// �����Ϳ������κ���Ҫʹ�õ�RealSubject�ĵط���ʹ��Proxy.
class Subject
{
public:
	Subject(){}
	virtual ~Subject(){}

	virtual void Request() = 0;
};

// ����ʹ�õ�ʵ��
class RealSubject
	: public Subject
{
public:
	RealSubject();
	virtual ~RealSubject(){}

	virtual void Request();
};

// ������,����һ��ָ��RealSubject�����ָ��
class Proxy
	: public Subject
{
public:
	Proxy();
	virtual ~Proxy();

	virtual void Request();

private:
	RealSubject* m_pRealSubject;
};
#endif
