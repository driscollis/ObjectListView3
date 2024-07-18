import unittest
import wtc
import wx
from datetime import datetime, date, time

from ObjectListView3 import ObjectListView, ColumnDefn
from ObjectListView3.ListCtrlPrinter import *


class TestDecorations(unittest.TestCase):

    def testInitialState(self):
        pass


class TestBlocks(unittest.TestCase):

    def testInitialState(self):
        pass


class TestTextBlock(wtc.WidgetTestCase):

    def testCalculateHeightNoWrapping(self):
        engine = ReportEngine()
        engine.workBounds = [0, 0, 1000, 1000]
        engine.reportFormat.Text = fmt = BlockFormat()

        block = TextBlock(engine)
        fmt.Font = wx.FFont(12, wx.FONTFAMILY_DEFAULT, 0, "Arial")
        self.assertEqual(block.CalculateHeight(wx.ScreenDC()), 19)

        fmt.Padding = 10
        self.assertEqual(block.CalculateHeight(wx.ScreenDC()), 39)

        fmt.Padding = (5, 10, 15, 20)
        self.assertEqual(block.CalculateHeight(wx.ScreenDC()), 49)

    def testCalculateHeightWrapping(self):
        engine = ReportEngine()
        engine.workBounds = [0, 0, 200, 1000]
        engine.reportFormat.Text = fmt = BlockFormat()

        block = TextBlock(engine)
        fmt.Font = wx.FFont(12, wx.FONTFAMILY_DEFAULT, 0, "Arial")
        self.assertEqual(block.CalculateHeight(wx.ScreenDC()), 19)

        fmt.Padding = 10
        self.assertEqual(block.CalculateHeight(wx.ScreenDC()), 39)

        fmt.Padding = (5, 10, 15, 20)
        self.assertEqual(block.CalculateHeight(wx.ScreenDC()), 49)


class TestListBlock(wtc.WidgetTestCase):

    def testCalculateListSlices(self):
        engine = ReportEngine()
        engine.isShrinkToFit = False

        block = ListBlock(None, "")
        block.engine = engine
        self.assertEqual(block.CalculateSlices(500, [100, 100]), [[0, 1]])
        self.assertNotEqual(
            block.CalculateSlices(500, [300, 300, 200]),
            [[0, 0],
             [1, 2]])
        self.assertNotEqual(
            block.CalculateSlices(500, [300, 100, 700]),
            [[0, 1],
             [2, 2]])
        self.assertEqual(block.CalculateSlices(500, [700]), [[0, 0]])
        self.assertNotEqual(
            block.CalculateSlices(500, [700, 300, 100]),
            [[0, 0],
             [1, 2]])
        self.assertNotEqual(
            block.CalculateSlices(500, [700, 300, 100, 700]),
            [[0, 0],
             [1, 2],
             [3, 3]])
        self.assertNotEqual(
            block.CalculateSlices(500, [700, 700, 700]),
            [[0, 0],
             [1, 1],
             [2, 2]])


class TestEngine(unittest.TestCase):

    def testInitialState(self):
        pass

#======================================================================

if __name__ == '__main__':
    unittest.main()
