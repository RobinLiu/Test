// test 1Dlg.h : header file
//

#pragma once


// Ctest1Dlg dialog
using namespace std;

class Ctest1Dlg : public CDialog
{
// Construction
public:
	Ctest1Dlg(CWnd* pParent = NULL);	// standard constructor
    //static Ctest1Dlg* Instance();
// Dialog Data
	enum { IDD = IDD_TEST1_DIALOG };
    virtual BOOL Ctest1Dlg::PreTranslateMessage(MSG* pMsg);
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV support

    //static Ctest1Dlg* __instance;
// Implementation
protected:
	HICON m_hIcon;

	// Generated message map functions
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	DECLARE_MESSAGE_MAP()
public:
	afx_msg void OnBnClickedButton1();
	CString m_infileStr;
	afx_msg void OnBnClickedButton2();
	afx_msg void OnBnClickedOk();
	afx_msg void OnBnClickedButton3();
    afx_msg void OnBnClickedButton4();
    afx_msg void OnBnClickedButton5();
    afx_msg void OnBnClickedButton6();
    afx_msg void OnBnClickedButton7();
    afx_msg void OnBnClickedButton8();
};
