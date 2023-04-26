import wx


class ChooseFile(wx.Panel):
    """
    Choose file panel class: shows the dialog to select the treebank file
    """
    def __init__(self, parent):
        self.parent = parent
        wx.Panel.__init__(self, parent)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.first_sizer = wx.BoxSizer(wx.HORIZONTAL)
        title = wx.StaticText(self, label="Select the treebank file -->")
        title.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.first_sizer.Add(title, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        openFileDlgBtn = wx.Button(self, label='Choose file')
        openFileDlgBtn.Bind(wx.EVT_BUTTON, self.onOpenFile)
        self.first_sizer.Add(openFileDlgBtn, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.main_sizer.Add(self.first_sizer)
        self.SetSizer(self.main_sizer)

    def onOpenFile(self, event):
        """
        Create and show the Open FileDialog
        """
        wildcard = "conllu files (*.conllu)|*.conllu|" \
                   "conll files (*.conll)|*.conll|" \
                   "All files (*.*)|*.*"

        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir="",
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR
        )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            setattr(self, 'file_path', paths[0])
        dlg.Destroy()
        if hasattr(self, "selected_file"):
            self.selected_file.Destroy()
        setattr(self, "second_sizer", wx.BoxSizer(wx.HORIZONTAL))
        setattr(self, "selected_file", wx.StaticText(self, label=f"Selected file: {getattr(self, 'file_path')}"))
        self.second_sizer.Add(self.selected_file, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.main_sizer.Add(self.second_sizer, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.main_sizer)
        self.Parent.Layout()
