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
            self.btn_nodes_panel.Bind(wx.EVT_BUTTON, self.show_feats_panel)
            setattr(self, "btn_reset_nodes", wx.Button(self.main_panel, label="Clear All"))
            self.btn_reset_nodes.Bind(wx.EVT_BUTTON, self.reset)
            btns_sizer.Add(self.btn_nodes_panel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            btns_sizer.Add(self.btn_reset_nodes, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            self.main_sizer.Add(btns_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)
            self.main_panel.SetSizer(self.main_sizer)
            self.main_panel.Layout()
            self.main_panel.SetupScrolling(scrollToTop=False)
            self.main_panel.Scroll(-1, self.main_panel.GetScrollRange(wx.VERTICAL))

    def show_feats_panel(self, event):
        """
        Function that runs when the confirm button in the nodes panel is pressed.
        It shows the panel to define the nodes' features.
        """
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

        # if a feats panel has not yet been shown, create one
        if not hasattr(self, "feats_panel"):
            setattr(self, "feats_panel", features.Features(self.main_panel, self.node_names, list_of_keys))
            self.main_sizer.Add(getattr(self, "feats_panel"), 0, wx.ALL | wx.ALIGN_LEFT, 10)
            setattr(self, "btn_reset_feats", wx.Button(self.main_panel, label="Clear All"))
            self.btn_reset_feats.Bind(wx.EVT_BUTTON, self.reset)
            btns_sizer = wx.BoxSizer(wx.HORIZONTAL)
            setattr(self, "btn_feats_panel", wx.Button(self.main_panel, label="Confirm"))
            self.btn_feats_panel.Bind(wx.EVT_BUTTON, self.show_relations_panel)
            btns_sizer.Add(self.btn_feats_panel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            btns_sizer.Add(self.btn_reset_feats, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            self.main_sizer.Add(btns_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)
            self.main_panel.SetSizer(self.main_sizer)
            self.main_panel.Layout()
            self.main_panel.SetupScrolling(scrollToTop=False)
            self.main_panel.Scroll(-1, self.main_panel.GetScrollRange(wx.VERTICAL))
        else:
            # destroyng the feats panel and its buttons
            getattr(self, "feats_panel").Destroy()
            getattr(self, "btn_feats_panel").Destroy()
            getattr(self, "btn_reset_feats").Destroy()

            # recreating the feats panel
            setattr(self, "feats_panel", features.Features(self.main_panel, self.node_names, list_of_keys))
            self.main_sizer.Add(getattr(self, "feats_panel"), 0, wx.ALL | wx.ALIGN_LEFT, 10)
            setattr(self, "btn_reset_feats", wx.Button(self.main_panel, label="Clear All"))
            self.btn_reset_feats.Bind(wx.EVT_BUTTON, self.reset)
            btns_sizer = wx.BoxSizer(wx.HORIZONTAL)
            setattr(self, "btn_feats_panel", wx.Button(self.main_panel, label="Confirm"))
            self.btn_feats_panel.Bind(wx.EVT_BUTTON, self.show_relations_panel)
            btns_sizer.Add(self.btn_feats_panel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            btns_sizer.Add(self.btn_reset_feats, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            self.main_sizer.Add(btns_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)
            self.main_panel.SetSizer(self.main_sizer)
            self.main_panel.Layout()
            self.main_panel.SetupScrolling(scrollToTop=False)
            self.main_panel.Scroll(-1, self.main_panel.GetScrollRange(wx.VERTICAL))

    def show_relations_panel(self, event):
        """
        Function that runs when the confirm button in the features panel is pressed.
        It shows the panel to define the nodes' relations.
        """
        if not hasattr(self, "relations_panel"):
            setattr(self, "features", {n: {} for n in self.node_names})
            for node in self.features:
                feat_node_panel = getattr(self.feats_panel, f"node_panel_{node}")
                for i in feat_node_panel.ids:
                    feat_row = getattr(feat_node_panel, f"feat_row{i}")
                    key = feat_row.feat_field.GetValue()
                    flag = feat_row.value_flag.GetValue()
                    if flag == 'value is':
                        f = True
                    else:
                        f = False
                    val = feat_row.value_field.GetValue()
                    if f:
                        self.features[node][key] = val
                    else:
                        self.features[node][key] = f'###NOT###{val}'
            setattr(self, "relations_panel", relations.Relations(self.main_panel, self.node_names))
            self.main_sizer.Add(getattr(self, "relations_panel"), 0, wx.ALL | wx.ALIGN_LEFT, 10)
            setattr(self, "btn_reset_relations", wx.Button(self.main_panel, label="Clear All"))
            self.btn_reset_relations.Bind(wx.EVT_BUTTON, self.reset)
            btns_sizer = wx.BoxSizer(wx.HORIZONTAL)
            setattr(self, "btn_relations_panel", wx.Button(self.main_panel, label="Confirm"))
            self.btn_relations_panel.Bind(wx.EVT_BUTTON, self.show_positions_panel)
            btns_sizer.Add(self.btn_relations_panel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            btns_sizer.Add(self.btn_reset_relations, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            self.main_sizer.Add(btns_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)
            self.main_panel.SetSizer(self.main_sizer)
            self.main_panel.Layout()
            self.main_panel.SetupScrolling(scrollToTop=False)
            self.main_panel.Scroll(-1, self.main_panel.GetScrollRange(wx.VERTICAL))

    def show_positions_panel(self, event):
        """
        Function that runs when the confirm button in the nodes panel is pressed.
        It shows the panel to define the nodes' features.
        """
        if not hasattr(self, "positions_panel"):
            setattr(self, "relations", [])
            for i in getattr(self.relations_panel, "ids"):
                rel_row = getattr(self.relations_panel, f"rel_row{i}")
                r = {}
                r['node1'] = rel_row.node1.GetValue()
                r['rel'] = rel_row.rel.GetValue()
                r['node2'] = rel_row.node2.GetValue()
                self.relations.append(r)
            setattr(self, "positions_panel", positions.Positions(self.main_panel, self.node_names))
            self.main_sizer.Add(getattr(self, "positions_panel"), 0, wx.ALL | wx.ALIGN_LEFT, 10)
            cb_sizer = wx.BoxSizer(wx.HORIZONTAL)
            setattr(self, "cb_title", wx.StaticText(self.main_panel, label="Visualize:"))
            setattr(self, "cb_sentences", wx.CheckBox(self.main_panel, label="conllu sentences"))
            setattr(self, "cb_conllu", wx.CheckBox(self.main_panel, label="conllu matched nodes"))
            setattr(self, "cb_trees", wx.CheckBox(self.main_panel, label="trees"))
            cb_sizer.Add(self.cb_title, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            cb_sizer.Add(self.cb_sentences, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            cb_sizer.Add(self.cb_conllu, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            cb_sizer.Add(self.cb_trees, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            btns_sizer = wx.BoxSizer(wx.HORIZONTAL)
            setattr(self, "btn_reset_positions", wx.Button(self.main_panel, label="Clear All"))
            self.btn_reset_positions.Bind(wx.EVT_BUTTON, self.reset)
            setattr(self, "btn_positions_panel", wx.Button(self.main_panel, label="Submit query"))
            self.btn_positions_panel.Bind(wx.EVT_BUTTON, self.search)
            btns_sizer.Add(self.btn_positions_panel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            btns_sizer.Add(self.btn_reset_positions, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            self.main_sizer.Add(cb_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)
            self.main_sizer.Add(btns_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)
            self.main_panel.SetSizer(self.main_sizer)
            self.main_panel.Layout()
            self.main_panel.SetupScrolling(scrollToTop=False)
            self.main_panel.Scroll(-1, self.main_panel.GetScrollRange(wx.VERTICAL))

    def search(self, event):
        """
        This function runs when the 'Submit query' button in the main frame is pressed.
        It process the query and iterates over the sentence of the selected treebank to look for patterns that meet the
        requests. It shows them in a new frame.
        """
        setattr(self, "positions", [])
        for i in getattr(self.positions_panel, "ids"):
            pos_row = getattr(self.positions_panel, f"pos_row{i}")
            p = {}
            p['node1'] = pos_row.node1.GetValue()
            p['rel'] = pos_row.rel.GetValue()
            p['node2'] = pos_row.node2.GetValue()
            p['by'] = pos_row.by.GetValue()
            p['dist'] = pos_row.pos.GetValue()
            self.positions.append(p)
        setattr(self, "res", search.QueryResults())
        self.res.process(tb=self.treebank, features=self.features, relations=self.relations,
                         positions=self.positions, show_sent=self.cb_sentences.GetValue(),
                         show_conllu=self.cb_conllu.GetValue(), show_trees=self.cb_trees.GetValue())
        setattr(self, "res_frame", results.ResultsFrame(self, self.res))

    def reset(self, event):
        """
        This function runs when the 'Clear all' button in the main frame is pressed.
        It resets all the panels and the values inserted so far.
        """
        to_be_deleted = ['nodes_panel', 'feats_panel', 'relations_panel', 'positions_panel']
        btns = ["btn_reset_nodes", "btn_reset_feats", "btn_reset_relations", "btn_reset_positions",
                "btn_nodes_panel", "btn_feats_panel", "btn_relations_panel", "btn_positions_panel"]
        cbs = ["cb_title", "cb_sentences", "cb_conllu", "cb_trees"]
        for attr in to_be_deleted + btns + cbs:
            if hasattr(self, attr):
                getattr(self, attr).Destroy()
                delattr(self, attr)
        self = MainFrame()

    def on_close(self, event):
        wx.Exit()


if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
