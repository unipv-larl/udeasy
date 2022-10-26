import wx
import wx.lib.scrolledpanel as scrolled


class ExportFrame(wx.Frame):
    """
    The frame that appears when clicking 'File - Export as csv'
    """
    def __init__(self, parent, *args, **kw):
        super().__init__(parent=parent, title='Export results', size=(500, 600))
        self.main_panel = scrolled.ScrolledPanel(self)
        self.main_panel.SetAutoLayout(1)
        self.main_panel.SetupScrolling()
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self.main_panel, label="Export results as csv")
        title.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        explanation = "Select the information you want to export"
        subtitle = wx.StaticText(self.main_panel, label=explanation)
        subtitle.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL))
        self.main_sizer.Add(title, 0, wx.ALL | wx.ALIGN_LEFT, 10)
        self.main_sizer.Add(subtitle, 0, wx.ALL | wx.ALIGN_LEFT, 8)
        # TODO add the panels

        # adding the title of the sent_info panel
        sent_info_title = wx.StaticText(self.main_panel, label="Sentence info")
        sent_info_title.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.main_sizer.Add(sent_info_title, 0, wx.ALL | wx.ALIGN_LEFT, 5)
        # adding the sent_info panel
        self.sent_info_panel = SentInfoPanel(parent=self.main_panel)
        self.main_sizer.Add(self.sent_info_panel, 0, wx.ALL | wx.ALIGN_LEFT, 5)

        # adding the title of the nodes_info panel
        nodes_info_title = wx.StaticText(self.main_panel, label="Nodes info")
        nodes_info_title.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.main_sizer.Add(nodes_info_title, 0, wx.ALL | wx.ALIGN_LEFT, 5)

        self.nodes_info_panel = NodesInfoPanel(parent=self.main_panel, node_names=['verb', 'noun'], list_of_keys=[])
        self.main_sizer.Add(self.nodes_info_panel, 0, wx.ALL | wx.ALIGN_LEFT, 5)

        self.main_panel.SetSizer(self.main_sizer)


class SentInfoPanel(wx.Panel):
    def __init__(self, parent, *args, **kw):
        super().__init__(parent=parent)
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # adding the checkboxes
        self.cb_id = wx.CheckBox(self, label="sent_id")
        self.cb_text = wx.CheckBox(self, label="text")
        self.cb_id.SetValue(True)
        self.cb_text.SetValue(True)
        self.main_sizer.Add(self.cb_id, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.main_sizer.Add(self.cb_text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        
        self.SetSizer(self.main_sizer)
        self.Layout()


class NodesInfoPanel(wx.Panel):
    def __init__(self, parent, node_names, list_of_keys, *args, **kw):
        self.node_names = node_names
        self.parent = parent
        self.choices = ['form', 'lemma', 'upos', 'xpos', 'deprel'] + sorted(list_of_keys)
        wx.Panel.__init__(self, parent)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, label="Features")
        title.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        explanation = "Choose a feature from the list or type a feature"
        subtitle = wx.StaticText(self, label=explanation)
        subtitle.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL))
        self.main_sizer.Add(title, 0, wx.ALL | wx.ALIGN_LEFT, 5)
        self.main_sizer.Add(subtitle, 0, wx.ALL | wx.ALIGN_LEFT, 5)
        for n in node_names:
            setattr(self, f"node_panel_{n}", NodePanel(self, n))
            self.main_sizer.Add(getattr(self, f"node_panel_{n}"), 0, wx.ALL | wx.ALIGN_LEFT, 5)
        self.SetSizer(self.main_sizer)


class NodePanel(wx.Panel):
    def __init__(self, parent, node_name, *args, **kw):
        self.parent = parent
        self.count = 1
        self.ids = [1]
        super().__init__(parent=parent)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, label=node_name)
        title.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_SLANT, wx.FONTWEIGHT_NORMAL))
        self.main_sizer.Add(title, 0, wx.ALL | wx.ALIGN_LEFT, 5)
        setattr(self, f"feat_row{self.count}", FeatRow(self))
        self.main_sizer.Add(getattr(self, f"feat_row{self.count}"), 0, wx.ALL | wx.ALIGN_LEFT, 5)
        self.SetSizer(self.main_sizer)
        self.Layout()


class FeatRow(wx.Panel):
    def __init__(self, parent, *args, **kw):
        self.parent = parent
        self.id = parent.count
        super().__init__(parent=parent)
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.feature = wx.ComboBox(self, choices=['a', 'b', 'c'])
        btn_add = wx.Button(self, label='+')
        btn_add.Bind(wx.EVT_BUTTON, self.on_add)
        self.main_sizer.Add(self.feature, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.main_sizer.Add(btn_add, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        if parent.count > 1:
            btn_rmv = wx.Button(self, label='-')
            btn_rmv.Bind(wx.EVT_BUTTON, self.on_rmv)
            self.main_sizer.Add(btn_rmv, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.SetSizer(self.main_sizer)
        self.Layout()
    
    def on_add(self, event):
        self.Parent.count += 1
        print(self.Parent.count)
        self.Parent.ids.append(self.Parent.count)
        setattr(self.Parent, f"feat_row{self.Parent.count}", FeatRow(self.Parent))
        self.Parent.main_sizer.Add(getattr(self.Parent, f"feat_row{self.Parent.count}"), 0, wx.ALL | wx.ALIGN_LEFT, 5)
        self.Parent.SetSizer(self.Parent.main_sizer)
        self.Parent.Layout()
        self.Parent.Parent.Parent.SetupScrolling(scrollToTop=False)
        self.Parent.Parent.Parent.Scroll(-1, self.Parent.Parent.Parent.GetScrollRange(wx.VERTICAL))
    
    def on_rmv(self, event):
        self.Parent.ids.remove(self.id)
        self.Destroy()
        self.parent.Layout()
        self.parent.parent.Layout()
        self.parent.parent.Parent.Layout()

if __name__ == '__main__':
    app = wx.App()
    frame = ExportFrame(parent=None)
    frame.Show()
    app.MainLoop()
