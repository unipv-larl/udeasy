import wx


class WordsOrder(wx.Panel):
    """
    Panel in the stats_query_frame
    """
    def __init__(self, parent, node_list):
        self.parent = parent
        self.nodes = node_list
        wx.Panel.__init__(self, parent)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, label="Words order")
        title.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.main_sizer.Add(title, 0, wx.ALL | wx.ALIGN_LEFT, 5)
        for n in node_list:
            setattr(self, f"cb_{n}", wx.CheckBox(self, label=n))
            self.main_sizer.Add(getattr(self, f"cb_{n}"), 0, wx.ALL | wx.ALIGN_LEFT, 5)
        self.SetSizer(self.main_sizer)
        self.Layout()
