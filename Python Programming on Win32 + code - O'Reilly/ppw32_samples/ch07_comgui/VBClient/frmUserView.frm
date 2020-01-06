VERSION 5.00
Object = "{5E9E78A0-531B-11CF-91F6-C2863C385E30}#1.0#0"; "MSFLXGRD.OCX"
Begin VB.Form frmUserView 
   Caption         =   "User Defined View"
   ClientHeight    =   3195
   ClientLeft      =   60
   ClientTop       =   345
   ClientWidth     =   4680
   LinkTopic       =   "Form1"
   MDIChild        =   -1  'True
   ScaleHeight     =   3195
   ScaleWidth      =   4680
   Begin MSFlexGridLib.MSFlexGrid grdData 
      Height          =   2895
      Left            =   120
      TabIndex        =   0
      Top             =   120
      Width           =   4335
      _ExtentX        =   7646
      _ExtentY        =   5106
      _Version        =   393216
      FixedRows       =   0
      FixedCols       =   0
   End
End
Attribute VB_Name = "frmUserView"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit
'supports user-defined BookSet views
Public ViewName As String

Private Sub Form_Resize()
    On Error Resume Next
    grdData.Move 40, 40, Me.ScaleWidth - 80, Me.ScaleHeight - 80
End Sub

Public Sub UpdateView()
    Dim table As Variant
    Dim rows As Integer, cols As Integer
    Dim row As Integer, col As Integer
    
    Caption = "User Defined View - " & ViewName
    table = frmMain.BookServer.getViewData(ViewName)
    
    rows = UBound(table, 1) - LBound(table, 1) + 1
    grdData.rows = rows
        
    If rows = 0 Then Exit Sub
    cols = UBound(table, 2) - LBound(table, 2) + 1
    grdData.cols = cols
    
    For row = 0 To rows - 1
        For col = 0 To cols - 1
            grdData.TextMatrix(row, col) = table(row, col)
        Next col
    Next row
End Sub


