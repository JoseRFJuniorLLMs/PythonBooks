unit mainunit;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, Menus,

  ComObj, ExtCtrls, Grids;

type
  TfrmMain = class(TForm)
    MainMenu1: TMainMenu;
    File1: TMenuItem;
    Open1: TMenuItem;
    N1: TMenuItem;
    Exit1: TMenuItem;
    PageControl1: TPageControl;
    tabJournal: TTabSheet;
    tabAccount: TTabSheet;
    StatusBar1: TStatusBar;
    lstJournal: TListBox;
    OpenDialog1: TOpenDialog;
    N2: TMenuItem;
    N1DemoData1DTJ1: TMenuItem;
    N2DemoData2DTJ1: TMenuItem;
    pnlAccountLeft: TPanel;
    Label1: TLabel;
    lstAllAccounts: TListBox;
    TabSheet1: TTabSheet;
    grdAccountDetails: TStringGrid;
    lblAccountDetailsCaption: TLabel;
    tabGraphics: TTabSheet;
    Label2: TLabel;
    procedure FormCreate(Sender: TObject);
    procedure Open1Click(Sender: TObject);
    procedure N1DemoData1DTJ1Click(Sender: TObject);
    procedure N2DemoData2DTJ1Click(Sender: TObject);
    procedure lstJournalDrawItem(Control: TWinControl; Index: Integer;
      Rect: TRect; State: TOwnerDrawState);
    procedure lstAllAccountsClick(Sender: TObject);
  private
    { Private declarations }
    SelectedAccount: string;
    procedure UpdateAllViews;
    procedure UpdateJournal;
    procedure UpdateAccountList;
    procedure UpdateAccountDetails;

    procedure doCallbackDemo;
  public
    { Public declarations }
    BookServer: Variant;
  end;

var
  frmMain: TfrmMain;

implementation

{$R *.DFM}


procedure TfrmMain.FormCreate(Sender: TObject);
begin
  try
    BookServer := CreateOleObject('Doubletalk.BookServer');
    StatusBar1.SimpleText := 'BookServer running';
  except
    MessageDlg(
      'An instance of the "Doubletalk.BookServer" COM class ' +
      'could not be created. Make sure that the BookServer application has ' +
      'been registered using a  command line.  If you have modified the ' +
      'source of the server, make very sure all public methods and attributes ' +
      'are spelled correctly',
      mtError, [mbOk], 0);
    Application.Terminate;
  end;
end;

procedure TfrmMain.Open1Click(Sender: TObject);
{prompt for a filename and ask BookSet to load it}
var trancount: integer;
    filename: string;
begin
    if OpenDialog1.Execute then
        begin
        filename := OpenDialog1.FileName;
        BookServer.load(OpenDialog1.FileName);
        trancount := BookServer.Count;
        StatusBar1.SimpleText := Format('Loaded file %s, %d transactions',
                [filename, trancount]
                );
        UpdateAllViews;
        end;
end;

procedure TfrmMain.N1DemoData1DTJ1Click(Sender: TObject);
{unrealistic shortcut that lets users restart it quickly - presumes
we have provided the sample data files in the same directory}
var trancount: integer;
    filename: string;
begin
    filename := 'DemoData1.DTJ';
    BookServer.load(filename);
    trancount := BookServer.Count;
    StatusBar1.SimpleText := Format('Loaded file %s, %d transactions',
                [filename, trancount]
                );
    UpdateAllViews;
end;

procedure TfrmMain.N2DemoData2DTJ1Click(Sender: TObject);
{unrealistic shortcut that lets users restart it quickly - presumes
we have provided the sample data files in the same directory}
var trancount: integer;
    filename: string;
begin
    filename := 'DemoData2.DTJ';
    BookServer.load(filename);
    trancount := BookServer.Count;
    StatusBar1.SimpleText := Format('Loaded file %s, %d transactions',
                [filename, trancount]
                );
    UpdateAllViews;
end;

procedure TfrmMain.UpdateAllViews;
begin
    Screen.Cursor := crHourglass;

    UpdateJournal;
    UpdateAccountList;
    UpdateAccountDetails;
    
    Screen.Cursor := crDefault;
end;

procedure TfrmMain.UpdateJournal;
{We've used a useful feature of Delphi's list boxes whereby
they defer asking for the actual string until they need to display it.
We put any old string in the list box, such as a text representation of
the index; then the VCL calls the method below to get the text for each
item as it becomes visible.  This saves a huge amount of time displaying
big lists.}
var i: integer;
begin
    lstJournal.Clear;
    for i := 0 to BookServer.Count - 1 do
        begin
        lstJournal.Items.Add(IntToStr(i))
        end;
end;

procedure TfrmMain.lstJournalDrawItem(Control: TWinControl; Index: Integer;
  Rect: TRect; State: TOwnerDrawState);
var tran: Variant;
begin
  tran := BookServer.getTransaction(Index);
  with (Control as TListBox).Canvas do
    TextOut(Rect.Left, Rect.Top, tran.getOneLineDescription);
end;

procedure TfrmMain.UpdateAccountList;
var AccountList: Variant;
    i: integer;
begin
    lstAllAccounts.Items.Clear;
    AccountList := BookServer.GetAccountList;
    for i := 0 to VarArrayHighBound(AccountList, 1) do
        lstAllAccounts.Items.Add(AccountList[i]);
end;

procedure TfrmMain.UpdateAccountDetails;
var data: Variant;
    datarows: integer;
    row, col: integer;
begin
    //set up grid titles - could be in FormCreate, but this keeps it
    //together
    grdAccountDetails.Cells[0, 0] := 'Index';
    grdAccountDetails.Cells[1, 0] := 'Date';
    grdAccountDetails.Cells[2, 0] := 'Comment';
    grdAccountDetails.Cells[3, 0] := 'Change';
    grdAccountDetails.Cells[4, 0] := 'Balance';

    lblAccountDetailsCaption.Caption := SelectedAccount;

    data := BookServer.getAccountDetails(SelectedAccount);
    datarows := VarArrayHighBound(data, 1);

    if datarows = 0 then
        //If we want the titles visible in grey, must have at least one
        //extra non-fixed row in the grid.
        begin
        grdAccountDetails.RowCount := 2;
        for col := 0 to 4 do grdAccountDetails.Cells[col, 1] := '';
        end
    else
        begin  //we have data
        grdAccountDetails.RowCount := datarows + 1;
        for row := 0 to datarows - 1 do
            {we could be lazy and do...
            for col := 0 to 4 do
                grdAccountDetails.Cells[col, row] := data[row, col];
            ... letting Delphi coerce each variant to a string,
            but it is nicer to control the formatting of each column}
            begin
            grdAccountDetails.Cells[0, row+1] := IntToStr(data[row, 0]); //index
            grdAccountDetails.Cells[1, row+1] := data[row, 1]; //date
            grdAccountDetails.Cells[2, row+1] := data[row, 2]; //date
            grdAccountDetails.Cells[3, row+1] := FormatFloat('#,##0.00', data[row, 3]); //change
            grdAccountDetails.Cells[4, row+1] := FormatFloat('#,##0.00', data[row, 4]); //change
            end;
        //end for row
        end;
    //end if
end;



procedure TfrmMain.lstAllAccountsClick(Sender: TObject);
begin
    SelectedAccount := lstAllAccounts.Items[lstAllAccounts.ItemIndex];
    //Update the views which relate to just this account;
    UpdateAccountDetails;
end;

procedure TfrmMain.doCallbackDemo;
begin
    {this just does not work:
    BookServer.doDelphiCallbackDemo(Self);
    }
end;



end.
