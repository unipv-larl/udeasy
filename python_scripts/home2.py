import wx
import wx.lib.scrolledpanel as scrolled
import choose_file
import nodes
import features
import relations
import positions
import search
import results
import udapi


class MainFrame(wx.Frame):
    """
    Main frame class: shows the main frame of the app.
    """
    def __init__(self):
        # defining the attributes of the main app
        self.file = None
        self.node_names = None
        self.features = None
        self.relations = None
        self.positions = None
        self.treebank = None
        super().__init__(parent=None, title='udeasy', size=(800, 400))
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.main_panel = scrolled.ScrolledPanel(self)
        self.main_panel.SetAutoLayout(1)
        self.main_panel.SetupScrolling()
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self.main_panel, label="Welcome to udeasy")
        title.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        # file chooser
        self.main_sizer.Add(title, 0, wx.ALL | wx.CENTER, 30)
        self.file_chooser = choose_file.ChooseFile(self.main_panel)
        self.main_sizer.Add(self.file_chooser, 0, wx.ALL | wx.ALIGN_LEFT, 10)
        btn_file_chooser = wx.Button(self.main_panel, label="Confirm")
        btn_file_chooser.Bind(wx.EVT_BUTTON, self.show_nodes_panel)
        self.main_sizer.Add(btn_file_chooser, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        self.main_panel.SetSizer(self.main_sizer)

    def show_nodes_panel(self, event):
        """
        Function that runs when the confirm button in the main frame is pressed.
        It shows the panel to define the node names.
        """
        # setting the attributes passed to the previous panel (file name and then conllu document)
        setattr(self, "file", self.file_chooser.file_path)
        setattr(self, "treebank", udapi.Document(self.file))

        # if a nodes panel has not yet been shown, create one
        if not hasattr(self, "nodes_panel"):
            setattr(self, "nodes_panel", nodes.Nodes(self.main_panel))
            self.main_sizer.Add(getattr(self, "nodes_panel"), 0, wx.ALL | wx.ALIGN_LEFT, 10)
            btns_sizer = wx.BoxSizer(wx.HORIZONTAL)
            setattr(self, "btn_nodes_panel", wx.Button(self.main_panel, label="Confirm"))
            self.btn_nodes_panel.Bind(wx.EVT_BUTTON, self.show_other_panels)
            setattr(self, "btn_reset_nodes", wx.Button(self.main_panel, label="Clear All"))
            self.btn_reset_nodes.Bind(wx.EVT_BUTTON, self.reset)
            btns_sizer.Add(self.btn_nodes_panel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            btns_sizer.Add(self.btn_reset_nodes, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            self.main_sizer.Add(btns_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)
            self.main_panel.SetSizer(self.main_sizer)
            self.main_panel.Layout()
            self.main_panel.SetupScrolling(scrollToTop=False)
            self.main_panel.Scroll(-1, self.main_panel.GetScrollRange(wx.VERTICAL))

    def show_other_panels(self, event):
        # setting the attributes passed to the previous panel (node's names)
        setattr(self, "node_names", [])
        for i in self.nodes_panel.ids:
            node_row = getattr(self.nodes_panel, f"node_row{i}")
            self.node_names.append(getattr(node_row, "node_field").GetValue())

        # extracting the keys of the feats and misc conllu fields
        list_of_keys = []
        for sent in self.treebank[:100]:
            root = sent.get_tree()
            nodes = root.descendants()
            for n in nodes:
                list_of_keys += list(n.feats.keys())
                list_of_keys += list(n.misc.keys())
        list_of_keys = list(set(list_of_keys))
        # TODO: show feats panel
        if not hasattr(self, "feats_panel"):
            pass
            # TODO: show relations panel
            # TODO: show positions panel
            # TODO: add buttons to confirm and import query file
            # TODO: add ticks for visualizing results

        else:
            # TODO: delete all the panels and buttons
            # TODO: show everything again
            pass
