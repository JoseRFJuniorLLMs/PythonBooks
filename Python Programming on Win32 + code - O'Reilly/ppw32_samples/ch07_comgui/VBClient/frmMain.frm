VERSION 5.00
Object = "{F9043C88-F6F2-101A-A3C9-08002B2F49FB}#1.2#0"; "COMDLG32.OCX"
Object = "{831FDD16-0C5C-11D2-A9FC-0000F8754DA1}#2.0#0"; "MSCOMCTL.OCX"
Begin VB.MDIForm frmMain 
   BackColor       =   &H8000000C&
   Caption         =   "Doubletalk Browser - Visual Basic Edition"
   ClientHeight    =   6705
   ClientLeft      =   165
   ClientTop       =   735
   ClientWidth     =   7230
   LinkTopic       =   "MDIForm1"
   StartUpPosition =   3  'Windows Default
   Begin MSComDlg.CommonDialog dlgCommonDialog 
      Left            =   2520
      Top             =   1350
      _ExtentX        =   847
      _ExtentY        =   847
      _Version        =   393216
   End
   Begin MSComctlLib.StatusBar sbStatusBar 
      Align           =   2  'Align Bottom
      Height          =   270
      Left            =   0
      TabIndex        =   0
      Top             =   6435
      Width           =   7230
      _ExtentX        =   12753
      _ExtentY        =   476
      _Version        =   393216
      BeginProperty Panels {8E3867A5-8586-11D1-B16A-00C0F0283628} 
         NumPanels       =   3
         BeginProperty Panel1 {8E3867AB-8586-11D1-B16A-00C0F0283628} 
            AutoSize        =   1
            Object.Width           =   7117
            Text            =   "Status"
            TextSave        =   "Status"
         EndProperty
         BeginProperty Panel2 {8E3867AB-8586-11D1-B16A-00C0F0283628} 
            Style           =   6
            AutoSize        =   2
            TextSave        =   "26/04/99"
         EndProperty
         BeginProperty Panel3 {8E3867AB-8586-11D1-B16A-00C0F0283628} 
            Style           =   5
            AutoSize        =   2
            TextSave        =   "22:07"
         EndProperty
      EndProperty
   End
   Begin MSComctlLib.ImageList imlToolbarIcons 
      Left            =   1740
      Top             =   1350
      _ExtentX        =   1005
      _ExtentY        =   1005
      BackColor       =   -2147483643
      ImageWidth      =   16
      ImageHeight     =   16
      MaskColor       =   12632256
      _Version        =   393216
      BeginProperty Images {2C247F25-8591-11D1-B16A-00C0F0283628} 
         NumListImages   =   13
         BeginProperty ListImage1 {2C247F27-8591-11D1-B16A-00C0F0283628} 
            Picture         =   "frmMain.frx":0000
            Key             =   "New"
         EndProperty
         BeginProperty ListImage2 {2C247F27-8591-11D1-B16A-00C0F0283628} 
            Picture         =   "frmMain.frx":0112
            Key             =   "Open"
         EndProperty
         BeginProperty ListImage3 {2C247F27-8591-11D1-B16A-00C0F0283628} 
            Picture         =   "frmMain.frx":0224
            Key             =   "Save"
         EndProperty
         BeginProperty ListImage4 {2C247F27-8591-11D1-B16A-00C0F0283628} 
            Picture         =   "frmMain.frx":0336
            Key             =   "Print"
         EndProperty
         BeginProperty ListImage5 {2C247F27-8591-11D1-B16A-00C0F0283628} 
            Picture         =   "frmMain.frx":0448
            Key             =   "Cut"
         EndProperty
         BeginProperty ListImage6 {2C247F27-8591-11D1-B16A-00C0F0283628} 
            Picture         =   "frmMain.frx":055A
            Key             =   "Copy"
         EndProperty
         BeginProperty ListImage7 {2C247F27-8591-11D1-B16A-00C0F0283628} 
            Picture         =   "frmMain.frx":066C
            Key             =   "Paste"
         EndProperty
         BeginProperty ListImage8 {2C247F27-8591-11D1-B16A-00C0F0283628} 
            Picture         =   "frmMain.frx":077E
            Key             =   "Bold"
         EndProperty
         BeginProperty ListImage9 {2C247F27-8591-11D1-B16A-00C0F0283628} 
            Picture         =   "frmMain.frx":0890
            Key             =   "Italic"
         EndProperty
         BeginProperty ListImage10 {2C247F27-8591-11D1-B16A-00C0F0283628} 
            Picture         =   "frmMain.frx":09A2
            Key             =   "Underline"
         EndProperty
         BeginProperty ListImage11 {2C247F27-8591-11D1-B16A-00C0F0283628} 
            Picture         =   "frmMain.frx":0AB4
            Key             =   "Align Left"
         EndProperty
         BeginProperty ListImage12 {2C247F27-8591-11D1-B16A-00C0F0283628} 
            Picture         =   "frmMain.frx":0BC6
            Key             =   "Center"
         EndProperty
         BeginProperty ListImage13 {2C247F27-8591-11D1-B16A-00C0F0283628} 
            Picture         =   "frmMain.frx":0CD8
            Key             =   "Align Right"
         EndProperty
      EndProperty
   End
   Begin MSComctlLib.Toolbar tbToolBar 
      Align           =   1  'Align Top
      Height          =   420
      Left            =   0
      TabIndex        =   1
      Top             =   0
      Width           =   7230
      _ExtentX        =   12753
      _ExtentY        =   741
      ButtonWidth     =   609
      ButtonHeight    =   582
      Appearance      =   1
      ImageList       =   "imlToolbarIcons"
      _Version        =   393216
      BeginProperty Buttons {66833FE8-8583-11D1-B16A-00C0F0283628} 
         NumButtons      =   10
         BeginProperty Button1 {66833FEA-8583-11D1-B16A-00C0F0283628} 
            Key             =   "New"
            Object.ToolTipText     =   "New"
            ImageKey        =   "New"
         EndProperty
         BeginProperty Button2 {66833FEA-8583-11D1-B16A-00C0F0283628} 
            Key             =   "Open"
            Object.ToolTipText     =   "Open"
            ImageKey        =   "Open"
         EndProperty
         BeginProperty Button3 {66833FEA-8583-11D1-B16A-00C0F0283628} 
            Key             =   "Save"
            Object.ToolTipText     =   "Save"
            ImageKey        =   "Save"
         EndProperty
         BeginProperty Button4 {66833FEA-8583-11D1-B16A-00C0F0283628} 
            Style           =   3
         EndProperty
         BeginProperty Button5 {66833FEA-8583-11D1-B16A-00C0F0283628} 
            Key             =   "Print"
            Object.ToolTipText     =   "Print"
            ImageKey        =   "Print"
         EndProperty
         BeginProperty Button6 {66833FEA-8583-11D1-B16A-00C0F0283628} 
            Style           =   3
         EndProperty
         BeginProperty Button7 {66833FEA-8583-11D1-B16A-00C0F0283628} 
            Key             =   "Cut"
            Object.ToolTipText     =   "Cut"
            ImageKey        =   "Cut"
         EndProperty
         BeginProperty Button8 {66833FEA-8583-11D1-B16A-00C0F0283628} 
            Key             =   "Copy"
            Object.ToolTipText     =   "Copy"
            ImageKey        =   "Copy"
         EndProperty
         BeginProperty Button9 {66833FEA-8583-11D1-B16A-00C0F0283628} 
            Key             =   "Paste"
            Object.ToolTipText     =   "Paste"
            ImageKey        =   "Paste"
         EndProperty
         BeginProperty Button10 {66833FEA-8583-11D1-B16A-00C0F0283628} 
            Style           =   3
         EndProperty
      EndProperty
   End
   Begin VB.Menu mnuFile 
      Caption         =   "&File"
      Begin VB.Menu mnuFileNew 
         Caption         =   "&New"
         Shortcut        =   ^N
      End
      Begin VB.Menu mnuFileOpen 
         Caption         =   "&Open..."
         Shortcut        =   ^O
      End
      Begin VB.Menu mnuFileClose 
         Caption         =   "&Close"
      End
      Begin VB.Menu mnuFileBar0 
         Caption         =   "-"
      End
      Begin VB.Menu mnuFileSave 
         Caption         =   "&Save"
      End
      Begin VB.Menu mnuFileSaveAs 
         Caption         =   "Save &As..."
      End
      Begin VB.Menu mnuFileSaveAll 
         Caption         =   "Save A&ll"
      End
      Begin VB.Menu mnuFileBar1 
         Caption         =   "-"
      End
      Begin VB.Menu mnuFileProperties 
         Caption         =   "Propert&ies"
      End
      Begin VB.Menu mnuFileBar2 
         Caption         =   "-"
      End
      Begin VB.Menu mnuFilePageSetup 
         Caption         =   "Page Set&up..."
      End
      Begin VB.Menu mnuFilePrintPreview 
         Caption         =   "Print Pre&view"
      End
      Begin VB.Menu mnuFilePrint 
         Caption         =   "&Print..."
      End
      Begin VB.Menu mnuFileBar3 
         Caption         =   "-"
      End
      Begin VB.Menu mnuFileSend 
         Caption         =   "Sen&d..."
      End
      Begin VB.Menu mnuFileBar4 
         Caption         =   "-"
      End
      Begin VB.Menu mnuFileMRU 
         Caption         =   ""
         Index           =   1
         Visible         =   0   'False
      End
      Begin VB.Menu mnuFileMRU 
         Caption         =   ""
         Index           =   2
         Visible         =   0   'False
      End
      Begin VB.Menu mnuFileMRU 
         Caption         =   ""
         Index           =   3
         Visible         =   0   'False
      End
      Begin VB.Menu mnuFileBar5 
         Caption         =   "-"
         Visible         =   0   'False
      End
      Begin VB.Menu mnuFileExit 
         Caption         =   "E&xit"
      End
   End
   Begin VB.Menu mnuEdit 
      Caption         =   "&Edit"
      Begin VB.Menu mnuEditUndo 
         Caption         =   "&Undo"
      End
      Begin VB.Menu mnuEditBar0 
         Caption         =   "-"
      End
      Begin VB.Menu mnuEditCut 
         Caption         =   "Cu&t"
         Shortcut        =   ^X
      End
      Begin VB.Menu mnuEditCopy 
         Caption         =   "&Copy"
         Shortcut        =   ^C
      End
      Begin VB.Menu mnuEditPaste 
         Caption         =   "&Paste"
         Shortcut        =   ^V
      End
      Begin VB.Menu mnuEditPasteSpecial 
         Caption         =   "Paste &Special..."
      End
      Begin VB.Menu mnuEditBar1 
         Caption         =   "-"
      End
      Begin VB.Menu mnuEditAdd 
         Caption         =   "&Add Transaction"
      End
   End
   Begin VB.Menu mnuView 
      Caption         =   "&View"
      Begin VB.Menu mnuViewToolbar 
         Caption         =   "&Toolbar"
         Checked         =   -1  'True
      End
      Begin VB.Menu mnuViewStatusBar 
         Caption         =   "Status &Bar"
         Checked         =   -1  'True
      End
      Begin VB.Menu mnuViewConsole 
         Caption         =   "&Console"
      End
      Begin VB.Menu mnuViewBar0 
         Caption         =   "-"
      End
      Begin VB.Menu mnuViewRefresh 
         Caption         =   "&Refresh"
      End
      Begin VB.Menu mnuViewOptions 
         Caption         =   "&Options..."
      End
      Begin VB.Menu mnuViewBar1 
         Caption         =   "-"
      End
      Begin VB.Menu mnuToolsAccountView 
         Caption         =   "New Account Details View"
      End
      Begin VB.Menu mnuViewAccountList 
         Caption         =   "New Account List View"
      End
      Begin VB.Menu mnuViewChart 
         Caption         =   "New Char&t"
      End
      Begin VB.Menu mnuViewScript 
         Caption         =   "New &Script Editor"
      End
      Begin VB.Menu mnuViewUser 
         Caption         =   "&User-defined view"
      End
   End
   Begin VB.Menu mnuTools 
      Caption         =   "&Tools"
      Begin VB.Menu mnuToolsUpdate 
         Caption         =   "&Update All Views"
      End
      Begin VB.Menu mnuToolsTestServer 
         Caption         =   "&Test Server"
      End
      Begin VB.Menu mnuToolsUpdateCurrentView 
         Caption         =   "&Update Current View"
      End
      Begin VB.Menu mnuToolsAdd2 
         Caption         =   "Add Dummy Transaction"
      End
      Begin VB.Menu mnuToolsTemp 
         Caption         =   "temp"
      End
      Begin VB.Menu mnuToolsBar0 
         Caption         =   "-"
      End
      Begin VB.Menu mnuToolsExec 
         Caption         =   "E&xec user expression"
      End
      Begin VB.Menu mnuToolsEval 
         Caption         =   "E&val user expression"
      End
      Begin VB.Menu mnuToolsBar1 
         Caption         =   "-"
      End
      Begin VB.Menu mnuToolsOptions 
         Caption         =   "&Options"
      End
   End
   Begin VB.Menu mnuWindow 
      Caption         =   "&Window"
      WindowList      =   -1  'True
      Begin VB.Menu mnuWindowNewWindow 
         Caption         =   "&New Window"
      End
      Begin VB.Menu mnuWindowBar0 
         Caption         =   "-"
      End
      Begin VB.Menu mnuWindowCascade 
         Caption         =   "&Cascade"
      End
      Begin VB.Menu mnuWindowTileHorizontal 
         Caption         =   "Tile &Horizontal"
      End
      Begin VB.Menu mnuWindowTileVertical 
         Caption         =   "Tile &Vertical"
      End
      Begin VB.Menu mnuWindowArrangeIcons 
         Caption         =   "&Arrange Icons"
      End
   End
   Begin VB.Menu mnuHelp 
      Caption         =   "&Help"
      Begin VB.Menu mnuHelpContents 
         Caption         =   "&Contents"
      End
      Begin VB.Menu mnuHelpSearchForHelpOn 
         Caption         =   "&Search For Help On..."
      End
      Begin VB.Menu mnuHelpBar0 
         Caption         =   "-"
      End
      Begin VB.Menu mnuHelpAbout 
         Caption         =   "&About "
      End
   End
