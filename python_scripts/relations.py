import wx


class Relations(wx.Panel):
    """
    Node's relations main panel
    """
    def __init__(self, parent, node_names):
        self.parent = parent
        self.count = 1
        self.ids = [1]
        wx.Panel.__init__(self, parent)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, label="Relations")
        title.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.main_sizer.Add(title, 0, wx.ALL | wx.ALIGN_LEFT, 5)
        setattr(self, f"rel_row{self.count}", RelRow(self, node_names))
        self.main_sizer.Add(getattr(self, f"rel_row{self.count}"), 0, wx.ALL | wx.ALIGN_LEFT, 5)
        self.SetSizer(self.main_sizer)
        self.Layout()


class RelRow(wx.Panel):
    def __init__(self, parent, node_names):
        self.parent = parent
        self.id = self.parent.count
        self.node_names = node_names
        possible_relations = ['is parent of', 'is ancestor of', 'is sibling of']
        wx.Panel.__init__(self, parent)
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        title = wx.StaticText(self, label=f"relation {self.id}")
        self.main_sizer.Add(title, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.node1 = wx.ComboBox(self, choices=node_names, value='')
        self.rel = wx.ComboBox(self, choices=possible_relations, value='')
        self.node2 = wx.ComboBox(self, choices=node_names, value='')
        btn_add = wx.Button(self, label='+')
        btn_add.Bind(wx.EVT_BUTTON, self.on_add)
        self.main_sizer.Add(self.node1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.main_sizer.Add(self.rel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.main_sizer.Add(self.node2, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.main_sizer.Add(btn_add, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        if parent.count > 1:
            btn_rmv = wx.Button(self, label='-')
            btn_rmv.Bind(wx.EVT_BUTTON, self.on_rmv)
            self.main_sizer.Add(btn_rmv, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.SetSizer(self.main_sizer)
        self.Layout()

    def on_add(self, event):
        """
        When the button '+' is clicked, this function show another relation row on the main panel
        """
        self.parent.count += 1
        self.parent.ids.append(self.parent.count)
        setattr(self.parent, f"rel_row{self.parent.count}", RelRow(self.parent, self.node_names))
        self.parent.main_sizer.Add(getattr(self.parent, f"rel_row{self.parent.count}"), 0, wx.ALL | wx.ALIGN_LEFT, 5)
        self.parent.SetSizer(self.parent.main_sizer)
        self.parent.Parent.Layout()
        self.parent.Parent.SetupScrolling(scrollToTop=False)
        self.parent.Parent.Scroll(-1, self.parent.Parent.GetScrollRange(wx.VERTICAL))
        self.parent.Layout()

    def on_rmv(self, event):
        """
        When the button '-' is clicked, this function removes the relation row from the main panel
        """
        self.parent.ids.remove(self.id)
        self.Destroy()
        self.parent.Parent.Layout()
        self.parent.Layout()
