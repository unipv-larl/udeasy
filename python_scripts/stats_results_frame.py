import wx


class StatsFrame(wx.Frame):
    """
    The frame in which the selected statistics are shown
    """
    def __init__(self, parent, stats_string):
        super().__init__(parent, title="stats", size=(600, 400))
        self.panel = wx.Panel(self)
        self.stats_text = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE, value=stats_string)
        size = self.stats_text.GetFont().GetPointSize()
        self.stats_text.SetFont(wx.Font(size, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.NORMAL, faceName="Monospace"))
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.stats_text, 1, wx.ALL | wx.EXPAND)
        self.panel.SetSizer(self.sizer)
        self.panel.Layout()
        self.Show()

        self.InitUI()

    def InitUI(self):
        menubar = wx.MenuBar()

        fileMenu = wx.Menu()
        item_saveas = wx.MenuItem(fileMenu, wx.ID_SAVEAS, text="Save as...")
        fileMenu.Append(item_saveas)
        menubar.Append(fileMenu, "&File")

        self.Bind(wx.EVT_MENU, self.menuhandler)
        self.SetMenuBar(menuBar=menubar)
        self.Layout()

    def menuhandler(self, event):
        id = event.GetId()
        if id == wx.ID_SAVEAS:
            wildcard = "txt file (*.txt)|*.txt|" \
                       "All files (*.*)|*.*"
            dlg = wx.FileDialog(
                self, message="Save as...",
                defaultDir="",
                defaultFile="",
                wildcard=wildcard,
                style=wx.FD_SAVE
            )
            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(self.stats_text.GetValue())
            dlg.Destroy()