End
Attribute VB_Name = "frmMain"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private Declare Function SendMessage Lib "user32" Alias "SendMessageA" (ByVal hwnd As Long, ByVal wMsg As Long, ByVal wParam As Long, ByVal lParam As Any) As Long
Const EM_UNDO = &HC7
Private Declare Function OSWinHelp% Lib "user32" Alias "WinHelpA" (ByVal hwnd&, ByVal HelpFile$, ByVal wCommand%, dwData As Any)
Public BookServer As Object
Public MDIChildren As New Collection
Public RemoteMachine As String
Public FileName As String


Private Sub MDIForm_Load()
    InitCOMServer
    frmJournal.Show
    MDIChildren.Add frmJournal
    RemoteMachine = ""
    Me.UpdateCaption
End Sub

Private Sub MDIForm_Unload(Cancel As Integer)
    CloseCOMServer
    End
End Sub

Sub InitCOMServer()
    Dim startupScript As String
    
    'called when the program starts
    On Error GoTo InitCOMServer_error
    
    Set BookServer = CreateObject("Doubletalk.BookServer", RemoteMachine)
    
    On Error GoTo 0
    
    'tell it to capture output for the console
    BookServer.beginTrappingOutput
    
    'if there is an init script, run it
    If frmOptions.txtStartupScript.text <> "" Then
        On Error GoTo InitCOMServer_StartupScriptError
        BookServer.execFile frmOptions.txtStartupScript.text
        On Error GoTo 0
    End If
    
    'grab any standard output for the console
    frmConsole.UpdateOutput
    Exit Sub
    
