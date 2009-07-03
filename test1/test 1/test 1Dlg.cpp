// test 1Dlg.cpp : implementation file
//

#include "stdafx.h"
#include "test 1.h"
#include "test 1Dlg.h"
#include "VocabularyBase.h"


#ifdef _DEBUG
#define new DEBUG_NEW
#endif


VocabularyBase vbase;
int word_index = 0;
// CAboutDlg dialog used for App About

class CAboutDlg : public CDialog
{
public:
	CAboutDlg();

// Dialog Data
	enum { IDD = IDD_ABOUTBOX };

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

// Implementation
protected:
	DECLARE_MESSAGE_MAP()
};

CAboutDlg::CAboutDlg() : CDialog(CAboutDlg::IDD)
{
}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialog)
END_MESSAGE_MAP()


// Ctest1Dlg dialog

/*
BOOL Ctest1Dlg::PreTranslateMessage(MSG* pMsg)
{
	if(pMsg->message == WM_KEDOWN)
	{
		switch(pMsg->wParam)
			case 48://"0"
				AfxMessageBox("0");
				return TRUE;
	}
	return CDialog::PreTranslateMessage(pMsg);
}
*/

Ctest1Dlg::Ctest1Dlg(CWnd* pParent /*=NULL*/)
	: CDialog(Ctest1Dlg::IDD, pParent)
	, m_infileStr(_T(""))
{
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void Ctest1Dlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	DDX_Text(pDX, IDC_EDIT1, m_infileStr);
}

BEGIN_MESSAGE_MAP(Ctest1Dlg, CDialog)
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	//}}AFX_MSG_MAP
	ON_BN_CLICKED(IDC_BUTTON1, &Ctest1Dlg::OnBnClickedButton1)
	ON_BN_CLICKED(IDC_BUTTON2, &Ctest1Dlg::OnBnClickedButton2)
	ON_BN_CLICKED(IDOK, &Ctest1Dlg::OnBnClickedOk)
	ON_BN_CLICKED(IDC_BUTTON3, &Ctest1Dlg::OnBnClickedButton3)
	ON_COMMAND_RANGE(IDC_STATIC,IDC_STATIC,OnNumberKey)
	ON_COMMAND_RANGE(IDC_STATIC,IDC_STATIC,OnOperationKey)
END_MESSAGE_MAP()


// Ctest1Dlg message handlers
void Ctest1Dlg::OnNumberKey(UINT nID)
{
	//switch(nID)
	AfxMessageBox("0");

}

void Ctest1Dlg::OnOperationKey(UINT nID)
{
	//switch(nID)
	AfxMessageBox("1");

}

BOOL Ctest1Dlg::OnInitDialog()
{
	CDialog::OnInitDialog();

	// Add "About..." menu item to system menu.

	// IDM_ABOUTBOX must be in the system command range.
	ASSERT((IDM_ABOUTBOX & 0xFFF0) == IDM_ABOUTBOX);
	ASSERT(IDM_ABOUTBOX < 0xF000);

	CMenu* pSysMenu = GetSystemMenu(FALSE);
	if (pSysMenu != NULL)
	{
		CString strAboutMenu;
		strAboutMenu.LoadString(IDS_ABOUTBOX);
		if (!strAboutMenu.IsEmpty())
		{
			pSysMenu->AppendMenu(MF_SEPARATOR);
			pSysMenu->AppendMenu(MF_STRING, IDM_ABOUTBOX, strAboutMenu);
		}
	}

	// Set the icon for this dialog.  The framework does this automatically
	//  when the application's main window is not a dialog
	SetIcon(m_hIcon, TRUE);			// Set big icon
	SetIcon(m_hIcon, FALSE);		// Set small icon

	// TODO: Add extra initialization here
	if(vbase.init_base())
	{
		MessageBox("Init history file error!");
		return FALSE;
	}
	return TRUE;  // return TRUE  unless you set the focus to a control
}

void Ctest1Dlg::OnSysCommand(UINT nID, LPARAM lParam)
{
	if ((nID & 0xFFF0) == IDM_ABOUTBOX)
	{
		CAboutDlg dlgAbout;
		dlgAbout.DoModal();
	}
	else
	{
		CDialog::OnSysCommand(nID, lParam);
	}
}

// If you add a minimize button to your dialog, you will need the code below
//  to draw the icon.  For MFC applications using the document/view model,
//  this is automatically done for you by the framework.

void Ctest1Dlg::OnPaint()
{
	if (IsIconic())
	{
		CPaintDC dc(this); // device context for painting

		SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);

		// Center icon in client rectangle
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		// Draw the icon
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialog::OnPaint();
	}
}

// The system calls this function to obtain the cursor to display while the user drags
//  the minimized window.
HCURSOR Ctest1Dlg::OnQueryDragIcon()
{
	return static_cast<HCURSOR>(m_hIcon);
}


void Ctest1Dlg::OnBnClickedButton1()
{
	// TODO: 在此添加控件通知处理程序代码
	//IDC_STATIC
	int num = vbase.get_number_of_new();
	if( word_index < num )
	{
		SetDlgItemText(IDC_STATIC,vbase.get_new_word_at(word_index++).word.c_str());
	}
	else
	{
		MessageBox("All word has been displayed!");
	}
}

void Ctest1Dlg::OnBnClickedButton2()
{
	// TODO: 在此添加控件通知处理程序代码
	CFileDialog Open(true/**/, "txt"/*默认后缀名*/, ""/*默认文件名*/, 0/*对话框风格*/, "Text File|*.txt|", this/*父窗口指针*/);
	CString strFilePath;
	if (Open.DoModal() == IDOK)
	{
		strFilePath = Open.GetPathName();
		SetDlgItemText(IDC_EDIT1, strFilePath);
	}

	if(vbase.load_word_file(strFilePath.GetBuffer()))
	{
		MessageBox("Load word file error!");
	}
}

void Ctest1Dlg::OnBnClickedOk()
{
	// TODO: 在此添加控件通知处理程序代码
	
	OnOK();
}

void Ctest1Dlg::OnBnClickedButton3()
{
	// TODO: 在此添加控件通知处理程序代码
	CString strFilePath;
	GetDlgItemText(IDC_EDIT1, strFilePath);
	if(strFilePath.IsEmpty())
	{
		MessageBox("No data to save!");
		return;
	}
	//CString FileName = strFilePath.Left(strFilePath.GetLength()-4);
	//FileName += "_new.txt";
	
	vbase.sort_list(BYSTR);
	vbase.stable_sort_list(BYNUMR);
	if(vbase.save_all())
	{
		MessageBox("Save data failed!");
	}
	else
	{
		MessageBox("All word has been displayed!");
	}
}

/*
void Ctest1Dlg::OnKeyDown(UINT nChar, UINT nRepCnt, UINT nFlags) 
{
	if (char(nChar) == 'X')
		OnOK();

	CDialog::OnKeyDown(nChar, nRepCnt, nFlags);
}
*/