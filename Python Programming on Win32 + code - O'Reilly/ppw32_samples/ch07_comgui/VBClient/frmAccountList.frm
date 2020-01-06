VERSION 5.00
Begin VB.Form frmAccountList 
   Caption         =   "Account list"
   ClientHeight    =   3195
   ClientLeft      =   60
   ClientTop       =   345
   ClientWidth     =   4680
   LinkTopic       =   "Form1"
   MDIChild        =   -1  'True
   ScaleHeight     =   3195
   ScaleWidth      =   4680
   Begin VB.ListBox lstAccounts 
      Height          =   2595
      Left            =   240
      TabIndex        =   0
      Top             =   120
      Width           =   4215
   End
End
Attribute VB_Name = "frmAccountList"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit
'Implements UpdatableView

Private Sub Form_Load()
    Form_Resize
End Sub

Private Sub Form_Resize()
    On Error Resume Next
    lstAccounts.Move 40, 40, Me.ScaleWidth - 80, Me.ScaleHeight - 80
End Sub

Public Sub UpdateView()

    Dim count, i As Integer
    Dim acctlist As Variant
    Dim strAcct As Variant
    Screen.MousePointer = vbHourglass
    DoEvents
    
    
    lstAccounts.Clear
    
    acctlist = frmMain.BookServer.getAccountList
    For Each strAcct In acctlist
        lstAccounts.AddItem strAcct
    Next
    
    
    Screen.MousePointer = vbDefault
    DoEvents
    
    'Caption
    Caption = "Account list - " & lstAccounts.ListCount & " accounts"
    
End Sub


Private Sub lstAccounts_DblClick()
    'ask what type of view
    Dim TypeCode As String
    Dim acct As String
        
    acct = lstAccounts.text
    
    TypeCode = InputBox("Enter C for Chart, L for List view", "Specify View Type")
    If LCase(Left(Trim(TypeCode), 1)) <> "c" Then
        'Create an account view
        Dim newAccountView As New frmAccountView
        newAccountView.SetAccount acct
        frmMain.MDIChildren.Add newAccountView
        newAccountView.Show
        newAccountView.UpdateView
    Else
        'Create a chart view
        Dim newAccountChart As New frmAccountChart
        newAccountChart.SetAccount acct
        frmMain.MDIChildren.Add newAccountChart
        newAccountChart.Show
        newAccountChart.UpdateView
    End If
    
    
End Sub



