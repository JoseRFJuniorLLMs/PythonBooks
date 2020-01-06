VERSION 5.00
Object = "{F9043C88-F6F2-101A-A3C9-08002B2F49FB}#1.2#0"; "COMDLG32.OCX"
Object = "{831FDD16-0C5C-11D2-A9FC-0000F8754DA1}#2.0#0"; "MSCOMCTL.OCX"
Begin VB.Form frmOptions 
   BorderStyle     =   3  'Fixed Dialog
   Caption         =   "Options"
   ClientHeight    =   4080
   ClientLeft      =   45
   ClientTop       =   330
   ClientWidth     =   6150
   KeyPreview      =   -1  'True
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   4080
   ScaleWidth      =   6150
   ShowInTaskbar   =   0   'False
   StartUpPosition =   1  'CenterOwner
   Tag             =   "Options"
   Begin MSComDlg.CommonDialog CommonDialog1 
      Left            =   0
      Top             =   3600
      _ExtentX        =   847
      _ExtentY        =   847
      _Version        =   393216
      Filter          =   "Python Scripts (*.py) | *.py | Compiled Python Scripts (*.pyc) | *.pyc"
   End
   Begin VB.CommandButton cmdOK 
      Caption         =   "OK"
      Height          =   375
      Left            =   2490
      TabIndex        =   1
      Tag             =   "OK"
      Top             =   3615
      Width           =   1095
   End
   Begin VB.CommandButton cmdCancel 
      Cancel          =   -1  'True
      Caption         =   "Cancel"
      Height          =   375
      Left            =   3720
      TabIndex        =   3
      Tag             =   "Cancel"
      Top             =   3615
      Width           =   1095
   End
   Begin VB.CommandButton cmdApply 
      Caption         =   "&Apply"
      Height          =   375
      Left            =   4920
      TabIndex        =   4
      Tag             =   "&Apply"
      Top             =   3615
      Width           =   1095
   End
   Begin VB.PictureBox picOptions 
      BorderStyle     =   0  'None
      Height          =   3780
      Index           =   3
      Left            =   -20000
      ScaleHeight     =   3840.968
      ScaleMode       =   0  'User
      ScaleWidth      =   5745.64
      TabIndex        =   6
      TabStop         =   0   'False
      Top             =   480
      Width           =   5685
      Begin VB.Frame fraSample4 
         Caption         =   "Sample 4"
         Height          =   2022
         Left            =   505
         TabIndex        =   10
         Tag             =   "Sample 4"
         Top             =   502
         Width           =   2033
      End
   End
   Begin VB.PictureBox picOptions 
      BorderStyle     =   0  'None
      Height          =   3780
      Index           =   2
      Left            =   -20000
      ScaleHeight     =   3840.968
      ScaleMode       =   0  'User
      ScaleWidth      =   5745.64
      TabIndex        =   8
      TabStop         =   0   'False
      Top             =   480
      Width           =   5685
      Begin VB.Frame fraSample3 
         Caption         =   "Sample 3"
         Height          =   2022
         Left            =   406
         TabIndex        =   9
         Tag             =   "Sample 3"
         Top             =   403
         Width           =   2033
      End
   End
   Begin VB.PictureBox picOptions 
      BorderStyle     =   0  'None
      Height          =   3780
      Index           =   1
      Left            =   -20000
      ScaleHeight     =   3840.968
      ScaleMode       =   0  'User
      ScaleWidth      =   5745.64
      TabIndex        =   5
      TabStop         =   0   'False
      Top             =   480
      Width           =   5685
      Begin VB.Frame fraSample2 
         Caption         =   "Sample 2"
         Height          =   2022
         Left            =   307
         TabIndex        =   7
         Tag             =   "Sample 2"
         Top             =   305
         Width           =   2033
      End
   End
   Begin VB.PictureBox picOptions 
      BorderStyle     =   0  'None
      Height          =   2820
      Index           =   0
      Left            =   210
      ScaleHeight     =   2865.484
      ScaleMode       =   0  'User
      ScaleWidth      =   5745.64
      TabIndex        =   2
      TabStop         =   0   'False
      Top             =   480
      Width           =   5685
      Begin VB.TextBox txtRemoteMachine 
         Height          =   375
         Left            =   120
         TabIndex        =   15
         Top             =   1320
         Width           =   3975
      End
      Begin VB.CommandButton cmdReload 
         Caption         =   "Reload BookServer Now"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   375
         Left            =   240
         TabIndex        =   14
         Top             =   2160
         Width           =   3855
      End
      Begin VB.CommandButton cmdBrowse 
         Caption         =   "&Browse"
         Height          =   375
         Left            =   4080
         TabIndex        =   13
         Top             =   480
         Width           =   1575
      End
      Begin VB.TextBox txtStartupScript 
         Height          =   375
         Left            =   120
         TabIndex        =   12
         Top             =   480
         Width           =   3975
      End
      Begin VB.Label Label2 
         Caption         =   "Remote Server (leave empty for local machine)"
         Height          =   255
         Left            =   120
         TabIndex        =   16
         Top             =   1080
         Width           =   3975
      End
      Begin VB.Label Label1 
         Caption         =   "&Startup Script"
         Height          =   255
         Left            =   120
         TabIndex        =   11
         Top             =   240
         Width           =   1215
      End
   End
   Begin MSComctlLib.TabStrip tbsOptions 
      Height          =   3405
      Left            =   105
      TabIndex        =   0
      Top             =   120
      Width           =   5895
      _ExtentX        =   10398
      _ExtentY        =   6006
      _Version        =   393216
      BeginProperty Tabs {1EFB6598-857C-11D1-B16A-00C0F0283628} 
         NumTabs         =   4
         BeginProperty Tab1 {1EFB659A-857C-11D1-B16A-00C0F0283628} 
            Caption         =   "Startup"
            ImageVarType    =   2
         EndProperty
         BeginProperty Tab2 {1EFB659A-857C-11D1-B16A-00C0F0283628} 
            Caption         =   "Remote"
            Object.ToolTipText     =   "Remote Server Settings"
            ImageVarType    =   2
         EndProperty
         BeginProperty Tab3 {1EFB659A-857C-11D1-B16A-00C0F0283628} 
            Caption         =   "Group 3"
            ImageVarType    =   2
         EndProperty
         BeginProperty Tab4 {1EFB659A-857C-11D1-B16A-00C0F0283628} 
            Caption         =   "Group 4"
            ImageVarType    =   2
         EndProperty
      EndProperty
   End
