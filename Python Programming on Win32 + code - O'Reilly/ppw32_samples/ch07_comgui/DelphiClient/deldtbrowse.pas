unit mainunit;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, Menus,

  ComObj;

type
  TfrmMain = class(TForm)
    MainMenu1: TMainMenu;
    File1: TMenuItem;
    Open1: TMenuItem;
    N1: TMenuItem;
    Exit1: TMenuItem;
    PageControl1: TPageControl;
    tabJournal: TTabSheet;
    TabSheet2: TTabSheet;
    StatusBar1: TStatusBar;
    lstJournal: TListBox;
    procedure FormCreate(Sender: TObject);
  private
    { Private declarations }
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
    //UpdateView(Self);
    //ListBox1.Enabled := True;
    //cmdAdd.Enabled := True;
    //cmdEdit.Enabled := True;
    //cmdDelete.Enabled := True;
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

end.
