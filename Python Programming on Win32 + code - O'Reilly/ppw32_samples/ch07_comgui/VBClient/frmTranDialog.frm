VERSION 5.00
Object = "{831FDD16-0C5C-11D2-A9FC-0000F8754DA1}#2.0#0"; "MSCOMCTL.OCX"
Object = "{5E9E78A0-531B-11CF-91F6-C2863C385E30}#1.0#0"; "MSFLXGRD.OCX"
Begin VB.Form frmTranDialog 
   BorderStyle     =   3  'Fixed Dialog
   Caption         =   "Editing Transaction"
   ClientHeight    =   4650
   ClientLeft      =   2760
   ClientTop       =   3750
   ClientWidth     =   6135
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   4650
   ScaleWidth      =   6135
   ShowInTaskbar   =   0   'False
   Begin MSComctlLib.StatusBar StatusBar1 
      Align           =   2  'Align Bottom
      Height          =   255
      Left            =   0
      TabIndex        =   15
      Top             =   4395
      Width           =   6135
      _ExtentX        =   10821
      _ExtentY        =   450
      Style           =   1
      _Version        =   393216
      BeginProperty Panels {8E3867A5-8586-11D1-B16A-00C0F0283628} 
         NumPanels       =   1
         BeginProperty Panel1 {8E3867AB-8586-11D1-B16A-00C0F0283628} 
         EndProperty
      EndProperty
   End
   Begin VB.CommandButton cmdDeleteLine 
      Caption         =   "&Delete Line"
      Height          =   375
      Left            =   4200
      TabIndex        =   13
      Top             =   3840
      Width           =   1695
   End
   Begin VB.CommandButton cmdEditLine 
      Caption         =   "&Edit Line"
      Height          =   375
      Left            =   2280
      TabIndex        =   12
      Top             =   3840
      Width           =   1695
   End
   Begin VB.CommandButton cmdAddLine 
      Caption         =   "&Add Line"
      Height          =   375
      Left            =   360
      TabIndex        =   11
      Top             =   3840
      Width           =   1695
   End
   Begin MSFlexGridLib.MSFlexGrid grdItems 
      Height          =   1695
      Left            =   360
      TabIndex        =   10
      Top             =   1680
      Width           =   5535
      _ExtentX        =   9763
      _ExtentY        =   2990
      _Version        =   393216
      Rows            =   4
      FixedCols       =   0
   End
   Begin VB.TextBox txtComment 
      Height          =   285
      Left            =   1800
      TabIndex        =   6
      Text            =   "NONE"
      Top             =   1080
      Width           =   4095
   End
   Begin VB.TextBox txtDate 
      Height          =   285
      Left            =   1800
      TabIndex        =   4
      Text            =   "NONE"
      Top             =   720
      Width           =   1455
   End
   Begin VB.CommandButton CancelButton 
      Caption         =   "Cancel"
      Height          =   375
      Left            =   4680
      TabIndex        =   1
      Top             =   600
      Width           =   1215
   End
   Begin VB.CommandButton OKButton 
      Caption         =   "OK"
      Height          =   375
      Left            =   4680
      TabIndex        =   0
      Top             =   120
      Width           =   1215
   End
   Begin VB.Label lblBalance 
      Alignment       =   1  'Right Justify
      Caption         =   "0.00"
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H000000FF&
      Height          =   255
      Left            =   360
      TabIndex        =   14
      Top             =   3480
      Width           =   5295
   End
   Begin VB.Label Label5 
      Caption         =   "Amount"
      Height          =   255
      Left            =   4920
      TabIndex        =   9
      Top             =   1440
      Width           =   855
   End
   Begin VB.Label Label4 
      Caption         =   "Account"
      Height          =   255
      Left            =   600
      TabIndex        =   8
      Top             =   1440
      Width           =   975
   End
   Begin VB.Label Label3 
      Caption         =   "Comment"
      Height          =   255
      Left            =   360
      TabIndex        =   7
      Top             =   1080
      Width           =   1215
   End
   Begin VB.Label Label2 
      Caption         =   "Date"
      Height          =   255
      Left            =   360
      TabIndex        =   5
      Top             =   720
      Width           =   1215
   End
   Begin VB.Label lblTranIndex 
      Caption         =   "(index)"
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   255
      Left            =   1920
      TabIndex        =   3
      Top             =   240
      Width           =   975
   End
   Begin VB.Label Label1 
      Caption         =   "Transaction no:"
      Height          =   255
      Left            =   360
      TabIndex        =   2
      Top             =   240
      Width           =   1335
   End
End
Attribute VB_Name = "frmTranDialog"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False

Option Explicit
' this form exposes two public methods for handling
' transactions.  It gets its own data from the BookServer
' and posts its own updates there.
Private FormExit As Integer
Private tran As Object   'the transaction being edited


