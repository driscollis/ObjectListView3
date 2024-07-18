# -*- coding: utf-8 -*-
#!/usr/bin/env python

import wx

# Where can we find the ObjectListView module?
import sys
sys.path.append("..")

import ObjectListView3 as OLV                                       # noqa: E402

import ExampleModel                                                 # noqa: E402

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        self.Init()

    def Init(self):
        self.InitModel()
        self.InitWidgets()
        self.InitObjectListView()

    def InitModel(self):
        self.songs = ExampleModel.GetTracks()

    def InitWidgets(self):
        panel = wx.Panel(self, -1)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(panel, 1, wx.ALL|wx.EXPAND)
        self.SetSizer(sizer_1)

        self.myOlv = OLV.ObjectListView(panel, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(self.myOlv, 1, wx.ALL|wx.EXPAND, 4)
        panel.SetSizer(sizer_2)

        self.Layout()

    def InitObjectListView(self):
        self.myOlv.SetColumns([
            OLV.ColumnDefn("Title", "left", 120, "title"),
            OLV.ColumnDefn("Size (MB)", "center", 100, "GetSizeInMb", stringConverter="%.1f"),
            OLV.ColumnDefn("Last Played", "left", 100, "lastPlayed", stringConverter="%d-%m-%Y"),
            OLV.ColumnDefn("Rating", "center", 100, "rating")
        ])
        self.myOlv.SetObjects(self.songs)

if __name__ == '__main__':
    print('Using {} ({}) from {}.'.format(OLV.__name__, OLV.__version__, OLV.__path__))
    app = wx.App()
    frame = MyFrame(None, -1, "ObjectListView Simple Example1")
    frame.Show()
    app.MainLoop()
