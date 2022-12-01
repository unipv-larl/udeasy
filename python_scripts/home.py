import udapi
import wx
import wx.lib.scrolledpanel as scrolled
import choose_file
import nodes
import features
import relations
import positions
import search
import results
import valideasy
import error_frame


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
        if hasattr(self.file_chooser, "file_path"):
            self.file = self.file_chooser.file_path
        
        # TODO validate file and open only if passes the validation
        errors = valideasy.validate(self.file)
        if errors:
            errors = 'Please, correct the following errors in the treebank before loading the treebank\n' + errors
            setattr(self, "error_frm", error_frame.ErrorFrame(self, errors))
        else:
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
        # setting node_names as a dict {'name': True|False according to the value of the optional checkbox}
        self.node_names = {}
        for i in self.nodes_panel.ids:
            node_row = getattr(self.nodes_panel, f"node_row{i}")
            self.node_names[getattr(node_row, "node_field").GetValue()] = getattr(node_row, "cb_optional").GetValue()

        # extracting the keys of the feats and misc conllu fields
        list_of_keys = []
        for sent in self.treebank[:250]:
            root = sent.get_tree()
            nodes = root.descendants()
            for n in nodes:
                list_of_keys += list(n.feats.keys())
                list_of_keys += list(n.misc.keys())
        list_of_keys = list(set(list_of_keys))

        if not hasattr(self, "feats_panel"):
            # showing feats panel
            setattr(self, "feats_panel", features.Features(self.main_panel, list(self.node_names.keys()), list_of_keys))
            self.main_sizer.Add(getattr(self, "feats_panel"), 0, wx.ALL | wx.ALIGN_LEFT, 10)

            # showing relations panel
            setattr(self, "relations_panel", relations.Relations(self.main_panel, list(self.node_names.keys())))
            self.main_sizer.Add(getattr(self, "relations_panel"), 0, wx.ALL | wx.ALIGN_LEFT, 10)

            # showing positions panel
            setattr(self, "positions_panel", positions.Positions(self.main_panel, list(self.node_names.keys())))
            self.main_sizer.Add(getattr(self, "positions_panel"), 0, wx.ALL | wx.ALIGN_LEFT, 10)

            # visualizing options
            cb_sizer = wx.BoxSizer(wx.HORIZONTAL)
            setattr(self, "cb_title", wx.StaticText(self.main_panel, label="Visualize:"))
            setattr(self, "cb_sentences", wx.CheckBox(self.main_panel, label="conllu sentences"))
            setattr(self, "cb_conllu", wx.CheckBox(self.main_panel, label="conllu matched nodes"))
            setattr(self, "cb_trees", wx.CheckBox(self.main_panel, label="trees"))
            cb_sizer.Add(self.cb_title, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            cb_sizer.Add(self.cb_sentences, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            cb_sizer.Add(self.cb_conllu, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            cb_sizer.Add(self.cb_trees, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            self.main_sizer.Add(cb_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)

            # adding the buttons to the main frame
            btns_sizer = wx.BoxSizer(wx.HORIZONTAL)
            setattr(self, "btn_reset", wx.Button(self.main_panel, label="Clear All"))
            self.btn_reset.Bind(wx.EVT_BUTTON, self.reset)
            setattr(self, "btn_submit", wx.Button(self.main_panel, label="Submit query"))
            self.btn_submit.Bind(wx.EVT_BUTTON, self.search)
            btns_sizer.Add(self.btn_submit, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            btns_sizer.Add(self.btn_reset, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            self.main_sizer.Add(btns_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)

            self.main_panel.SetSizer(self.main_sizer)
            self.main_panel.Layout()
            self.main_panel.SetupScrolling(scrollToTop=False)
            self.main_panel.Scroll(-1, self.main_panel.GetScrollRange(wx.VERTICAL))

        # if something changes in the nodes panel
        elif hasattr(self, "feats_panel") and self.feats_panel.node_names != self.node_names:
            # clearing the main frame from everything except the nodes panel
            self.reset(event, delete_everything=False)

            # showing feats panel
            setattr(self, "feats_panel", features.Features(self.main_panel, list(self.node_names.keys()), list_of_keys))
            self.main_sizer.Add(getattr(self, "feats_panel"), 0, wx.ALL | wx.ALIGN_LEFT, 10)

            # showing relations panel
            setattr(self, "relations_panel", relations.Relations(self.main_panel, list(self.node_names.keys())))
            self.main_sizer.Add(getattr(self, "relations_panel"), 0, wx.ALL | wx.ALIGN_LEFT, 10)

            # showing positions panel
            setattr(self, "positions_panel", positions.Positions(self.main_panel, list(self.node_names.keys())))
            self.main_sizer.Add(getattr(self, "positions_panel"), 0, wx.ALL | wx.ALIGN_LEFT, 10)

            # visualizing options
            cb_sizer = wx.BoxSizer(wx.HORIZONTAL)
            setattr(self, "cb_title", wx.StaticText(self.main_panel, label="Visualize:"))
            setattr(self, "cb_sentences", wx.CheckBox(self.main_panel, label="conllu sentences"))
            setattr(self, "cb_conllu", wx.CheckBox(self.main_panel, label="conllu matched nodes"))
            setattr(self, "cb_trees", wx.CheckBox(self.main_panel, label="trees"))
            cb_sizer.Add(self.cb_title, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            cb_sizer.Add(self.cb_sentences, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            cb_sizer.Add(self.cb_conllu, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            cb_sizer.Add(self.cb_trees, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            self.main_sizer.Add(cb_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)

            # adding the buttons to the main frame
            btns_sizer = wx.BoxSizer(wx.HORIZONTAL)
            setattr(self, "btn_reset", wx.Button(self.main_panel, label="Clear All"))
            self.btn_reset.Bind(wx.EVT_BUTTON, self.reset)
            setattr(self, "btn_submit", wx.Button(self.main_panel, label="Submit query"))
            self.btn_submit.Bind(wx.EVT_BUTTON, self.search)
            btns_sizer.Add(self.btn_submit, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            btns_sizer.Add(self.btn_reset, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            self.main_sizer.Add(btns_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)

            self.main_panel.SetSizer(self.main_sizer)
            self.main_panel.Layout()
            self.main_panel.SetupScrolling(scrollToTop=False)
            self.main_panel.Scroll(-1, self.main_panel.GetScrollRange(wx.VERTICAL))

    def search(self, event):
        # creating the feats dict
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
            self.features[node]['optional'] = self.node_names[node]

        # creating the relations list
        setattr(self, "relations", [])
        for i in getattr(self.relations_panel, "ids"):
            rel_row = getattr(self.relations_panel, f"rel_row{i}")
            r = {}
            r['node1'] = rel_row.node1.GetValue()
            r['rel'] = rel_row.rel.GetValue()
            r['node2'] = rel_row.node2.GetValue()
            self.relations.append(r)

        # creating the positions list
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

        #TODO here create the YAML file and store it somewhere
        #TODO add a button to save and export the query

        # results object
        setattr(self, "res", search.QueryResults())
        self.res.process(tb=self.treebank, features=self.features, relations=self.relations,
                         positions=self.positions, show_sent=self.cb_sentences.GetValue(),
                         show_conllu=self.cb_conllu.GetValue(), show_trees=self.cb_trees.GetValue())

        # show results
        if not self.res.abort:
            setattr(self, "res_frame", results.ResultsFrame(self, self.res))

    def reset(self, event, delete_everything=True):
        # defining the lists of objects to be deleted
        to_be_deleted = ['feats_panel', 'relations_panel', 'positions_panel']
        btns = ["btn_reset", "btn_submit"]
        cbs = ["cb_title", "cb_sentences", "cb_conllu", "cb_trees"]
        if delete_everything:
            to_be_deleted += ['nodes_panel']
            btns += ['btn_nodes_panel', 'btn_reset_nodes']
        for attr in to_be_deleted + btns + cbs:
            if hasattr(self, attr):
                getattr(self, attr).Destroy()
                delattr(self, attr)
        if delete_everything:
            setattr(self, "file", self.file_chooser.file_path)
            setattr(self, "treebank", udapi.Document(self.file))

            # recreating the nodes panel
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

    def on_close(self, event):
        wx.Exit()


def main():
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    frame.Maximize()
    app.MainLoop()


if __name__ == '__main__':
    main()
