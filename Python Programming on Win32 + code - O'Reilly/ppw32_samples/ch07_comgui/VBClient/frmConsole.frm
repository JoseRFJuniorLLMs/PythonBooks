VERSION 5.00
Begin VB.Form frmConsole 
   Caption         =   "Python Console"
   ClientHeight    =   4065
   ClientLeft      =   60
   ClientTop       =   345
   ClientWidth     =   4905
   LinkTopic       =   "Form1"
   MDIChild        =   -1  'True
   ScaleHeight     =   4065
   ScaleWidth      =   4905
   Begin VB.TextBox txtInput 
      BeginProperty Font 
         Name            =   "Courier New"
         Size            =   9.75
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   1215
      Left            =   120
      MultiLine       =   -1  'True
      TabIndex        =   0
      Top             =   360
      Width           =   4695
   End
   Begin VB.TextBox txtOutput 
      BeginProperty Font 
         Name            =   "Courier New"
         Size            =   9.75
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   2055
      Left            =   120
      Locked          =   -1  'True
      MultiLine       =   -1  'True
      ScrollBars      =   2  'Vertical
      TabIndex        =   1
      Top             =   1920
      Width           =   4695
   End
   Begin VB.Label Label2 
      Caption         =   "Input (Press F5 to execute):"
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
      Left            =   120
      TabIndex        =   3
      Top             =   0
      Width           =   4455
   End
   Begin VB.Label Label1 
      Caption         =   "Python Console Output"
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
      Left            =   120
      TabIndex        =   2
      Top             =   1680
      Width           =   2415
   End
End
Attribute VB_Name = "frmConsole"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit
'a crude but usable Python console


Private Sub Form_QueryUnload(Cancel As Integer, UnloadMode As Integer)
    ' trap the user clicking the close box; do not trap
    ' the whole application closing
    ' ensure it is just hidden; update the menu item state
    If UnloadMode = vbFormControlMenu Then
        Cancel = True
        Hide
        frmMain.mnuViewConsole.Checked = False
    End If
End Sub


Private Sub Form_Resize()
    'the measurements were taken at design time
    txtInput.Width = ScaleWidth - 210
    txtOutput.Width = ScaleWidth - 210
    If ScaleHeight > 2965 Then
        txtOutput.Height = ScaleHeight - 2010
    Else
        txtOutput.Height = 1000  'have a sensible minimum
    End If
End Sub

Function ProcessPythonCode(expr As String) As String
    'passes a chunk of text to the server's interpretString
    'method, and returns the result.  If an error occurs,
    'returns the error message.
    
    On Error GoTo mnuProcessPythonCode_Error
    ProcessPythonCode = frmMain.BookServer.interpretString(expr)
    Exit Function

mnuProcessPythonCode_Error:
    ProcessPythonCode = Err.Description
End Function

Sub ProcessCommand()
    'gets a one-line string from the input text box.
    'if there is a result, appends it to the output box.
    'Also copy the input command to output to keep a command history
    Dim strInput As String
    Dim strResult As String
    Dim strStandardOutput As String
    Dim strOutText As String  'for building the final textbox data
    
    'VB puts CRLF pairs in the input for multi-line
    'statements; Python just wants line feeds
    strInput = Replace(txtInput.text, vbCrLf, vbLf)
    
    'multi-line statements need a final line-feed; this is optional
    'fopr one liners.  WE'll add it anyway.
    If Right(strInput, 1) <> vbLf Then strInput = strInput + vbLf
           
    'process it
    strResult = ProcessPythonCode(strInput)
    
    'see if there is any standard output.  If so, make sure
    'we have proper VB newlines
    strStandardOutput = frmMain.BookServer.getStandardOutput()
    strStandardOutput = Replace(strStandardOutput, vbLf, vbCrLf)
    
    

    'insert at end
    strOutText = txtOutput.text + _
            ">>>" + Replace(txtInput.text, vbCrLf, vbCrLf + "...")
    If Right(strOutText, 2) <> vbCrLf Then strOutText = strOutText + vbCrLf
    
    strOutText = strOutText + strStandardOutput + strResult
    If Right(strOutText, 2) <> vbCrLf Then strOutText = strOutText + vbCrLf
    
    txtOutput.text = strOutText
            
    'move selection to end to ensure it is all visible
    txtOutput.SelStart = Len(txtOutput.text)
    
    'ditch the input and reset focus for the next command
    txtInput.text = ""
    txtInput.SetFocus
    
    
End Sub


Public Sub UpdateOutput()
    'other forms can call this when there may be more output to grab
    Dim strOutput As String
    strOutput = frmMain.BookServer.getStandardOutput()
    strOutput = Replace(strOutput, vbLf, vbCrLf)
    If Right(txtOutput.text, 2) = vbCrLf Then
        txtOutput.text = txtOutput.text + strOutput
    Else
        txtOutput.text = txtOutput.text + vbCrLf + strOutput
    End If
    
End Sub

Public Sub Clear()
    txtOutput.text = ""
End Sub
Private Sub txtInput_KeyUp(KeyCode As Integer, Shift As Integer)
    If KeyCode = vbKeyF5 Then ProcessCommand
End Sub

