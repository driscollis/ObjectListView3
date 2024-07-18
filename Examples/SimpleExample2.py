# -*- coding: utf-8 -*-
#!/usr/bin/env python

import wx

# Where can we find the ObjectListView module?
import sys
sys.path.append("..")

import ObjectListView3 as OLV                                       # noqa: E402

import ExampleModel                                                 # noqa: E402
import ExampleImages # We store our images as python code           # noqa: E402


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
        groupImage = self.myOlv.AddImages(ExampleImages.Group16.GetBitmap(), ExampleImages.Group32.GetBitmap())
        userImage = self.myOlv.AddImages(ExampleImages.User16.GetBitmap(), ExampleImages.User32.GetBitmap())
        musicImage = self.myOlv.AddImages(ExampleImages.Music16.GetBitmap(), ExampleImages.Music32.GetBitmap())

        soloArtists = ["Nelly Furtado", "Missy Higgins", "Moby", "Natalie Imbruglia",
                       "Dido", "Paul Simon", "Bruce Cockburn"]
        def artistImageGetter(track):
            if track.artist in soloArtists:
                return userImage
            else:
                return groupImage

        def sizeToNiceString(byteCount):
            """
            Convert the given byteCount into a string like: 9.9bytes/KB/MB/GB
            """
            for (cutoff, label) in [(1024*1024*1024, "GB"), (1024*1024, "MB"), (1024, "KB")]:
                if byteCount >= cutoff:
                    return "%.1f %s" % (byteCount * 1.0 / cutoff, label)

            if byteCount == 1:
                return "1 byte"
            else:
                return "%d bytes" % byteCount

        self.myOlv.SetColumns([
            OLV.ColumnDefn("Title", "left", 120, "title", imageGetter=musicImage),
            OLV.ColumnDefn("Artist", "left", 120, "artist", imageGetter=artistImageGetter),
            OLV.ColumnDefn("Size", "center", 100, "sizeInBytes", stringConverter=sizeToNiceString),
            OLV.ColumnDefn("Last Played", "left", 100, "lastPlayed", stringConverter="%d-%m-%Y"),
            OLV.ColumnDefn("Rating", "center", 100, "rating")
        ])
        self.myOlv.SetObjects(self.songs)

if __name__ == '__main__':
    print("Using {} ({}) from {}".format(OLV.__name__, OLV.__version__, OLV.__path__))
    app = wx.App()
    frame = MyFrame(None, -1, "{} ({}) Simple Example 2".format(OLV.__name__, OLV.__version__))
    frame.Show()
    app.MainLoop()
