// test 1Dlg.cpp : implementation file
//

#include "stdafx.h"
#include "test 1.h"
#include "test 1Dlg.h"
#include "VocabularyBase.h"
#include <direct.h>


#ifdef _DEBUG
#define new DEBUG_NEW
#endif


VocabularyBase vbase;
int word_index = 0;
char *cwd = NULL;
//Ctest1Dlg dlg;
// CAboutDlg dialog used for App About
#if 0
Ctest1Dlg* Ctest1Dlg::__instance = 0;

Ctest1Dlg* Ctest1Dlg::Instance() {
    /*if (__instance == 0) {
        __instance = new Ctest1Dlg;
    }*/
    static Ctest1Dlg dlg;
    return &dlg;
}
#endif 

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

#if 1
BOOL Ctest1Dlg::PreTranslateMessage(MSG* pMsg)
{
    if(pMsg->message==WM_CHAR)
    {
        int num = vbase.get_number_of_new();
        if( word_index < num )
        {
            switch (pMsg->wParam) 
            {
                case 'j':
                    OnBnClickedButton5();
                    break;
                case 'k':
                    OnBnClickedButton6();   
                    break;
                case 'l':
                    OnBnClickedButton7();   
                    break;
                case 'n':
                    OnBnClickedButton1();
                    break;
                default:
                    break;
            }
        }
        else
        {
            AfxMessageBox("All words have been displayed!");
        }

    }

	return CDialog::PreTranslateMessage(pMsg);
}
#endif

Ctest1Dlg::Ctest1Dlg(CWnd* pParent /*=NULL*/)
	: CDialog(Ctest1Dlg::IDD, pParent)
	, m_infileStr(_T(""))
{
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void Ctest1Dlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//DDX_Text(pDX, IDC_EDIT1, m_infileStr);
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
    ON_BN_CLICKED(IDC_BUTTON4, &Ctest1Dlg::OnBnClickedButton4)
    ON_BN_CLICKED(IDC_BUTTON5, &Ctest1Dlg::OnBnClickedButton5)
    ON_BN_CLICKED(IDC_BUTTON6, &Ctest1Dlg::OnBnClickedButton6)
    ON_BN_CLICKED(IDC_BUTTON7, &Ctest1Dlg::OnBnClickedButton7)
    ON_BN_CLICKED(IDC_BUTTON8, &Ctest1Dlg::OnBnClickedButton8)
END_MESSAGE_MAP()



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
    if( (cwd = _getcwd( NULL, 0 )) == NULL )
    {
        MessageBox("getcwd error!");
    }

	if(vbase.init_base(cwd))
	{
		MessageBox("Init history file error!");
		return FALSE;
	}
    //((Ctest1App*)AfxGetApp())->m_hwndDlg=m_hWnd;
    /*if(CreateDirectory("./ttttt"))
    {
        AfxMessageBox("OK");
    }
    else
    {
        DWORD ret = GetLastError();
        if(ERROR_ALREADY_EXISTS == ret)
        {
            AfxMessageBox("exist");
        }
        else if(ERROR_PATH_NOT_FOUND == ret)
        {
            AfxMessageBox("Path not right");
        }

    }*/
    CFont * f; 
    f = new CFont; 
    f->CreateFont(53, // nHeight 
                 0, // nWidth 
                 0, // nEscapement 
                 0, // nOrientation 
                 FW_BOLD, // nWeight 
                 FALSE, // bItalic 
                 FALSE, // bUnderline 
                 0, // cStrikeOut 
                 ANSI_CHARSET, // nCharSet 
                 OUT_DEFAULT_PRECIS, // nOutPrecision 
                 CLIP_DEFAULT_PRECIS, // nClipPrecision 
                 DEFAULT_QUALITY, // nQuality 
                 DEFAULT_PITCH | FF_SWISS, // nPitchAndFamily 
                 _T("Times New Roman")); // lpszFac 


    GetDlgItem(IDC_STATIC)->SetFont(f);        
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
	if( word_index < num -1 )
	{
		SetDlgItemText(IDC_STATIC,vbase.get_new_word_at(++word_index).word.c_str());
        CString numofword, repeat_times;
        numofword.Format("There are %d word(s) need to be classified",
            num - word_index);
        SetDlgItemText(IDC_STATIC_NO,numofword);
        repeat_times.Format("This is the %d time(s) you met the word",
            vbase.get_unknown_times(vbase.get_new_word_at(word_index)));
        SetDlgItemText(IDC_STATIC_TIMES,repeat_times);
	}
	else
	{
        SetDlgItemText(IDC_STATIC_NO,"");
        SetDlgItemText(IDC_STATIC,"");
        SetDlgItemText(IDC_STATIC_TIMES,"");
        MessageBox("All word has been classified!");
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
        SetDlgItemText(IDC_WORD_PATH, strFilePath);    
	}
	else
	{
		MessageBox("Select one text file to load!");
		return;
	}

	if(vbase.load_word_file(strFilePath.GetBuffer()))
	{
		MessageBox("Load word file error!");
		return;
	}
    SetDlgItemText(IDC_STATIC,vbase.get_new_word_at(0).word.c_str());
    CString numofword,repeat_times;
    numofword.Format("There are %d word(s) need to be classified",
        vbase.get_number_of_new());
    SetDlgItemText(IDC_STATIC_NO,numofword);

    repeat_times.Format("This is the %d time(s) you met the word",
        vbase.get_unknown_times(vbase.get_new_word_at(0)));
    SetDlgItemText(IDC_STATIC_TIMES,repeat_times);

}

