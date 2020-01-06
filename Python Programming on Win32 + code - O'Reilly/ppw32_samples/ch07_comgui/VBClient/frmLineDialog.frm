VERSION 5.00
Begin VB.Form frmLineDialog 
   BorderStyle     =   3  'Fixed Dialog
   Caption         =   "Dialog Caption"
   ClientHeight    =   3015
   ClientLeft      =   2760
   ClientTop       =   3750
   ClientWidth     =   7530
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   3015
   ScaleWidth      =   7530
   ShowInTaskbar   =   0   'False
   Begin VB.TextBox txtAmount 
      Height          =   285
      Left            =   1680
      TabIndex        =   5
      Text            =   "Text1"
      Top             =   960
      Width           =   1815
   End
   Begin VB.ComboBox cboAccount 
      Height          =   315
      Left            =   120
      TabIndex        =   4
      Text            =   "Combo1"
      Top             =   360
      Width           =   7095
   End
   Begin VB.CommandButton cmdCancel 
      Caption         =   "Cancel"
      Height          =   375
      Left            =   3840
      TabIndex        =   1
      Top             =   2280
      Width           =   1215
   End
   Begin VB.CommandButton cmdOK 
      Caption         =   "OK"
      Default         =   -1  'True
      Height          =   375
      Left            =   2160
      TabIndex        =   0
      Top             =   2280
      Width           =   1215
   End
   Begin VB.Label Label2 
      Caption         =   "Amount"
      Height          =   255
      Left            =   120
      TabIndex        =   3
      Top             =   960
      Width           =   1455
   End
   Begin VB.Label Label1 
      Caption         =   "Account:"
      Height          =   255
      Left            =   120
      TabIndex        =   2
      Top             =   0
      Width           =   1335
   End
End
Attribute VB_Name = "frmLineDialog"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
'this dialog lets you edit one line of a transaction
'maintains a list of accounts in the combobox
'exposes two variable the user can edit or access from outside -
'account and amount; and methods, AddLine and EditLine, which
'run the dialog and return whether OK was clicked.

Option Explicit
Private FormExit As Integer

Public Account As String
Public Amount As Currency


Public Function AddLine() As Boolean
    'call this to interactively prompt for a new line
    Account = ""
    Amount = 0
    cboAccount.Text = ""
    txtAmount.Text = "0.00"
    cmdOK.Enabled = False  'force a change and validation before they OK
    
    Show vbModal
    
    If FormExit = vbOK Then
        Account = cboAccount.Text
        Amount = Val(txtAmount.Text)
        AddLine = True
    Else
        AddLine = False
    End If
End Function

Public Function EditLine(acct As String, amt As Currency) As Boolean
    'call this to interactively prompt for a new line
    Account = acct
    Amount = amt
    cboAccount.Text = acct
    txtAmount.Text = Str(amt)
    
    cmdOK.Enabled = False  'force a change and validation before they OK
    
    Show vbModal
    
    If FormExit = vbOK Then
        Account = cboAccount.Text
        Amount = Val(txtAmount.Text)
        EditLine = True
    Else
        EditLine = False
    End If
End Function


Private Sub cboAccount_Change()
    Validate
End Sub

Private Sub txtAmount_Change()
   Validate
End Sub


Private Sub cmdCancel_Click()
    FormExit = vbCancel
    Hide
End Sub

Private Sub cmdOK_Click()
    'if text not in list, prompt.
    Dim txt As String
    Dim i As Integer
    Dim found As Boolean
    Dim confirmed As Boolean
    
    'check if the text is in the list
    found = False
    txt = cboAccount.Text
    For i = 0 To cboAccount.ListCount - 1
        If cboAccount.List(i) = cboAccount.Text Then
            found = True
            Exit For
        End If
    Next i
    
    If Not found Then
        confirmed = MsgBox( _
            "The account '" & cboAccount.Text & "' is a new one.  Proceed?", _
            vbOKCancel, _
            "Add new account?" _
            )
        If Not confirmed Then Exit Sub
    End If
    
    
    FormExit = vbOK
    Hide
End Sub

Private Sub Form_Load()
    UpdateAccountsList
End Sub

Private Sub Validate()
    'disable OK buton unless valid
    Dim valid As Boolean
    
    valid = (Trim(cboAccount.Text) <> "" Or IsNumeric(txtAmount.Text))
    cmdOK.Enabled = valid
    
End Sub

Private Sub UpdateAccountsList()
    Dim acctlist As Variant
    Dim strAcct As Variant
    cboAccount.Clear
    
    acctlist = frmMain.BookServer.getAccountList
    For Each strAcct In acctlist
        cboAccount.AddItem strAcct
    Next

End Sub

