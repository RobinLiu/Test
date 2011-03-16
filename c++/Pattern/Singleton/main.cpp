#include <iostream>
#include "singleton.h"

using namespace std;

class CTestSingleton
    : public CSingleton<CTestSingleton>
{
public:

    void Set(int a)
    {
        m_a = a;
    }
    int Get()
    {
        return m_a;
    }

private:
    CTestSingleton()
        : m_a(0)
    {

    }
    DECLARE_SINGLETON_CLASS(CTestSingleton)
private:
    int m_a;
};

int main()
{
    if (NULL == CTestSingleton::GetInstance())
    {
        cout << "GetInstance() error!" << endl;
    }

    cout << "before set: " << CTestSingleton::GetInstance()->Get() << endl;

    CTestSingleton::GetInstance()->Set(100);

    cout << "after set: " << CTestSingleton::GetInstance()->Get() << endl;

    return 0;
}