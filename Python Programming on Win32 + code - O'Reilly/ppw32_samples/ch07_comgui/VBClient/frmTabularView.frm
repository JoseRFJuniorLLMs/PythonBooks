VERSION 5.00
Object = "{5E9E78A0-531B-11CF-91F6-C2863C385E30}#1.0#0"; "MSFLXGRD.OCX"
Begin VB.Form frmTabularView 
   Caption         =   "frmTabularView"
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
Attribute VB_Name = "frmTabularView"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit
'generic viewer for arrays of data

Private Sub Form_Resize()
    On Error Resume Next
    grdTable.Move 40, 40, Me.ScaleWidth - 80, Me.ScaleHeight - 80
End Sub

