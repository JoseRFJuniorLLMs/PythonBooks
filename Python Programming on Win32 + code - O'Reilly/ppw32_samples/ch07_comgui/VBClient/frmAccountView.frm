VERSION 5.00
Object = "{5E9E78A0-531B-11CF-91F6-C2863C385E30}#1.0#0"; "MSFLXGRD.OCX"
Begin VB.Form frmAccountView 
   Caption         =   "Account View"
   ClientHeight    =   3195
   ClientLeft      =   60
   ClientTop       =   345
   ClientWidth     =   4680
   LinkTopic       =   "Form1"
   MDIChild        =   -1  'True
   ScaleHeight     =   3195
   ScaleWidth      =   4680
   Begin MSFlexGridLib.MSFlexGrid grdTable 
      Height          =   2775
      Left            =   240
      TabIndex        =   0
      Top             =   240
      Width           =   4335
      _ExtentX        =   7646
      _ExtentY        =   4895
      _Version        =   393216
   End
End
Attribute VB_Name = "frmAccountView"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit
'Implements UpdatableView

Private AccountName As String

Private Sub Form_Load()
    ' set up the grid labels and widths
    grdTable.cols = 5
    grdTable.rows = 2
    grdTable.FixedRows = 1
    grdTable.FixedCols = 0
    
    grdTable.TextMatrix(0, 0) = "Index"
    grdTable.TextMatrix(0, 1) = "Date"
    grdTable.TextMatrix(0, 2) = "Comment"
    grdTable.TextMatrix(0, 3) = "Amount"
    grdTable.TextMatrix(0, 4) = "Balance"
    
    grdTable.ColWidth(2) = 2880
    Form_Resize
End Sub

Private Sub Form_Resize()
    On Error Resume Next
    grdTable.Move 40, 40, Me.ScaleWidth - 80, Me.ScaleHeight - 80
End Sub

Public Sub SetAccount(acname As String)
    AccountName = acname
    Caption = "Details of account " & AccountName
    UpdateView
End Sub
Public Sub UpdateView() 'This is mnade public by the updatableView class
    Dim table As Variant
    Dim rows As Integer, cols As Integer
    Dim row As Integer, col As Integer
    
    table = frmMain.BookServer.getAccountDetails(AccountName)
    
    rows = UBound(table, 1) - LBound(table, 1) + 1
    grdTable.rows = rows + 1 'leave one for titles
        
    If rows = 0 Then Exit Sub
    
    cols = UBound(table, 2) - LBound(table, 2) + 1 'should be 5
    
    For row = 0 To rows - 1
        For col = 0 To cols - 1
            grdTable.TextMatrix(row + 1, col) = table(row, col)
        Next col
    Next row
End Sub
