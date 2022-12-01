import wx


class ErrorFrame(wx.Frame):
    def __init__(self, parent, errors):
        super().__init__(parent, title="errors", size=(600, 400))
        self.errors = errors

        self.panel = wx.Panel(self)
        self.errors_text = wx.TextCtrl(self.panel, id=-1, style=wx.TE_MULTILINE | wx.TE_RICH2, value=self.errors)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.errors_text, 1, wx.ALL | wx.EXPAND)
        self.panel.SetSizer(self.sizer)
        self.panel.Layout()
        self.Show()
