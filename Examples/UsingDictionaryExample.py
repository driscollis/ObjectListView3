#!/usr/bin/env python

"""
This example shows how to use a list of dictionaries as the
datasource for an ObjectListView
"""

import wx

# Where can we find the ObjectListView module?
import sys
sys.path.append("..")

import ObjectListView3 as OLV                                       # noqa: E402

# We store our images as python code
import ExampleImages                                                # noqa: E402

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        self.Init()

    def Init(self):
        self.InitModel()
        self.InitWidgets()
        self.InitObjectListView()

    def InitModel(self):
        self.listOfDictionaries = [
            { "title":"Shiver", "artist": "Natalie Imbruglia", "album":"Counting Down the Days"},
            { "title":"Who's Gonna Ride Your Wild Horses", "artist": "U2",  "album":"Achtung Baby"},
            { "title":"So Cruel", "artist": "U2",  "album":"Achtung Baby"},
            { "title":"The Fly", "artist": "U2",  "album":"Achtung Baby"},
            { "title":"Fight For All The Wrong Reason", "artist": "Nickelback",  "album":"All The Right Reasons"},
            { "title":"Photograph", "artist": "Nickelback",  "album":"All The Right Reasons"},
            { "title":"Animals", "artist": "Nickelback",  "album":"All The Right Reasons"},
            { "title":"Savin' Me", "artist": "Nickelback",  "album":"All The Right Reasons"},
            { "title":"Far Away", "artist": "Nickelback",  "album":"All The Right Reasons"},
            { "title":"Next Contestant", "artist": "Nickelback",  "album":"All The Right Reasons"},
            { "title":"My Girl", "artist": "Hoodoo Gurus",  "album":"Ampology"},
            { "title":"Be My Guru", "artist": "Hoodoo Gurus",  "album":"Ampology"},
            { "title":"I Want You Back", "artist": "Hoodoo Gurus",  "album":"Ampology"},
            { "title":"Dare you to move", "artist": "Switchfoot",  "album":"The Beautiful Letdown"},
            { "title":"Redemption", "artist": "Switchfoot",  "album":"The Beautiful Letdown"},
            { "title":"The beautiful letdown", "artist": "Switchfoot",  "album":"The Beautiful Letdown"},
        ]

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

        soloArtists = ["Nelly Furtado", "Missy Higgins", "Moby", "Natalie Imbruglia"]
        def artistImageGetter(track):
            if track["artist"] in soloArtists:
                return userImage
            else:
                return groupImage

        self.myOlv.SetColumns([
            OLV.ColumnDefn("Title", "left", -1, "title", imageGetter=musicImage),
            OLV.ColumnDefn("Artist", "left", -1, "artist", imageGetter=artistImageGetter),
            OLV.ColumnDefn("Album", "center", -1, "album")
        ])
        self.myOlv.SetObjects(self.listOfDictionaries)

if __name__ == '__main__':
    print('Using {} ({}) from {}.'.format(OLV.__name__, OLV.__version__, OLV.__path__))
    app = wx.App()
    wx.InitAllImageHandlers()
    frame = MyFrame(None, -1, "ObjectListView Dictionary Example")
    frame.Show()
    app.MainLoop()