End
Attribute VB_Name = "frmOptions"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Private Sub cmdApply_Click()
    'ToDo: Add 'cmdApply_Click' code.
    frmMain.RemoteMachine = Trim(txtRemoteMachine.text)
    
End Sub


Private Sub cmdBrowse_Click()
    CommonDialog1.ShowOpen
    If CommonDialog1.FileName <> "" Then
        txtStartupScript.text = CommonDialog1.FileName
    End If
End Sub

Private Sub cmdCancel_Click()
    Hide
End Sub


Private Sub cmdOK_Click()
    'ToDo: Add 'cmdOK_Click' code.
    frmMain.RemoteMachine = Trim(txtRemoteMachine.text)
    Hide
End Sub




Private Sub cmdReload_Click()
    Dim Proceed As Boolean
    If frmMain.BookServer.count > 0 Then
        If MsgBox("You have data in the BookServer which will be lost.  Proceed?", vbOKCancel, "Warning") = vbCancel Then
            Exit Sub
        End If
    End If
    frmConsole.Clear
    frmMain.CloseCOMServer
    frmMain.InitCOMServer  'this calls the script
    frmMain.UpdateAllViews
    Beep
    
End Sub

Private Sub Form_KeyDown(KeyCode As Integer, Shift As Integer)
    Dim i As Integer
    i = tbsOptions.SelectedItem.index
    'handle ctrl+tab to move to the next tab
    If (Shift And 3) = 2 And KeyCode = vbKeyTab Then
        If i = tbsOptions.Tabs.count Then
            'last tab so we need to wrap to tab 1
            Set tbsOptions.SelectedItem = tbsOptions.Tabs(1)
        Else
            'increment the tab
            Set tbsOptions.SelectedItem = tbsOptions.Tabs(i + 1)
        End If
    ElseIf (Shift And 3) = 3 And KeyCode = vbKeyTab Then
        If i = 1 Then
            'last tab so we need to wrap to tab 1
            Set tbsOptions.SelectedItem = tbsOptions.Tabs(tbsOptions.Tabs.count)
        Else
            'increment the tab
            Set tbsOptions.SelectedItem = tbsOptions.Tabs(i - 1)
        End If
    End If
End Sub


Private Sub tbsOptions_Click()
    

    Dim i As Integer
    'show and enable the selected tab's controls
    'and hide and disable all others
    For i = 0 To tbsOptions.Tabs.count - 1
        If i = tbsOptions.SelectedItem.index - 1 Then
            picOptions(i).Left = 210
            picOptions(i).Enabled = True
        Else
            picOptions(i).Left = -20000
            picOptions(i).Enabled = False
        End If
    Next
    

End Sub