InitCOMServer_error:
    Dim msg As String
    msg = "There was an error trying to initialize the BookServer." + _
            "Please check that it is properly registered and try the Python " + _
            "test functions first.  The program will now abort."
    MsgBox msg
    End
    
InitCOMServer_StartupScriptError:
    MsgBox "An error occurred running your startup script '" + _
        frmOptions.txtStartupScript.text + "'. " + _
        "Please check it is present and correct."
End Sub

Sub CloseCOMServer()
    Set BookServer = Nothing
End Sub

Sub TestCOMServer()
    'just to check it is alive
    Dim hopefully_four As Integer
    hopefully_four = BookServer.Double(2)
    MsgBox "2 x 2 = " & hopefully_four & ", so your server is alive"
End Sub

Public Sub UpdateAllViews()
    Dim ChildForm As Form
    For Each ChildForm In MDIChildren  'this will only work if they implement UpdateView
        ChildForm.UpdateView
    Next
    
    UpdateCaption
    
End Sub

Private Sub mnuEditAdd_Click()
    frmTranDialog.AddNew
    
End Sub

Private Sub mnuToolsAccountView_Click()
    Dim acview As frmAccountView
    Set acview = New frmAccountView
    MDIChildren.Add acview
    acview.SetAccount "MyCo.Assets.OtherLia.BankLoan"
    acview.Show
    acview.UpdateView
    
