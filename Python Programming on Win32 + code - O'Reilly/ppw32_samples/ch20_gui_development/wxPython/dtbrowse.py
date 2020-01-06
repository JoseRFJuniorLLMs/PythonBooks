
from wxPython.wx import *
from doubletalk.bookset import BookSet

from dtjournal import JournalView
from dtedittrans import EditTransDlg

import time


#----------------------------------------------------------------------

ID_OPEN   = 101
ID_CLOSE  = 102
ID_EXIT   = 103
ID_ABOUT  = 104
ID_SAVE   = 105
ID_ADD    = 106
ID_EDIT   = 107
ID_JRNL   = 108
ID_DTAIL  = 109
ID_SAVEAS = 110


class MainFrame(wxMDIParentFrame):
    title = "Doubletalk Browser - wxPython Edition"
    def __init__(self, parent):
        wxMDIParentFrame.__init__(self, parent, -1, self.title)
        self.bookset = None
        self.views = []

        if wxPlatform == '__WXMSW__':
            self.icon = wxIcon('chart7.ico', wxBITMAP_TYPE_ICO)
            self.SetIcon(self.icon)

        # create a statusbar that shows the time and date on the right
        sb = self.CreateStatusBar(2)
        sb.SetStatusWidths([-1, 150])
        self.timer = wxPyTimer(self.Notify)
        self.timer.Start(1000)
        self.Notify()

        menu = self.MakeMenu(false)
        self.SetMenuBar(menu)
        menu.EnableTop(1, false)

        EVT_MENU(self, ID_OPEN,  self.OnMenuOpen)
        EVT_MENU(self, ID_CLOSE, self.OnMenuClose)
        EVT_MENU(self, ID_SAVE,  self.OnMenuSave)
        EVT_MENU(self, ID_SAVEAS,self.OnMenuSaveAs)
        EVT_MENU(self, ID_EXIT,  self.OnMenuExit)
        EVT_MENU(self, ID_ABOUT, self.OnMenuAbout)
        EVT_MENU(self, ID_ADD,   self.OnAddTrans)
        EVT_MENU(self, ID_JRNL,  self.OnViewJournal)
        EVT_MENU(self, ID_DTAIL, self.OnViewDetail)

        EVT_CLOSE(self, self.OnCloseWindow)


    def MakeMenu(self, withEdit):
        fmenu = wxMenu()
        fmenu.Append(ID_OPEN,  "&Open BookSet",  "Open a BookSet file")
        fmenu.Append(ID_CLOSE, "&Close BookSet",
                     "Close the current BookSet")
        fmenu.Append(ID_SAVE,  "&Save", "Save the current BookSet")
        fmenu.Append(ID_SAVEAS,  "Save &As", "Save the current BookSet")
        fmenu.AppendSeparator()
        fmenu.Append(ID_EXIT, "E&xit",   "Terminate the program")

        dtmenu = wxMenu()
        dtmenu.Append(ID_ADD, "&Add Transaction",
                      "Add a new transaction")
        if withEdit:
            dtmenu.Append(ID_EDIT, "&Edit Transaction",
                          "Edit selected transaction in current view")
        dtmenu.Append(ID_JRNL, "&Journal view",
                      "Open or raise the journal view")
        dtmenu.Append(ID_DTAIL,"&Detail view",
                      "Open or raise the detail view")

        hmenu = wxMenu()
        hmenu.Append(ID_ABOUT, "&About",
                     "More information about this program")

        main = wxMenuBar()
        main.Append(fmenu, "&File")
        main.Append(dtmenu,"&Bookset")
        main.Append(hmenu, "&Help")

        return main


    def UpdateViews(self):
        for view in self.views:
            view[0].UpdateView()

    def CloseView(self, aView):
        for x in range(len(self.views)):
            view = self.views[x][0]
            if view == aView:
                del self.views[x]
                return

    def OnMenuOpen(self, event):
        # This should be checking if another is already open,
        # but is left as an exercise for the reader...
        dlg = wxFileDialog(self)
        dlg.SetStyle(wxOPEN)
        dlg.SetWildcard("*.dtj")
        if dlg.ShowModal() == wxID_OK:
            self.path = dlg.GetPath()
            self.SetTitle(self.title + ' - ' + self.path)
            self.bookset = BookSet()
            self.bookset.load(self.path)
            self.GetMenuBar().EnableTop(1, true)

            win = JournalView(self, self.bookset, ID_EDIT)
            self.views.append((win, ID_JRNL))

        dlg.Destroy()


    def OnMenuClose(self, event):
        # should be asking to save here...
        self.GetMenuBar().EnableTop(1, false)
        for view in self.views:
            view[0].Close()
        self.views = []
        self.SetTitle(self.title)


    def OnMenuSave(self, event):
        self.bookset.save(self.path)
        dlg = wxMessageDialog(self, "Bookset Saved", "",
                              wxOK | wxICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


    def OnMenuSaveAs(self, event):
        dlg = wxFileDialog(self)
        dlg.SetStyle(wxSAVE | wxOVERWRITE_PROMPT)
        dlg.SetWildcard("*.dtj")
        dlg.SetMessage("Save the BookSet as:")
        if dlg.ShowModal() == wxID_OK:
            self.path = dlg.GetPath()
            self.bookset.save(self.path)
            self.SetTitle(self.title + ' - ' + self.path)
        dlg.Destroy()


    def OnMenuExit(self, event):
        self.Close()

    def OnMenuAbout(self, event):
        dlg = wxMessageDialog(self,
                              "This program uses the doubletalk package to\n"
                              "demonstrate the wxPython toolkit.\n\n"
                              "by Robin Dunn",
                              "About", wxOK | wxICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


    def OnAddTrans(self, event):
        dlg = EditTransDlg(self, None, self.bookset.getAccountList())
        if dlg.ShowModal() == wxID_OK:
            trans = dlg.GetTrans()
            self.bookset.add(trans)
            self.UpdateViews()
        dlg.Destroy()


    def OnViewJournal(self, event):
        for view in self.views:
            if view[1] == ID_JRNL:
                view[0].Restore()
                view[0].Raise()
                return
        win = JournalView(self, self.bookset, ID_EDIT)
        self.views.append((win, ID_JRNL))


    def OnViewDetail(self, event):
        pass




    # Time-out handler
    def Notify(self):
        t = time.localtime(time.time())
        st = time.strftime(" %d-%b-%Y   %I:%M:%S", t)
        self.SetStatusText(st, 1)


    def OnCloseWindow(self, event):
        self.timer.Stop()
        del self.timer
        del self.icon
        self.Destroy()


#----------------------------------------------------------------------

class DoubleTalkBrowserApp(wxApp):
    def OnInit(self):
        frame = MainFrame(NULL)
        frame.Show(true)
        self.SetTopWindow(frame)
        return true

app = DoubleTalkBrowserApp(0)
app.MainLoop()
