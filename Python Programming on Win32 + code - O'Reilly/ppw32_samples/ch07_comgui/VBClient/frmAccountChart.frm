VERSION 5.00
Begin VB.Form frmAccountChart 
   Caption         =   "Account Chart"
   ClientHeight    =   3195
   ClientLeft      =   60
   ClientTop       =   345
   ClientWidth     =   4680
   LinkTopic       =   "Form1"
   MDIChild        =   -1  'True
   ScaleHeight     =   3195
   ScaleWidth      =   4680
   Begin VB.CommandButton cmdDemo 
      Caption         =   "&Demo"
      Height          =   375
      Left            =   3000
      TabIndex        =   1
      Top             =   2760
      Visible         =   0   'False
      Width           =   1335
   End
   Begin VB.PictureBox picChart 
      AutoRedraw      =   -1  'True
      Height          =   2535
      Left            =   120
      ScaleHeight     =   2475
      ScaleWidth      =   4395
      TabIndex        =   0
      Top             =   120
      Width           =   4455
   End
End
Attribute VB_Name = "frmAccountChart"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit
'frmAccountChart - exposes an API to allow Python to draw on it

Private AccountName As String

Private Sub cmdDemo_Click()
    'this just proves that our graphics API works...
    Me.DrawLine 100, 100, 100, 1000, RGB(0, 0, 255)
    Me.DrawLine 100, 1000, 1000, 1000, RGB(0, 0, 255)
    Me.DrawLine 1000, 1000, 100, 100, RGB(0, 0, 255)
    
    Me.DrawBox 100, 1200, 900, 1800, RGB(255, 0, 0), 0 'red border, black fill
    Me.DrawBox 1100, 1200, 1900, 1800, RGB(255, 0, 0), RGB(0, 255, 0) 'solid green box, red border
    
    Me.DrawText 1100, 400, 12, "Demo of minimal Graphics API" '12 point text
    
    'test the variant array passing
    Dim area As Variant, msg As String
    area = Me.GetClientArea  'gets a 2-element variant array
    msg = "Window Size: " & area(0) & "x" & area(1)
    Me.DrawText 1100, 800, 12, msg
    
End Sub

Private Sub Form_Load()
    Form_Resize
End Sub
Private Sub Form_Resize()
    On Error Resume Next
    picChart.Move 40, 40, Me.ScaleWidth - 80, Me.ScaleHeight - 80
    UpdateView  'this one needs redrawing when resized
End Sub
Public Sub SetAccount(acname As String)
    AccountName = acname
    Caption = "Chart of account " & AccountName
    UpdateView
End Sub

Public Sub UpdateView()
    'ask Python to scribble on me
    frmMain.BookServer.drawAccountChart Me
End Sub

Public Function GetAccount() As String
    GetAccount = AccountName
End Function

Public Function GetClientArea() As Variant
    'return a 2-element variant array
    GetClientArea = Array(picChart.Width, picChart.Height)
End Function

Public Sub ClearChart()
    picChart.Cls
End Sub
Public Sub DrawLine(x1 As Integer, y1 As Integer, x2 As Integer, y2 As Integer, _
                    color As Long)
    picChart.FillStyle = vbTransparent
    picChart.Line (x1, y1)-(x2, y2), color
    
End Sub
Public Sub DrawBox(x1 As Integer, y1 As Integer, x2 As Integer, y2 As Integer, _
                    lineColor As Long, fillColor As Long)
    picChart.FillStyle = vbSolid
    picChart.fillColor = fillColor
    picChart.Line (x1, y1)-(x2, y2), lineColor, B
End Sub


Public Sub DrawText(x As Integer, y As Integer, size As Integer, text As String)
    picChart.CurrentX = x
    picChart.CurrentY = y
    picChart.FontSize = size
    picChart.Print text
End Sub


