VERSION 5.00
Object = "{F9043C88-F6F2-101A-A3C9-08002B2F49FB}#1.2#0"; "COMDLG32.OCX"
Object = "{3B7C8863-D78F-101B-B9B5-04021C009402}#1.2#0"; "RICHTX32.OCX"
Begin VB.Form frmScriptEditor 
   Caption         =   "Script Editor"
   ClientHeight    =   3660
   ClientLeft      =   165
   ClientTop       =   450
   ClientWidth     =   4665
   LinkTopic       =   "Form1"
   MDIChild        =   -1  'True
   ScaleHeight     =   3660
   ScaleWidth      =   4665
   Begin MSComDlg.CommonDialog CommonDialog1 
      Left            =   3600
      Top             =   0
      _ExtentX        =   847
      _ExtentY        =   847
      _Version        =   393216
      Filter          =   "Python script (*.py) | *.py"
   End
   Begin RichTextLib.RichTextBox rtfEditor 
      Height          =   3255
      Left            =   0
      TabIndex        =   0
      Top             =   240
      Width           =   4335
      _ExtentX        =   7646
      _ExtentY        =   5741
      _Version        =   393217
      BackColor       =   16777215
      Enabled         =   -1  'True
      TextRTF         =   $"frmScriptEditor.frx":0000
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "Courier New"
         Size            =   9.75
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
   End
   Begin VB.Menu mnuScript 
      Caption         =   "&Script"
      NegotiatePosition=   2  'Middle
      Begin VB.Menu mnuScriptOpen 
         Caption         =   "&Open"
      End
      Begin VB.Menu mnuScriptSave 
         Caption         =   "&Save"
      End
      Begin VB.Menu mnuScriptSaveAs 
         Caption         =   "Save &As..."
      End
      Begin VB.Menu mnuScriptBar0 
         Caption         =   "-"
      End
      Begin VB.Menu mnuScriptRun 
         Caption         =   "&Run"
      End
      Begin VB.Menu mnuScriptImport 
         Caption         =   "&Import"
      End
   End
End
Attribute VB_Name = "frmScriptEditor"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit
Private FileName As String
Private Saved As Boolean


Private Sub Form_Resize()
    On Error Resume Next
    rtfEditor.Move 40, 40, Me.ScaleWidth - 80, Me.ScaleHeight - 80
End Sub


Private Sub mnuScriptOpen_Click()
    CommonDialog1.FileName = ""
    CommonDialog1.ShowOpen
    If Len(CommonDialog1.FileName) > 0 Then
        FileName = CommonDialog1.FileName
        rtfEditor.LoadFile FileName, rtfText
        Caption = "Script - " + FileName
        Saved = True
    End If
    
End Sub


Private Sub mnuScriptSave_Click()
    If FileName = "" Then
        mnuScriptSaveAs_Click
    Else
        rtfEditor.SaveFile FileName, rtfText
        Saved = True
    End If
End Sub

Private Sub mnuScriptSaveAs_Click()
    CommonDialog1.FileName = FileName
    CommonDialog1.ShowSave
    If Len(CommonDialog1.FileName) > 0 Then
        FileName = CommonDialog1.FileName
        Caption = "Script - " + FileName
        rtfEditor.SaveFile FileName, rtfText
        Saved = True
    End If
End Sub


Private Sub rtfEditor_Change()
    Saved = False
End Sub

Private Sub mnuScriptRun_Click()
    mnuScriptSave_Click
    If Saved Then
        On Error GoTo mnuScriptRun_Error
        frmMain.BookServer.execFile FileName
        On Error GoTo 0
        frmConsole.UpdateOutput
    End If
    Exit Sub
    
mnuScriptRun_Error:
    MsgBox "Error running script:" + vbCrLf + vbCrLf + Err.Description
End Sub


Private Sub mnuScriptImport_Click()
    mnuScriptSave_Click
    If Saved Then
        On Error GoTo mnuScriptImport_Error
        frmMain.BookServer.importFile FileName
        On Error GoTo 0
        frmConsole.UpdateOutput
    Else
        Exit Sub
    End If
    
mnuScriptImport_Error:
    MsgBox "Error importing script:" + vbCrLf + vbCrLf + Err.Description
End Sub

