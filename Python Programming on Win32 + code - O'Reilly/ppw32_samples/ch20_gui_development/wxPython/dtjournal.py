
from wxPython.wx import *

from dtedittrans import EditTransDlg


#----------------------------------------------------------------------

class JournalView(wxMDIChildFrame):
    def __init__(self, parent, bookset, editID):
        wxMDIChildFrame.__init__(self, parent, -1, "")
        self.bookset = bookset
        self.parent = parent

        tID = wxNewId()
        self.lc = wxListCtrl(self, tID, wxDefaultPosition, wxDefaultSize,
                             wxLC_REPORT)
        # Forces a resize event to get around a minor bug...
        sz = self.GetSize()
        self.SetSize((sz.width-1, sz.height-1))

        self.lc.InsertColumn(0, "Date")
        self.lc.InsertColumn(1, "Comment")
        self.lc.InsertColumn(2, "Amount")

        self.currentItem = -1
        EVT_LIST_ITEM_SELECTED(self, tID, self.OnItemSelected)
        EVT_LEFT_DCLICK(self.lc, self.OnDoubleClick)

        menu = parent.MakeMenu(true)
        self.SetMenuBar(menu)
        EVT_MENU(self, editID, self.OnEdit)
        EVT_CLOSE(self, self.OnCloseWindow)

        self.UpdateView()


    def OnEdit(self, *event):
        if self.currentItem != -1:
            trans = self.bookset[self.currentItem]
            dlg = EditTransDlg(self, trans, self.bookset.getAccountList())
            if dlg.ShowModal() == wxID_OK:
                trans = dlg.GetTrans()
                self.bookset.edit(self.currentItem, trans)
                self.parent.UpdateViews()
            dlg.Destroy()


    def OnItemSelected(self, event):
        self.currentItem = event.m_itemIndex

    def OnDoubleClick(self, event):
        self.OnEdit()

    def OnCloseWindow(self, event):
        self.parent.CloseView(self)
        self.Destroy()


    def UpdateView(self):
        self.lc.DeleteAllItems()
        for x in range(len(self.bookset)):
            trans = self.bookset[x]
            self.lc.InsertStringItem(x, trans.getDateString())
            self.lc.SetStringItem(x, 1, trans.comment)
            self.lc.SetStringItem(x, 2, str(trans.magnitude()))

        self.lc.SetColumnWidth(0, wxLIST_AUTOSIZE)
        self.lc.SetColumnWidth(1, wxLIST_AUTOSIZE)
        self.lc.SetColumnWidth(2, wxLIST_AUTOSIZE)

        self.SetTitle("Journal view - %d transactions" %
                      len(self.bookset))


#----------------------------------------------------------------------


