import wx
import wx.lib.scrolledpanel as scrolled
import stats_results_frame
import wo_stats
import wos_stats
import dist_stats
import feat_stats
import stats_func


class StatsFrame(wx.Frame):
    """
    The main frame that allows the user to select which kind of statistics get
    """
    def __init__(self, parent, all_results):
        self.wo = False
        self.wos = False
        self.dist = False
        self.feat = False
        self.dfs = []
        nodes = []
        for res in all_results:
            nodes += list(res.keys())
        self.nodes = list(set(nodes))
        self.results = all_results
        super().__init__(parent, title="select parameters", size=(800, 400))
        self.main_panel = scrolled.ScrolledPanel(self)
        self.main_panel.SetAutoLayout(1)
        self.main_panel.SetupScrolling()
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self.main_panel, label="What do you want information about?")
        title.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.main_sizer.Add(title, 0, wx.ALL | wx.ALIGN_LEFT, 10)
        cb_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cb_wo = wx.CheckBox(self.main_panel, label="word order (2 nodes)")
        self.cb_wos = wx.CheckBox(self.main_panel, label="word order (more nodes)")
        self.cb_dist = wx.CheckBox(self.main_panel, label="distances")
        self.cb_feat = wx.CheckBox(self.main_panel, label="features distribution")
        cb_sizer.Add(self.cb_wo, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        cb_sizer.Add(self.cb_wos, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        cb_sizer.Add(self.cb_dist, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        cb_sizer.Add(self.cb_feat, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.main_sizer.Add(cb_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        btn1 = wx.Button(self.main_panel, label="Confirm")
        btn1.Bind(wx.EVT_BUTTON, self.on_confirm)
        self.main_sizer.Add(btn1, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        self.main_panel.SetSizer(self.main_sizer)
        self.Show()

    def on_confirm(self, event):
        """
        This function show the panels to select the parameters of the stats chosen by the user
        """
        self.wo = self.cb_wo.GetValue()
        self.wos = self.cb_wos.GetValue()
        self.dist = self.cb_dist.GetValue()
        self.feat = self.cb_feat.GetValue()
        if self.wo:
            if not hasattr(self.main_panel, "wo_panel"):
                setattr(self.main_panel, "wo_panel", wo_stats.WordOrder(self.main_panel, self.nodes))
                self.main_sizer.Add(getattr(self.main_panel, "wo_panel"), 0, wx.ALL | wx.ALIGN_LEFT, 10)
                self.main_panel.SetSizer(self.main_sizer)
                self.main_panel.Layout()
                self.main_panel.SetupScrolling(scrollToTop=False)
                self.main_panel.Scroll(-1, self.main_panel.GetScrollRange(wx.VERTICAL))
        else:
            if hasattr(self.main_panel, "wo_panel"):
                self.main_panel.wo_panel.Destroy()
                delattr(self.main_panel, "wo_panel")
                self.main_panel.SetSizer(self.main_sizer)
                self.main_panel.Layout()
        if self.wos:
            if not hasattr(self.main_panel, "wos_panel"):
                setattr(self.main_panel, "wos_panel", wos_stats.WordsOrder(self.main_panel, self.nodes))
                self.main_sizer.Add(getattr(self.main_panel, "wos_panel"), 0, wx.ALL | wx.ALIGN_LEFT, 10)
                self.main_panel.SetSizer(self.main_sizer)
                self.main_panel.Layout()
                self.main_panel.SetupScrolling(scrollToTop=False)
                self.main_panel.Scroll(-1, self.main_panel.GetScrollRange(wx.VERTICAL))
        else:
            if hasattr(self.main_panel, "wos_panel"):
                self.main_panel.wos_panel.Destroy()
                delattr(self.main_panel, "wos_panel")
                self.main_panel.SetSizer(self.main_sizer)
                self.main_panel.Layout()
        if self.dist:
            if not hasattr(self.main_panel, "dist_panel"):
                setattr(self.main_panel, "dist_panel", dist_stats.Distance(self.main_panel, self.nodes))
                self.main_sizer.Add(getattr(self.main_panel, "dist_panel"), 0, wx.ALL | wx.ALIGN_LEFT, 10)
                self.main_panel.SetSizer(self.main_sizer)
                self.main_panel.Layout()
                self.main_panel.SetupScrolling(scrollToTop=False)
                self.main_panel.Scroll(-1, self.main_panel.GetScrollRange(wx.VERTICAL))
        else:
            if hasattr(self.main_panel, "dist_panel"):
                self.main_panel.dist_panel.Destroy()
                delattr(self.main_panel, "dist_panel")
                self.main_panel.SetSizer(self.main_sizer)
                self.main_panel.Layout()
        if self.feat:
            if not hasattr(self.main_panel, "feat_panel"):
                setattr(self.main_panel, "feat_panel", feat_stats.Features(self.main_panel, self.nodes))
                self.main_sizer.Add(getattr(self.main_panel, "feat_panel"), 0, wx.ALL | wx.ALIGN_LEFT, 10)
                self.main_panel.SetSizer(self.main_sizer)
                self.main_panel.Layout()
                self.main_panel.SetupScrolling(scrollToTop=False)
                self.main_panel.Scroll(-1, self.main_panel.GetScrollRange(wx.VERTICAL))
        else:
            if hasattr(self.main_panel, "feat_panel"):
                self.main_panel.feat_panel.Destroy()
                delattr(self.main_panel, "feat_panel")
                self.main_panel.SetSizer(self.main_sizer)
                self.main_panel.Layout()
        if hasattr(self.main_panel, "btn_submit"):
            self.main_panel.btn_submit.Destroy()
            delattr(self.main_panel, "btn_submit")
        setattr(self.main_panel, "btn_submit", wx.Button(self.main_panel, label="Submit"))
        self.main_panel.btn_submit.Bind(wx.EVT_BUTTON, self.on_submit)
        self.main_sizer.Add(self.main_panel.btn_submit, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        self.main_panel.SetSizer(self.main_sizer)
        self.main_panel.Layout()

    def on_submit(self, event):
        """
        This function shows the frame in which are listed all the results about the statistics chosen by the user
        """
        setattr(self, "wo_stats_list", [])
        setattr(self, "wos_stats_list", [])
        setattr(self, "dist_stats_list", [])
        setattr(self, "feat_stats_list", [])
        if self.wo:
            for i in self.main_panel.wo_panel.ids:
                d = {}
                wo_row = getattr(self.main_panel.wo_panel, f"wo_row{i}")
                d['node1'] = wo_row.node1.GetValue()
                d['node2'] = wo_row.node2.GetValue()
                self.wo_stats_list.append(d)
        if self.wos:
            for n in self.main_panel.wos_panel.nodes:
                if getattr(self.main_panel.wos_panel, f"cb_{n}").GetValue():
                    self.wos_stats_list.append(n)
            print(self.wos_stats_list)
        if self.dist:
            for i in self.main_panel.dist_panel.ids:
                d = {}
                dist_row = getattr(self.main_panel.dist_panel, f"dist_row{i}")
                d['node1'] = dist_row.node1.GetValue()
                d['node2'] = dist_row.node2.GetValue()
                self.dist_stats_list.append(d)
        if self.feat:
            for i in self.main_panel.feat_panel.ids:
                d = {}
                feat_row = getattr(self.main_panel.feat_panel, f"feat_row{i}")
                d['node'] = feat_row.node.GetValue()
                d['feat'] = feat_row.feat.GetValue()
                self.feat_stats_list.append(d)

        setattr(self, "stats_dict", {'wo': self.wo_stats_list,
                                     'wos': self.wos_stats_list,
                                     'dist': self.dist_stats_list,
                                     'feat': self.feat_stats_list})

        stats_string = ''

        for stat in self.stats_dict['wo']:
            stat_res = stats_func.wo(self.results, stat)
            stats_string += stat_res['table'] + '\n\n\n'
            self.dfs.append(stat_res['df'])

        if self.stats_dict['wos']:
            stat_res = stats_func.wos(self.results, self.stats_dict['wos'])
            stats_string += stats_res['table'] + '\n\n\n'
            self.dfs.append(stat_res['df'])

        for stat in self.stats_dict['dist']:
            stat_res = stats_func.dist(self.results, stat)
            stats_string += stat_res['table'] + '\n\n'
            stats_string += 'average distance: ' + f"{stat_res['av_dist']}" + '\n\n\n'
            self.dfs.append(stat_res['df'])

        if self.stats_dict['feat']:
            stat_res = stats_func.feat(self.results, self.stats_dict['feat'])
            stats_string += stat_res['table']
            self.dfs.append(stat_res['df'])

        stats_res_frame = stats_results_frame.StatsFrame(self, stats_string, self.dfs)


if __name__ == "__main__":
    app = wx.App()
    frame = StatsFrame(None, [{'3': 2, '1': 5}])
    app.MainLoop()
