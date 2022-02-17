import wx


class Positions(wx.Panel):
    """
    Nodes' positions main panel
    """
    def __init__(self, parent, node_names):
        self.parent = parent
        self.count = 1
        self.ids = [1]
        wx.Panel.__init__(self, parent)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, label="Positions")
        title.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.main_sizer.Add(title, 0, wx.ALL | wx.ALIGN_LEFT, 5)
        setattr(self, f"pos_row{self.count}", PosRow(self, node_names))
        self.main_sizer.Add(getattr(self, f"pos_row{self.count}"), 0, wx.ALL | wx.ALIGN_LEFT, 5)
        self.SetSizer(self.main_sizer)
        self.Layout()


class PosRow(wx.Panel):
    def __init__(self, parent, node_names):
        self.parent = parent
        self.id = self.parent.count
        self.node_names = node_names
        possible_positions = ['precedes', 'follows']
        possible_by = ['by exactly', 'by at least']
        wx.Panel.__init__(self, parent)
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.node1 = wx.ComboBox(self, choices=node_names)
        self.rel = wx.ComboBox(self, choices=possible_positions)
        self.node2 = wx.ComboBox(self, choices=node_names)
        self.by = wx.ComboBox(self, choices=possible_by)
        self.pos = wx.TextCtrl(self)
        posit = wx.StaticText(self, label=f"positions")
        btn_add = wx.Button(self, label='+')
        btn_add.Bind(wx.EVT_BUTTON, self.on_add)
        self.main_sizer.Add(self.node1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.main_sizer.Add(self.rel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.main_sizer.Add(self.node2, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.main_sizer.Add(self.by, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.main_sizer.Add(self.pos, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.main_sizer.Add(posit, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.main_sizer.Add(btn_add, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        if parent.count > 1:
            btn_rmv = wx.Button(self, label='-')
            btn_rmv.Bind(wx.EVT_BUTTON, self.on_rmv)
            self.main_sizer.Add(btn_rmv, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.SetSizer(self.main_sizer)
        self.Layout()

    def on_add(self, event):
        """
        When the button '+' is clicked, this function show another position row on the main panel
        """
        self.parent.count += 1
        self.parent.ids.append(self.parent.count)
        setattr(self.parent, f"pos_row{self.parent.count}", PosRow(self.parent, self.node_names))
        self.parent.main_sizer.Add(getattr(self.parent, f"pos_row{self.parent.count}"), 0, wx.ALL | wx.ALIGN_LEFT, 5)
        self.parent.SetSizer(self.parent.main_sizer)
        self.parent.Parent.Layout()
        self.parent.Parent.SetupScrolling(scrollToTop=False)
        self.parent.Parent.Scroll(-1, self.parent.Parent.GetScrollRange(wx.VERTICAL))
        self.parent.Layout()

    def on_rmv(self, event):
        """
        When the button '-' is clicked, this function removes the position row from the main panel
        """
        self.parent.ids.remove(self.id)
        self.Destroy()
        self.parent.Parent.Layout()
        self.parent.Layout()
