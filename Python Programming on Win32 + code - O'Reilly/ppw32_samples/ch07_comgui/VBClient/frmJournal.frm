VERSION 5.00
Begin VB.Form frmJournal 
   Caption         =   "frmJournal"
   ClientHeight    =   3465
   ClientLeft      =   60
   ClientTop       =   345
   ClientWidth     =   5070
   LinkTopic       =   "Form1"
   MDIChild        =   -1  'True
   ScaleHeight     =   3465
   ScaleWidth      =   5070
   Begin VB.ListBox lstJournal 
      Height          =   2790
      Left            =   120
      TabIndex        =   0
      Top             =   120
      Width           =   4455
   End
End
Attribute VB_Name = "frmJournal"
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
    lstJournal.Move 40, 40, Me.ScaleWidth - 80, Me.ScaleHeight - 80
End Sub

Public Sub UpdateView()
    'make a list with a string describing each transaction
    
    Dim count, i As Integer
    Dim trantext As String
    Dim tran As Object
    
    Screen.MousePointer = vbHourglass
    lstJournal.Clear
    
    For i = 0 To frmMain.BookServer.count - 1
        trantext = frmMain.BookServer.getOneLineDescription(i)
        lstJournal.AddItem trantext
    Next i
    
    Screen.MousePointer = vbDefault
    Caption = "Journal view - " & lstJournal.ListCount & " transactions"
    
End Sub


Private Sub lstJournal_DblClick()
    'trigger an Edit
    If frmTranDialog.Edit(lstJournal.ListIndex) Then UpdateView
End Sub

