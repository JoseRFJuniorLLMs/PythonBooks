
from wxPython.wx import *
from doubletalk.transac import Transaction
from doubletalk  import dates

import string
import copy

#----------------------------------------------------------------------

ID_DATE    = 200
ID_COMMENT = 201
ID_LIST    = 202
ID_ACCT    = 203
ID_AMT     = 204
ID_ADD     = 205
ID_UPDT    = 206
ID_DEL     = 207
ID_BAL     = 208

#----------------------------------------------------------------------

class EditTransDlg(wxDialog):

    def __init__(self, parent, trans, accountList):

        # This is fairly simple stuff.  We just invoke the parent
        # class' __init__ method, do some initialization, and
        # determine if we are editing an existing transaction or
        # creating a new one.  If editing an existing transaction then
        # we use the Python copy module to make a copy of the object.
        # We do this because we will be editing the transaction
        # in-place and we don't want to have any partially edited
        # transactions stuck in the bookset.  If the dialog is being
        # used to add a new transaction, we create one, and then fix
        # its date by truncating the time from it.  The default date
        # in the transaction includes the current time, but this
        # dialog is only equipped to deal with the date portion.  So
        # far, so good.
        wxDialog.__init__(self, parent, -1, "")
        self.item = -1
        if trans:
            self.trans = copy.deepcopy(trans)
            self.SetTitle("Edit Transaction")
        else:
            self.trans = Transaction()
            self.trans.setDateString(dates.ddmmmyyyy(self.trans.date))
            self.SetTitle("Add Transaction")

        # This is how we create the labels and the text fields at the
        # top of the dialog.  Notice the use of wxDLG_PNT and
        # wxDLG_SZE to convert dialog units to a wxPoint and a wxSize
        # respectively.  (The -1's used above mean that the default
        # size should be used for the height.)  The wxPoint and wxSize
        # are always defined in terms of pixels, but these conversion
        # functions allow the actual number of pixels use to
        # automatically vary from machine to machine where the default
        # font is different.  For wxPython it also helps for moving
        # programs from platform to platform as well.
        wxStaticText(self, -1, "Date:", wxDLG_PNT(self, 5,5))
        self.date = wxTextCtrl(self, ID_DATE, "",
                               wxDLG_PNT(self, 35,5), wxDLG_SZE(self, 50, -1))

        wxStaticText(self, -1, "Comment:", wxDLG_PNT(self, 5,21))
        self.comment = wxTextCtrl(self, ID_COMMENT, "",
                                  wxDLG_PNT(self, 35, 21), wxDLG_SZE(self, 195, -1))


        # An important thing to note here is that the width of this
        # list control is 225 dialog units.  Since this control spans
        # the entire width of the dialog, we know the space we have to
        # work with.  We can use this value when deciding where to
        # place or how to size the other controls.
        #
        # Instead of auto-sizing the width of the list columns this
        # time we've decided to use explicit sizes.  But we're still
        # able to use dialog units to do it by extracting the width
        # attribute from the wxSize object returned from wxDLG_SZE.
        self.lc = wxListCtrl(self, ID_LIST,
                             wxDLG_PNT(self, 5,34), wxDLG_SZE(self, 225, 60),
                             wxLC_REPORT)

        self.lc.InsertColumn(0, "Account")
        self.lc.InsertColumn(1, "Amount")
        self.lc.SetColumnWidth(0, wxDLG_SZE(self, 180,-1).width)
        self.lc.SetColumnWidth(1, wxDLG_SZE(self,  40,-1).width)

        wxStaticText(self, -1, "Balance:", wxDLG_PNT(self, 165,100))
        self.balance = wxTextCtrl(self, ID_BAL, "",
                                  wxDLG_PNT(self, 190,100), wxDLG_SZE(self, 40, -1))
        self.balance.Enable(false)


        wxStaticLine(self, -1, wxDLG_PNT(self, 5, 115), wxDLG_SZE(self, 225,-1))

        wxStaticText(self, -1, "Account:", wxDLG_PNT(self, 5,122))
        self.account = wxComboBox(self, ID_ACCT, "",
                                  wxDLG_PNT(self, 30,122), wxDLG_SZE(self, 130, -1),
                                  accountList, wxCB_DROPDOWN | wxCB_SORT)

        wxStaticText(self, -1, "Amount:", wxDLG_PNT(self, 165,122))
        self.amount = wxTextCtrl(self, ID_AMT, "",
                                 wxDLG_PNT(self, 190,122), wxDLG_SZE(self, 40, -1))

        btnSz = wxDLG_SZE(self, 40,12)
        wxButton(self, ID_ADD, "&Add Line", wxDLG_PNT(self, 52,140), btnSz)
        wxButton(self, ID_UPDT, "&Update Line", wxDLG_PNT(self, 97,140), btnSz)
        wxButton(self, ID_DEL, "&Delete Line", wxDLG_PNT(self, 142,140), btnSz)

        self.ok = wxButton(self, wxID_OK, "OK", wxDLG_PNT(self, 145, 5), btnSz)
        self.ok.SetDefault()
        wxButton(self, wxID_CANCEL, "Cancel", wxDLG_PNT(self, 190, 5), btnSz)

        # Resize the window to fit the controls
        self.Fit()

        # Set some event handlers
        EVT_BUTTON(self, ID_ADD,  self.OnAddBtn)
        EVT_BUTTON(self, ID_UPDT, self.OnUpdtBtn)
        EVT_BUTTON(self, ID_DEL,  self.OnDelBtn)
        EVT_LIST_ITEM_SELECTED(self,   ID_LIST, self.OnListSelect)
        EVT_LIST_ITEM_DESELECTED(self, ID_LIST, self.OnListDeselect)
        EVT_TEXT(self, ID_DATE, self.Validate)


        # Initialize the controls with current values
        self.date.SetValue(self.trans.getDateString())
        self.comment.SetValue(self.trans.comment)
        for x in range(len(self.trans.lines)):
            account, amount, dict = self.trans.lines[x]
            self.lc.InsertStringItem(x, account)
            self.lc.SetStringItem(x, 1, str(amount))

        self.Validate()


    def Validate(self, *ignore):
        bal = self.trans.balance()
        self.balance.SetValue(str(bal))
        date = self.date.GetValue()
        try:
            dateOK = (date == dates.testasc(date))
        except:
            dateOK = 0

        if bal == 0 and dateOK:
            self.ok.Enable(true)
        else:
            self.ok.Enable(false)



    def GetTrans(self):
        self.trans.setDateString(self.date.GetValue())
        self.trans.comment = self.comment.GetValue()
        # the lines are maintained in the tranaction already
        return self.trans


    def OnAddBtn(self, event):
        account = self.account.GetValue()
        amount = string.atof(self.amount.GetValue())
        self.trans.addLine(account, amount)

        # update the list control
        idx = len(self.trans.lines)
        self.lc.InsertStringItem(idx-1, account)
        self.lc.SetStringItem(idx-1, 1, str(amount))

        self.Validate()
        self.account.SetValue("")
        self.amount.SetValue("")



    def OnUpdtBtn(self, event):
        if self.item != -1:
            account = self.account.GetValue()
            amount = string.atof(self.amount.GetValue())

            # update the transaction
            self.trans.lines[self.item : self.item+1] = [(account, amount, None)]

            # update the list control
            self.lc.SetStringItem(self.item, 0, account)
            self.lc.SetStringItem(self.item, 1, str(amount))

            self.Validate()


    def OnDelBtn(self, event):
        if self.item != -1:
            self.lc.DeleteItem(self.item)
            del self.trans.lines[self.item]
            self.item = -1
            self.Validate()


    def OnListSelect(self, event):
        self.item = event.m_itemIndex
        account, amount, dict = self.trans.lines[self.item]
        self.account.SetValue(account)
        self.amount.SetValue(str(amount))


    def OnListDeselect(self, event):
        self.item = -1
        self.account.SetValue("")
        self.amount.SetValue("")











