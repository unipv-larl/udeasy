import wx
import wx.lib.scrolledpanel as scrolled
import printer


class ExportFrame(wx.Frame):
    """
    The frame that appears when clicking 'File - Export as csv'
    """
    def __init__(self, parent, results, *args, **kw):
        self.results = results
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
        # getting the list of nodes and the list of keys
        node_names = []
        list_of_keys = []
        for r in self.results:
            node_names += list(r.keys())
            for n in r:
                list_of_keys += list(r[n].feats.keys()) + list(r[n].misc.keys())

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
        # adding the nodes_info_panel
        self.nodes_info_panel = NodesInfoPanel(parent=self.main_panel, node_names=list(set(node_names)), list_of_keys=list(set(list_of_keys)))
        self.main_sizer.Add(self.nodes_info_panel, 0, wx.ALL | wx.ALIGN_LEFT, 5)

        btn_confirm = wx.Button(self.main_panel, label="Confirm")
        btn_confirm.Bind(wx.EVT_BUTTON, self.pass_parameters)
        self.main_sizer.Add(btn_confirm, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        
        self.main_panel.SetSizer(self.main_sizer)
        self.Show()

    def pass_parameters(self, event):
        """
        This function stores the parameters passed to the frame to export the results as a csv file.
        It opens a file dialog to select the path where to store the file.
        """
        fields = {'sent': []}
        if self.sent_info_panel.cb_id.GetValue():
            fields['sent'].append('sent_id')
        if self.sent_info_panel.cb_text.GetValue():
            fields['sent'].append('text')
        for n in self.nodes_info_panel.node_names:
            node_panel = getattr(self.nodes_info_panel, f"node_panel_{n}")
            fields[n] = []
            for i in node_panel.ids:
                feat_row = getattr(node_panel, f"feat_row{i}")
                if feat_row.feature.GetValue():
                    fields[n].append(feat_row.feature.GetValue())
        setattr(self, "csv_parameters", fields)
        wildcard = "csv file (*.csv)|*.csv|" \
                       "All files (*.*)|*.*"
        dlg = wx.FileDialog(
            self, message="Export as csv file",
            defaultDir="",
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_SAVE
        )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            printer.res2csv(results=self.results, fields=self.csv_parameters, path=path)
        dlg.Destroy()


class SentInfoPanel(wx.Panel):
    """
    The panel where boxes with information about the sentence can be checked
    """
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
    """
    The panel where boxes with information about the nodes can be selected
    """
    def __init__(self, parent, node_names, list_of_keys=[], *args, **kw):
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
        self.feature = wx.ComboBox(self, choices=self.parent.parent.choices)
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
    frame = ExportFrame(parent=None, node_names=['verb', 'noun'], list_of_keys=[])
    frame.Show()
    app.MainLoop()
