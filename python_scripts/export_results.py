from random import choices
import wx


class ExportFrame(wx.Frame):
    """
    The frame that appears when clicking 'File - Export as csv'
    """
    def __init__(self, parent, *args, **kw):
        super().__init__(parent=parent, title='Export results', size=(500, 600))
        self.main_panel = wx.Panel(self)
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
    pass


class NodePanel(wx.Panel):
    def __init__(self, parent, node_name, *args, **kw):
        self.count = 1
        self.ids = [1]
        super().__init__(parent=parent)


class FeatRow(wx.Panel):
    def __init__(self, parent, *args, **kw):
        self.id = parent.count
        super().__init__(parent=parent)
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.feature = wx.ComboBox(self, choices=['a', 'b', 'c'])
        btn_add = wx.Button(self, label='+')
        btn_add.Bind(wx.EVT_BUTTON, )
        

if __name__ == '__main__':
    app = wx.App()
    frame = ExportFrame(parent=None)
    frame.Show()
    app.MainLoop()
