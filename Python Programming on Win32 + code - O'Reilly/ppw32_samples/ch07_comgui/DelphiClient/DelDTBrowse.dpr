program DelDTBrowse;

uses
  Forms,
  MainUnit in 'MainUnit.pas' {frmMain};

{$R *.RES}

begin
  Application.Initialize;
  Application.CreateForm(TfrmMain, frmMain);
  Application.Run;
end.