End Sub

Private Sub mnuToolsAdd1_Click()
    'test adding with CreateObject
    Dim newtran As Object
    
    Set newtran = CreateObject("Doubletalk.Transaction")
    newtran.setDateString "31/12/99"
    newtran.setComment "Python on Windows Royalty Cheque"
    newtran.AddLine "MyCo.Assets.NCA.CurAss.Cash", 5000
    newtran.addLastLine "MyCo.Capital.PL.Income.Writing"
    
    BookServer.Add newtran
    frmJournal.UpdateView
End Sub
Private Sub mnuToolsAdd2_Click()
    'test adding with BookServer.CreateTransaction
    Dim newtran As Object
    
    Set newtran = BookServer.CreateTransaction
    newtran.setDateString "31/3/99"
    newtran.setComment "Even more royalties"
    newtran.AddLine "MyCo.Assets.NCA.CurAss.Cash", 5000
    newtran.addLastLine "MyCo.Capital.PL.Income.Writing"
    
    BookServer.Add newtran
    frmJournal.UpdateView
End Sub

Private Sub mnuToolsEval_Click()
    Dim result As Variant
    Dim expr As String
    
    expr = InputBox("Enter a Python expression", "Dynamic Expression Evaluation")
    
    'handle any errors
    On Error GoTo mnuToolsEval_Click_Error
    result = BookServer.interpretString(expr)
    On Error GoTo 0
    
    MsgBox "Result is: " + vbCrLf + result
    Exit Sub
    
