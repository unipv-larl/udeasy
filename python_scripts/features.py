import wx


class Features(wx.Panel):
    """
    Node's features main panel
    """
    def __init__(self, parent, node_names, list_of_keys):
        self.parent = parent
        self.choices = ['form', 'lemma', 'upos', 'xpos', 'deprel'] + sorted(list_of_keys)
        wx.Panel.__init__(self, parent)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, label="Features")
        title.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        explanation = "Choose a feature from the list or type a feature, then insert a value"
        subtitle = wx.StaticText(self, label=explanation)
        subtitle.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL))
        self.main_sizer.Add(title, 0, wx.ALL | wx.ALIGN_LEFT, 5)
        self.main_sizer.Add(subtitle, 0, wx.ALL | wx.ALIGN_LEFT, 5)
        for n in node_names:
            setattr(self, f"node_panel_{n}", NodePanel(self, n))
            self.main_sizer.Add(getattr(self, f"node_panel_{n}"), 0, wx.ALL | wx.ALIGN_LEFT, 5)
        self.SetSizer(self.main_sizer)


class NodePanel(wx.Panel):
    """
    Features panel for each single node
    """
    def __init__(self, parent, node_name):
        self.parent = parent
        self.count = 1
        self.ids = [1]
        wx.Panel.__init__(self, parent)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, label=node_name)
        title.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_SLANT, wx.FONTWEIGHT_NORMAL))
        self.main_sizer.Add(title, 0, wx.ALL | wx.ALIGN_LEFT, 5)
        setattr(self, f"feat_row{self.count}", FeatRow(self))
        self.main_sizer.Add(getattr(self, f"feat_row{self.count}"), 0, wx.ALL | wx.ALIGN_LEFT, 5)
        self.SetSizer(self.main_sizer)
        self.Layout()


class FeatRow(wx.Panel):
    """
    A row consisting of a feature name field and a feature value field
    """
    def __init__(self, parent):
        self.parent = parent
        self.id = self.parent.count
        wx.Panel.__init__(self, parent)
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        f_text = wx.StaticText(self, label="feature")
        setattr(self, f"feat_field", wx.ComboBox(self, choices=self.parent.parent.choices))
        setattr(self, "value_flag", wx.ComboBox(self, value='value is', choices=['value is', 'value is not']))
        setattr(self, f"value_field", wx.TextCtrl(self))
        btn_add = wx.Button(self, label='+')
        btn_add.Bind(wx.EVT_BUTTON, self.on_add)
        self.main_sizer.Add(f_text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.main_sizer.Add(self.feat_field, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.main_sizer.Add(self.value_flag, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.main_sizer.Add(self.value_field, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.main_sizer.Add(btn_add, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        if parent.count > 1:
            btn_rmv = wx.Button(self, label='-')
            btn_rmv.Bind(wx.EVT_BUTTON, self.on_rmv)
            self.main_sizer.Add(btn_rmv, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.SetSizer(self.main_sizer)
        self.Layout()

    def on_add(self, event):
        """
        When the button '+' is clicked, this function show another feature row on the main panel
        """
        self.parent.count += 1
        self.parent.ids.append(self.parent.count)
        setattr(self.parent, f"feat_row{self.parent.count}", FeatRow(self.parent))
        self.parent.main_sizer.Add(getattr(self.parent, f"feat_row{self.parent.count}"), 0, wx.ALL | wx.ALIGN_LEFT, 5)
        self.parent.SetSizer(self.parent.main_sizer)
        self.parent.Layout()
        self.parent.parent.Parent.SetupScrolling(scrollToTop=False)
        self.parent.parent.Parent.Scroll(-1, self.parent.parent.Parent.GetScrollRange(wx.VERTICAL))

    def on_rmv(self, event):
        """
        When the button '-' is clicked, this function removes the feature row from the main panel
        """
        self.parent.ids.remove(self.id)
        self.Destroy()
        self.parent.Layout()
        self.parent.parent.Layout()
        self.parent.parent.Parent.Layout()