void Ctest1Dlg::OnBnClickedOk()
{
	// TODO: 在此添加控件通知处理程序代码
	int ret = AfxMessageBox("Save your data? ",MB_YESNOCANCEL);
    if(ret == IDCANCEL)
    {
        return;
    }
    else if(ret == IDYES)
    {
        OnBnClickedButton3();
        OnOK();
    }
    else if(ret == IDNO)
    {
        OnOK();
    }
    
    return;
}

void Ctest1Dlg::OnBnClickedButton3()
{
	// TODO: 在此添加控件通知处理程序代码
	CString strFilePath;
    
	//GetDlgItemText(IDC_EDIT1, strFilePath);
    GetDlgItemText(IDC_WORD_PATH, strFilePath);
	if(strFilePath.IsEmpty())
	{
		MessageBox("No data to save!");
		return;
	}
	//CString FileName = strFilePath.Left(strFilePath.GetLength()-4);
	//FileName += "_new.txt";
	
	vbase.sort_list(BYSTR);
	vbase.stable_sort_list(BYNUMR);
	//vbase.reset_all_counter();
	if(vbase.save_all(cwd))
	{
		MessageBox("Save data failed!");
	}
	else
	{
		MessageBox("Save data successfully!");
	}
}


void Ctest1Dlg::OnBnClickedButton4()
{
    CString strFilePath;
    GetDlgItemText(IDC_WORD_PATH, strFilePath);
    int n = strFilePath.Replace(_T(".txt"), _T("_new.txt"));
    ASSERT(n == 1);
    if(0 == vbase.save_word_to_file(strFilePath.GetBuffer()))
    {   
        MessageBox("Save data successfully!");
    }
    else
    {
        MessageBox("Save data failed!");
    }
}

void Ctest1Dlg::OnBnClickedButton5()
{
    vbase.clssify_word(vbase.get_new_word_at(word_index),KNOWN);
    OnBnClickedButton1();
}

void Ctest1Dlg::OnBnClickedButton6()
{
    vbase.clssify_word(vbase.get_new_word_at(word_index),UNKNOWN);
    OnBnClickedButton1();
}

void Ctest1Dlg::OnBnClickedButton7()
{
    vbase.clssify_word(vbase.get_new_word_at(word_index),NONEED);
    OnBnClickedButton1();
}

void Ctest1Dlg::OnBnClickedButton8()
{
    OnBnClickedButton1();
}