mnuToolsEval_Click_Error:
    MsgBox "Python encountered an error while evaluating/executing " + _
                "your code. " + vbCrLf + _
                "Your expression was: '" + expr + "'" + vbCrLf + _
                "The Error Message was: " + vbCrLf + vbCrLf + Err.Description
    
End Sub

Private Sub mnuToolsExec_Click()
    Dim expr As String
    expr = InputBox("Enter a Python expression", "Dynamic Expression Evaluation")
    
    On Error GoTo mnuToolsExec_Click_Error
    BookServer.execstring expr
    Exit Sub

mnuToolsExec_Click_Error:
    MsgBox "Python encountered an error while executing your code. " + vbCrLf + _
                "Your expression: '" + expr + "'" + vbCrLf + _
                "Error Message: " + vbCrLf + Err.Description

End Sub

Private Sub mnuToolsOptions_Click()
    frmOptions.Show vbModal
End Sub

Private Sub mnuToolsTemp_Click()
    MsgBox Me.count
End Sub

Private Sub mnuToolsTestServer_Click()
    'this helps establish if the COM server is alive
    'using a minimal diagnostic function in the modMain module
    TestCOMServer
End Sub

Private Sub mnuToolsUpdate_Click()
    UpdateAllViews
End Sub

Private Sub mnuToolsUpdateCurrentView_Click()
    ActiveForm.UpdateView
