import wx


class Nodes(wx.Panel):
    """
    Node names main panel
    """
    def __init__(self, parent):
        self.count = 1
        self.ids = [1]
        self.parent = parent
        wx.Panel.__init__(self, parent)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, label="Nodes")
        title.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        explanation = "Choose a name for the nodes you want to search in the treebank"
        subtitle = wx.StaticText(self, label=explanation)
        subtitle.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL))
        self.main_sizer.Add(title, 0, wx.ALL | wx.ALIGN_LEFT, 5)
        self.main_sizer.Add(subtitle, 0, wx.ALL | wx.ALIGN_LEFT, 5)
        setattr(self, f"node_row{self.count}", NodeRow(self))
        self.main_sizer.Add(getattr(self, f"node_row{self.count}"), 0, wx.ALL | wx.ALIGN_LEFT, 5)
        self.SetSizer(self.main_sizer)
        self.Layout()


class NodeRow(wx.Panel):
    def __init__(self, parent):
        self.parent = parent
        self.id = self.parent.count
        wx.Panel.__init__(self, parent)
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        title = wx.StaticText(self, label=f"node {self.id}")
        self.main_sizer.Add(title, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        setattr(self, f"node_field", wx.TextCtrl(self))
        self.main_sizer.Add(getattr(self, f"node_field"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        btn_add = wx.Button(self, label='+')
        btn_add.Bind(wx.EVT_BUTTON, self.on_add)
        self.main_sizer.Add(btn_add, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        if parent.count > 1:
            btn_rmv = wx.Button(self, label='-')
            btn_rmv.Bind(wx.EVT_BUTTON, self.on_rmv)
            self.main_sizer.Add(btn_rmv, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        if parent.count == 1:
            self.main_sizer.AddSpacer(95)
        setattr(self, "cb_optional", wx.CheckBox(self, label="optional"))
        self.main_sizer.Add(getattr(self, "cb_optional"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.SetSizer(self.main_sizer)
        self.Layout()

    def on_add(self, event):
        """
        When the button '+' is clicked, this function show another node row on the main panel
        """
        self.parent.count += 1
        self.parent.ids.append(self.parent.count)
        setattr(self.parent, f"node_row{self.parent.count}", NodeRow(self.parent))
        self.parent.main_sizer.Add(getattr(self.parent, f"node_row{self.parent.count}"), 0, wx.ALL | wx.ALIGN_LEFT, 5)
        self.parent.SetSizer(self.parent.main_sizer)
        self.parent.Parent.Layout()
        self.parent.Parent.SetupScrolling(scrollToTop=False)
        self.parent.Parent.Scroll(-1, self.parent.Parent.GetScrollRange(wx.VERTICAL))
        self.parent.Layout()

    def on_rmv(self, event):
        """
        When the button '-' is clicked, this function removes the node row from the main panel
        """
        self.parent.ids.remove(self.id)
        self.Destroy()
        self.parent.Parent.Layout()
        self.parent.Layout()