Public Function Edit(index As Integer) As Boolean
    'returns true is the transaction was successfully edited
    Dim i As Integer
    Dim linecount As Integer
    
    Set tran = frmMain.BookServer.getTransaction(index)
    
    'display the transaction details
    lblTranIndex.Caption = Str(index)
    txtDate.text = FormatDateTime(tran.getCOMDate)
    txtComment.text = tran.getComment
    
    linecount = tran.getLineCount
    grdItems.rows = linecount + 1
    For i = 0 To linecount - 1
        grdItems.TextMatrix(i + 1, 0) = tran.GetAccount(i)
        grdItems.TextMatrix(i + 1, 1) = tran.getAmount(i)
    Next i
    Set tran = Nothing
    UpdateFormState
    
    'display and allow editing
    Me.Show vbModal
    
    
    If FormExit = vbOK Then
        Set tran = frmMain.BookServer.CreateTransaction
        tran.setComment txtComment.text
        
        If IsDate(txtDate.text) Then tran.setCOMDate CDbl(CDate(txtDate.text))
        
        For i = 1 To grdItems.rows - 1
            tran.AddLine grdItems.TextMatrix(i, 0), CDbl(grdItems.TextMatrix(i, 1))
        Next i
        frmMain.BookServer.Edit index, tran
        Set tran = Nothing
        Edit = True
    Else
        Edit = False
    End If
    
End Function

Public Function AddNew() As Boolean
    'lets you create and add a new transaction
    'just makes a new one and edits it
    'returns true is the transaction was successfully edited
    Dim i As Integer
    Dim linecount As Integer
    
    lblTranIndex.Caption = "(new transaction)"
    txtDate.text = FormatDateTime(Now)
    txtComment.text = ""
    
    grdItems.rows = 1
    
    UpdateFormState
    'display and allow editing
    Me.Show vbModal
    
    If FormExit = vbOK Then
        'do whatever to save it
        Set tran = frmMain.BookServer.CreateTransaction
        tran.setComment txtComment.text
        
        'if an error in the date format crept through, let Python use its
        'default value of now
        If IsDate(txtDate.text) Then tran.setCOMDate CDbl(CDate(txtDate.text))
        
        For i = 1 To grdItems.rows - 1
            tran.AddLine grdItems.TextMatrix(i, 0), CDbl(grdItems.TextMatrix(i, 1))
        Next i
        
        frmMain.BookServer.Add tran
        AddNew = True
    Else
        AddNew = False
    End If
    
End Function



Private Sub cmdAddLine_Click()
    Dim Account As String
    Dim Amount As Currency
    
    Dim row As Integer
    
    
    If frmLineDialog.AddLine Then
        row = grdItems.rows
        grdItems.rows = row + 1   'add an extra line
        grdItems.TextMatrix(row, 0) = frmLineDialog.Account
        grdItems.TextMatrix(row, 1) = Str(frmLineDialog.Amount)
        UpdateFormState
    End If
End Sub

Private Sub cmdDeleteLine_Click()
    Dim lineno As Integer
    
    lineno = grdItems.row
    If lineno = 0 Then
        MsgBox "A data row in the grid must be selected"
        Exit Sub
    End If
    
    'if not the last line, overwrite with lower data
    While lineno < grdItems.rows - 1
        grdItems.TextMatrix(lineno, 0) = grdItems.TextMatrix(lineno + 1, 0)
        grdItems.TextMatrix(lineno, 1) = grdItems.TextMatrix(lineno + 1, 1)
        lineno = lineno + 1
    Wend
    
    'last line is easy to do...
    grdItems.rows = grdItems.rows - 1
  
    UpdateFormState
End Sub

Private Sub cmdEditLine_Click()
    Dim lineno As Integer
    Dim acct As String
    Dim amt As Currency
    
    lineno = grdItems.row
    If lineno = 0 Then
        MsgBox "A data row in the grid must be selected"
        Exit Sub
    End If
    
    acct = grdItems.TextMatrix(lineno, 0)
    amt = Val(grdItems.TextMatrix(lineno, 1))
    
    If frmLineDialog.EditLine(acct, amt) Then
        grdItems.TextMatrix(lineno, 0) = frmLineDialog.Account
        grdItems.TextMatrix(lineno, 1) = Str(frmLineDialog.Amount)
    End If
    
    UpdateFormState
End Sub

Private Sub Form_Load()
    grdItems.TextMatrix(0, 0) = "Account"
    grdItems.ColAlignment(0) = vbLeftJustify
    grdItems.ColWidth(0) = 2880  '2 inches
    
    grdItems.TextMatrix(0, 1) = "Amount"
    grdItems.ColAlignment(1) = vbRightJustify
    grdItems.ColWidth(1) = 1440  '1 inch
End Sub

Private Sub OKButton_Click()
    FormExit = vbOK
    Hide
End Sub

Private Sub CancelButton_Click()
    FormExit = vbCancel
    Hide
End Sub

Private Sub UpdateFormState()
    'enables/disables buttons while editing, sets the balance label
    'etc.  Includes validation.
    Dim balance As Currency
    Dim valid As Boolean
    Dim i As Integer
    valid = True
    
    'date must be OK
    If Not IsDate(txtDate.text) Then
        valid = False
        StatusBar1.SimpleText = "Invalid Date"
    End If
    
    'comment must be non-null
    If Trim(txtComment.text) = "" Then
        valid = False
        StatusBar1.SimpleText = "Comment must not be blank"
    End If
    
    'balance must be zero
    balance = 0
    For i = 1 To grdItems.rows - 1
        balance = balance + CCur(grdItems.TextMatrix(i, 1))
    Next i
    If balance <> 0 Then
        valid = False
        StatusBar1.SimpleText = "Transaction does not balance"
        End If
    'now take action
    lblBalance.Caption = "Out of balance by " + Str(balance)
    lblBalance.Visible = Not valid
    OKButton.Enabled = valid
 
End Sub