End Sub


Private Sub mnuViewAccountList_Click()
    Dim aclistview As frmAccountList
    Set aclistview = New frmAccountList
    MDIChildren.Add aclistview
    aclistview.Show
    aclistview.UpdateView
End Sub

Private Sub mnuViewChart_Click()
    Dim chartview As frmAccountChart
    Set chartview = New frmAccountChart
    MDIChildren.Add chartview
    chartview.Show
    chartview.UpdateView
End Sub

Private Sub mnuViewConsole_Click()
    If mnuViewConsole.Checked Then
        frmConsole.Hide
        mnuViewConsole.Checked = False
    Else
        frmConsole.Show
        mnuViewConsole.Checked = True
    End If
End Sub

Private Sub mnuViewScript_Click()
    Dim frmEdit As New frmScriptEditor
    frmEdit.Show
End Sub

Private Sub mnuViewUser_Click()
    Dim view As New frmUserView
    Dim name As String
    
    name = InputBox("Enter the name of a daa view you have created")
    If name = "" Then Exit Sub
    
    view.ViewName = name
    view.Show
    view.UpdateView
    
End Sub

Private Sub tbToolBar_ButtonClick(ByVal Button As MSComCtlLib.Button)
    On Error Resume Next
    Select Case Button.Key
        Case "Open"
            mnuFileOpen_Click
        Case "Save"
            mnuFileSave_Click
        Case "Print"
            mnuFilePrint_Click
        Case "Cut"
            mnuEditCut_Click
        Case "Copy"
            mnuEditCopy_Click
        Case "Paste"
            mnuEditPaste_Click
        Case "Bold"
            ActiveForm.rtfText.SelBold = Not ActiveForm.rtfText.SelBold
            Button.Value = IIf(ActiveForm.rtfText.SelBold, tbrPressed, tbrUnpressed)
        Case "Italic"
            ActiveForm.rtfText.SelItalic = Not ActiveForm.rtfText.SelItalic
            Button.Value = IIf(ActiveForm.rtfText.SelItalic, tbrPressed, tbrUnpressed)
        Case "Underline"
            ActiveForm.rtfText.SelUnderline = Not ActiveForm.rtfText.SelUnderline
            Button.Value = IIf(ActiveForm.rtfText.SelUnderline, tbrPressed, tbrUnpressed)
        Case "Align Left"
            ActiveForm.rtfText.SelAlignment = rtfLeft
        Case "Center"
            ActiveForm.rtfText.SelAlignment = rtfCenter
        Case "Align Right"
            ActiveForm.rtfText.SelAlignment = rtfRight
    End Select
End Sub

Private Sub mnuHelpAbout_Click()
    frmAbout.Show vbModal, Me
End Sub

