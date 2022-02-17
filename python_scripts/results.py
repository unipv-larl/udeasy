import wx
import wx.lib.newevent
import stats_query_frame


ID_STATS_FRAME = wx.NewId()
ID_COUNT = wx.NewId()


class ResultsFrame(wx.Frame):
    """
    The frame in which the matched patterns are shown
    """
    def __init__(self, parent, res):
        super().__init__(parent, title="matched patterns", size=(600, 400))
        self.res = res

        self.panel = wx.Panel(self)
        self.results_text = wx.TextCtrl(self.panel, id=-1, style=wx.TE_MULTILINE | wx.TE_RICH2, value=self.res.string)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.results_text, 1, wx.ALL | wx.EXPAND)
        self.panel.SetSizer(self.sizer)
        self.panel.Layout()

        self.InitUI()

    def InitUI(self):
        menubar = wx.MenuBar()

        fileMenu = wx.Menu()
        item_saveas = wx.MenuItem(fileMenu, wx.ID_SAVEAS, text="Save as...")
        fileMenu.Append(item_saveas)
        menubar.Append(fileMenu, "&File")

        statsMenu = wx.Menu()
        item_stats = wx.MenuItem(statsMenu, ID_STATS_FRAME, text="Stats")
        statsMenu.Append(item_stats)
        item_count = wx.MenuItem(statsMenu, ID_COUNT, text="Count results")
        statsMenu.Append(item_count)
        menubar.Append(statsMenu, "&Stats")

        self.Bind(wx.EVT_MENU, self.menuhandler)
        self.SetMenuBar(menuBar=menubar)
        self.Show()

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
                    file.write(self.results_text.GetValue())
            dlg.Destroy()

        elif id == ID_STATS_FRAME:
            stats_frame = stats_query_frame.StatsFrame(self, self.res.results)

        elif id == ID_COUNT:
            count_frame = CountFrame(self, self.res.count)


class CountFrame(wx.Frame):
    """
    The frame that appears when clicking 'Stats - Count' in the menu bar
    """
    def __init__(self, parent, doc_stats):
        super().__init__(parent, title="Some numbers", size=(300, 200))
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        text = ''
        for key in doc_stats:
            text += f'{key}: {doc_stats[key]}\n'
        count_text = wx.StaticText(self.panel, label=text)
        self.sizer.Add(count_text, 1, wx.ALL | wx.ALIGN_LEFT, 10)
        self.panel.SetSizer(self.sizer)
        self.panel.Layout()
        self.Show()