Private Sub mnuHelpSearchForHelpOn_Click()
    Dim nRet As Integer


    'if there is no helpfile for this project display a message to the user
    'you can set the HelpFile for your application in the
    'Project Properties dialog
    If Len(App.HelpFile) = 0 Then
        MsgBox "Unable to display Help Contents. There is no Help associated with this project.", vbInformation, Me.Caption
    Else
        On Error Resume Next
        nRet = OSWinHelp(Me.hwnd, App.HelpFile, 261, 0)
        If Err Then
            MsgBox Err.Description
        End If
    End If

End Sub

Private Sub mnuHelpContents_Click()
    Dim nRet As Integer


    'if there is no helpfile for this project display a message to the user
    'you can set the HelpFile for your application in the
    'Project Properties dialog
    If Len(App.HelpFile) = 0 Then
        MsgBox "Unable to display Help Contents. There is no Help associated with this project.", vbInformation, Me.Caption
    Else
        On Error Resume Next
        nRet = OSWinHelp(Me.hwnd, App.HelpFile, 3, 0)
        If Err Then
            MsgBox Err.Description
        End If
    End If

End Sub


Private Sub mnuWindowArrangeIcons_Click()
    Me.Arrange vbArrangeIcons
End Sub

Private Sub mnuWindowTileVertical_Click()
    Me.Arrange vbTileVertical
End Sub

Private Sub mnuWindowTileHorizontal_Click()
    Me.Arrange vbTileHorizontal
End Sub

Private Sub mnuWindowCascade_Click()
    Me.Arrange vbCascade
End Sub

Private Sub mnuWindowNewWindow_Click()
    'LoadNewDoc
End Sub

Private Sub mnuViewOptions_Click()
    frmOptions.Show vbModal, Me
End Sub

Private Sub mnuViewRefresh_Click()
    'ToDo: Add 'mnuViewRefresh_Click' code.
    MsgBox "Add 'mnuViewRefresh_Click' code."
End Sub

Private Sub mnuViewStatusBar_Click()
    mnuViewStatusBar.Checked = Not mnuViewStatusBar.Checked
    sbStatusBar.Visible = mnuViewStatusBar.Checked
End Sub

Private Sub mnuViewToolbar_Click()
    mnuViewToolbar.Checked = Not mnuViewToolbar.Checked
    tbToolBar.Visible = mnuViewToolbar.Checked
End Sub

Private Sub mnuEditPasteSpecial_Click()
    'ToDo: Add 'mnuEditPasteSpecial_Click' code.
    MsgBox "Add 'mnuEditPasteSpecial_Click' code."
End Sub

Private Sub mnuEditPaste_Click()
    On Error Resume Next
    ActiveForm.rtfText.SelRTF = Clipboard.GetText

End Sub

Private Sub mnuEditCopy_Click()
    On Error Resume Next
    Clipboard.SetText ActiveForm.rtfText.SelRTF

End Sub

Private Sub mnuEditCut_Click()
    On Error Resume Next
    Clipboard.SetText ActiveForm.rtfText.SelRTF
    ActiveForm.rtfText.SelText = vbNullString

End Sub

Private Sub mnuEditUndo_Click()
    'ToDo: Add 'mnuEditUndo_Click' code.
    MsgBox "Add 'mnuEditUndo_Click' code."
End Sub


Private Sub mnuFileExit_Click()
    'unload the form
    Unload Me

End Sub

Private Sub mnuFileSend_Click()
    'ToDo: Add 'mnuFileSend_Click' code.
    MsgBox "Add 'mnuFileSend_Click' code."
End Sub

Private Sub mnuFilePrint_Click()
    On Error Resume Next
    If ActiveForm Is Nothing Then Exit Sub
    

    With dlgCommonDialog
        .DialogTitle = "Print"
        .CancelError = True
        .Flags = cdlPDReturnDC + cdlPDNoPageNums
        If ActiveForm.rtfText.SelLength = 0 Then
            .Flags = .Flags + cdlPDAllPages
        Else
            .Flags = .Flags + cdlPDSelection
        End If
        .ShowPrinter
        If Err <> MSComDlg.cdlCancel Then
            ActiveForm.rtfText.SelPrint .hDC
        End If
    End With

End Sub

Private Sub mnuFilePrintPreview_Click()
    'ToDo: Add 'mnuFilePrintPreview_Click' code.
    MsgBox "Add 'mnuFilePrintPreview_Click' code."
End Sub

Private Sub mnuFilePageSetup_Click()
    On Error Resume Next
    With dlgCommonDialog
        .DialogTitle = "Page Setup"
        .CancelError = True
        .ShowPrinter
    End With

End Sub

Private Sub mnuFileProperties_Click()
    'ToDo: Add 'mnuFileProperties_Click' code.
    MsgBox "Add 'mnuFileProperties_Click' code."
End Sub

Private Sub mnuFileSaveAll_Click()
    'ToDo: Add 'mnuFileSaveAll_Click' code.
    MsgBox "Add 'mnuFileSaveAll_Click' code."
End Sub

Private Sub mnuFileSaveAs_Click()
    Dim sFile As String
    

    If ActiveForm Is Nothing Then Exit Sub
    

    With dlgCommonDialog
        .DialogTitle = "Save As"
        .CancelError = False
        'ToDo: set the flags and attributes of the common dialog control
        .Filter = "All Files (*.*)|*.*"
        .ShowSave
        If Len(.FileName) = 0 Then
            Exit Sub
        End If
        sFile = .FileName
    End With
    ActiveForm.Caption = sFile
    ActiveForm.rtfText.SaveFile sFile

End Sub

Private Sub mnuFileSave_Click()
    Dim sFile As String
    If Left$(ActiveForm.Caption, 8) = "Document" Then
        With dlgCommonDialog
            .DialogTitle = "Save"
            .CancelError = False
            'ToDo: set the flags and attributes of the common dialog control
            .Filter = "All Files (*.*)|*.*"
            .ShowSave
            If Len(.FileName) = 0 Then
                Exit Sub
            End If
            sFile = .FileName
        End With
        ActiveForm.rtfText.SaveFile sFile
    Else
        sFile = ActiveForm.Caption
        ActiveForm.rtfText.SaveFile sFile
    End If

End Sub

Private Sub mnuFileClose_Click()
    'ToDo: Add 'mnuFileClose_Click' code.
    MsgBox "Add 'mnuFileClose_Click' code."
End Sub

Private Sub mnuFileOpen_Click()
    Dim sFile As String
    Dim sShortFile As String
    Dim i As Integer
    Dim sChar As String * 1
    
    With dlgCommonDialog
        .DialogTitle = "Open"
        .CancelError = False
        'ToDo: set the flags and attributes of the common dialog control
        .Filter = "Doubletalk Journal Files (*.dtj)|*.dtj"
        .ShowOpen
        If Len(.FileName) = 0 Then
            Exit Sub
        End If
        sFile = .FileName
    End With
    BookServer.Load sFile
    FileName = sFile    'store it in the form
    'display something helpful in the Journal caption
    
    'extract filename, dropping the path
    sShortFile = ""
    i = Len(sFile)
    sChar = Mid(sFile, i, 1)
    While sChar <> "\"
        sShortFile = sChar + sShortFile
        i = i - 1
        sChar = Mid(sFile, i, 1)
    Wend
    frmJournal.Caption = sShortFile & ", " & BookServer.count & " Transactions"
    frmJournal.UpdateView
    UpdateCaption
End Sub

Private Sub mnuFileNew_Click()
    'LoadNewDoc
End Sub

Public Sub UpdateCaption()
    Dim NewCaption As String
    If (RemoteMachine = "") And (FileName = "") Then Exit Sub
    NewCaption = FileName
    If RemoteMachine <> "" Then
        NewCaption = NewCaption + " on \\" + RemoteMachine
    End If
    Me.Caption = NewCaption
End Sub
