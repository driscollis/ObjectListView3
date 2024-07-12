import wtc
import unittest
import wx
print(wx.VERSION_STRING)
import datetime
import time

from ObjectListView2 import ObjectListView, FastObjectListView, VirtualObjectListView, GroupListView, ColumnDefn, EVT_SORT, Filter


class Person:

    def __init__(self, name, birthdate, sex):
        self.name = name
        self.birthdate = birthdate
        self.sex = sex

    def age(self):
        return datetime.datetime.now().year - self.birthdate.year

personColumns = [
    ("Name", "left", -1, "name"),
    ("Age", "right", -1, "age"),
    ColumnDefn("Birthdate", "left", 100, "birthdate"),
    ColumnDefn("Sex", "centre", -1, "sex", isSpaceFilling=True),
]

persons = [
    Person("Alex Bawling", datetime.datetime(1955, 1, 2), "Male"),
    Person("Cindy Dawn", datetime.datetime(1967, 3, 4), "Female"),
    Person("Eric Fandango", datetime.datetime(1957, 5, 6), "Male"),
    Person("Ginger Hawk", datetime.datetime(1977, 7, 8), "Female"),
    Person("Ian Janide", datetime.datetime(1931, 9, 10), "Male"),
    Person("Zoe Meliko", datetime.datetime(1974, 9, 10), "Female"),
    Person("ae cummings", datetime.datetime(1944, 9, 10), "Male"),
]


def loadOLV(olv):
    """Load the OLV with columns and data."""
    olv.SetColumns(personColumns)
    olv.SetObjects(persons)


class TestObjectListView(wtc.WidgetTestCase):

    """
    Setup of all base tests used for all types of ObjectListView's and do test the
    normal ObjectListView.

    The other ObjectListView tests just override setUp to create the appropriate ListView.
    """

    def setUp(self):
        super(TestObjectListView, self).setUp()

        panel = wx.Panel(self.frame, -1)
        self.objectListView = ObjectListView(
            panel, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        sizerPanel = wx.BoxSizer(wx.VERTICAL)
        sizerPanel.Add(self.objectListView, 1, wx.ALL | wx.EXPAND, 4)
        panel.SetSizer(sizerPanel)

        sizerFrame = wx.BoxSizer(wx.VERTICAL)
        sizerFrame.Add(panel, 1, wx.ALL | wx.EXPAND, 4)
        self.frame.SetSizer(sizerFrame)

        loadOLV(self.objectListView)

    def testInitialState(self):
        self.objectListView.ClearAll()
        self.assertEqual(self.objectListView.GetColumnCount(), 0)
        self.assertEqual(self.objectListView.GetItemCount(), 0)
        self.assertEqual(len(self.objectListView.modelObjects), 0)
        loadOLV(self.objectListView)

    def testBasicState(self):
        self.assertEqual(
            self.objectListView.GetColumnCount(),
            len(personColumns))
        self.assertEqual(self.objectListView.GetItemCount(), len(persons))

    def testSelectObject(self):
        self.objectListView.SelectObject(persons[0])
        self.assertEqual(self.objectListView.GetSelectedObject(), persons[0])

        males = [x for x in persons if x.sex == "Male"]
        self.objectListView.SelectObjects(males)
        self.assertEqual(
            set(self.objectListView.GetSelectedObjects()),
            set(males))

    def testSelectAll(self):
        self.objectListView.SelectAll()
        for i in range(0, self.objectListView.GetItemCount()):
            self.assertTrue(self.objectListView.IsSelected(i))

    def testDeSelectAll(self):
        self.objectListView.SelectAll()
        self.objectListView.DeselectAll()
        for i in range(0, self.objectListView.GetItemCount()):
            self.assertFalse(self.objectListView.IsSelected(i))

    def testGetSelectedObject(self):
        self.objectListView.SelectAll()
        self.assertEqual(self.objectListView.GetSelectedObject(), None)

        self.objectListView.DeselectAll()
        self.assertEqual(self.objectListView.GetSelectedObject(), None)

        self.objectListView.SelectObject(persons[0])
        self.assertEqual(self.objectListView.GetSelectedObject(), persons[0])

        self.objectListView.SelectObject(persons[1], False)
        self.assertEqual(self.objectListView.GetSelectedObject(), None)

    def testGetSelectedObjects(self):
        self.objectListView.SelectAll()
        self.assertEqual(
            set(self.objectListView.GetSelectedObjects()),
            set(persons))

        self.objectListView.SelectObject(persons[0])
        self.assertEqual(len(self.objectListView.GetSelectedObjects()), 1)

        self.objectListView.DeselectAll()
        self.assertEqual(len(self.objectListView.GetSelectedObjects()), 0)

    def testRefresh(self):
        rowIndex = 1
        primaryColumn = self.objectListView.GetPrimaryColumnIndex()
        person = self.objectListView[rowIndex]
        nameInList = self.objectListView.GetItem(
            rowIndex,
            primaryColumn).GetText()
        self.assertEqual(nameInList, person.name)

        person.name = "Some different name"
        self.assertNotEqual(nameInList, person.name)

        self.objectListView.RefreshObject(person)
        self.assertEqual(
            self.objectListView.GetItem(
                rowIndex,
                primaryColumn).GetText(),
            person.name)
        person.name = nameInList

    def testSorting(self):
        self.objectListView.SortBy(0, False)
        self.assertEqual(
            self.objectListView.GetItem(0).GetText(),
            "Zoe Meliko")
        self.objectListView.SortBy(0, True)
        self.assertEqual(
            self.objectListView.GetItem(0).GetText(),
            "ae cummings")
        self.objectListView.SortBy(2, False)
        self.assertEqual(
            self.objectListView.GetItem(0).GetText(),
            "Ginger Hawk")
        self.objectListView.SortBy(2, True)
        self.assertEqual(
            self.objectListView.GetItem(0).GetText(),
            "Ian Janide")

    def testColumnResizing(self):
        widths = [
            self.objectListView.GetColumnWidth(i)
            for i in range(len(self.objectListView.columns))]
        self.frame.SetSize(self.frame.GetSize() + (100, 100))
        self.objectListView.Layout()

        # The space filling columns should have increased in width, but the
        # others should be the same
        for (colIndex, oldWidth) in enumerate(widths):
            if self.objectListView.columns[colIndex].isSpaceFilling:
                self.assertTrue(
                    oldWidth < self.objectListView.GetColumnWidth(colIndex))
            else:
                self.assertEqual(
                    oldWidth,
                    self.objectListView.GetColumnWidth(colIndex))

    def testEditing(self):
        rowIndex = 1
        primaryColumnIndex = self.objectListView.GetPrimaryColumnIndex()
        self.objectListView.cellEditMode = ObjectListView.CELLEDIT_F2ONLY
        # self.objectListView.SortBy(primaryColumnIndex+1)

        originalName = self.objectListView[rowIndex].name
        self.assertEqual(
            self.objectListView.GetItem(
                rowIndex,
                primaryColumnIndex).GetText(),
            originalName)
        self.objectListView.DeselectAll()
        self.objectListView.SetItemState(
            rowIndex,
            wx.LIST_STATE_SELECTED | wx.LIST_STATE_FOCUSED,
            wx.LIST_STATE_SELECTED | wx.LIST_STATE_FOCUSED)

        # Fake an F2, change the value of the edit, and then fake a Return to
        # commit the change
        evt = wx.KeyEvent(wx.EVT_CHAR.evtType[0])
        evt.m_keyCode = wx.WXK_F2
        self.objectListView._HandleChar(evt)
        self.objectListView.StartCellEdit(rowIndex, primaryColumnIndex)
        self.objectListView.cellEditor.SetValue("new name for X")
        self.objectListView.FinishCellEdit()
        evt.m_keyCode = wx.WXK_RETURN
        self.objectListView._HandleChar(evt)
        self.assertEqual(
            self.objectListView.GetItem(
                rowIndex,
                primaryColumnIndex).GetText(),
            "new name for X")

        # Put the original value back
        evt.m_keyCode = wx.WXK_F2
        self.objectListView._HandleChar(evt)
        self.objectListView.StartCellEdit(rowIndex, primaryColumnIndex)
        self.objectListView.cellEditor.SetValue(originalName)
        self.objectListView.FinishCellEdit()
        evt.m_keyCode = wx.WXK_RETURN
        self.objectListView._HandleChar(evt)
        self.assertEqual(
            self.objectListView.GetItem(
                rowIndex,
                primaryColumnIndex).GetText(),
            originalName)

    def testLackOfCheckboxes(self):
        self.objectListView.InstallCheckStateColumn(None)

        firstObject = self.objectListView[0]
        self.assertIn(self.objectListView.IsChecked(firstObject), (None, False))

        self.assertEqual(self.objectListView.GetCheckedObjects(), list())

        self.objectListView.Check(firstObject)
        self.assertIn(self.objectListView.IsChecked(firstObject), (None, False))

    def testCreateCheckStateColumn(self):
        self.objectListView.InstallCheckStateColumn(None)

        firstObject = self.objectListView[0]
        self.assertIn(self.objectListView.IsChecked(firstObject), (False, None))

        self.objectListView.CreateCheckStateColumn()
        self.objectListView.Check(firstObject)
        self.assertEqual(self.objectListView.IsChecked(firstObject), True)

    def testAutoCheckboxes(self):
        col = ColumnDefn("Check")
        self.objectListView.AddColumnDefn(col)
        self.assertTrue(col.checkStateGetter is None)
        self.assertTrue(col.checkStateSetter is None)

        self.objectListView.InstallCheckStateColumn(col)
        self.assertTrue(col.checkStateGetter is not None)
        self.assertTrue(col.checkStateSetter is not None)

        object = self.objectListView[0]
        self.assertEqual(self.objectListView.IsChecked(object), False)

        self.objectListView.Check(object)
        self.assertEqual(self.objectListView.IsChecked(object), True)

    def testCheckboxes(self):
        def myGetter(modelObject):
            return getattr(modelObject, "isChecked", False)

        def mySetter(modelObject, newValue):
            modelObject.isChecked = newValue
        self.objectListView.SetImageLists()
        col = ColumnDefn(
            "Check",
            checkStateGetter=myGetter,
            checkStateSetter=mySetter)
        self.objectListView.AddColumnDefn(col)
        self.assertEqual(self.objectListView.checkStateColumn, col)

        firstObject = self.objectListView[1]
        lastObject = self.objectListView[4]
        self.assertEqual(self.objectListView.IsChecked(firstObject), False)
        self.assertEqual(self.objectListView.IsChecked(lastObject), False)

        self.objectListView.Check(firstObject)
        self.assertEqual(self.objectListView.IsChecked(firstObject), True)
        self.assertEqual(self.objectListView.IsChecked(lastObject), False)

        self.objectListView.Check(lastObject)
        self.assertEqual(self.objectListView.IsChecked(firstObject), True)
        self.assertEqual(self.objectListView.IsChecked(lastObject), True)
        if not isinstance(self.objectListView, VirtualObjectListView):
            self.assertEqual(
                set(self.objectListView.GetCheckedObjects()),
                set([firstObject, lastObject]))

        self.objectListView.Uncheck(firstObject)
        self.assertEqual(self.objectListView.IsChecked(firstObject), False)
        self.assertEqual(self.objectListView.IsChecked(lastObject), True)

        self.objectListView.ToggleCheck(lastObject)
        self.assertEqual(self.objectListView.IsChecked(firstObject), False)
        self.assertEqual(self.objectListView.IsChecked(lastObject), False)

    def testNoAlternateColours(self):
        # When there is no alternate colors, each row's background colour
        # should be invalid
        self.objectListView.useAlternateBackColors = False
        self.objectListView.RepopulateList()
        bkgdColours = [
            self.getBackgroundColour(i).GetIM()
            for i in range(self.objectListView.GetItemCount())]
        self.assertFalse(
            self.objectListView.oddRowsBackColor.GetIM() in set(bkgdColours))
        self.assertFalse(
            self.objectListView.evenRowsBackColor.GetIM() in set(bkgdColours))

    def testAlternateColours(self):
        self.objectListView.useAlternateBackColors = True
        self.objectListView.RepopulateList()
        for i in range(self.objectListView.GetItemCount()):
            if i & 1:
                self.assertEqual(
                    self.objectListView.oddRowsBackColor,
                    self.getBackgroundColour(i))
            else:
                self.assertEqual(
                    self.objectListView.evenRowsBackColor,
                    self.getBackgroundColour(i))

    def getBackgroundColour(self, i):
        # There is no consistent way to get the background color of an item (i.e. one that
        # works on both normal and virtual lists) so we have to split this into a method
        # so we can change it for a virtual list
        return self.objectListView.GetItemBackgroundColour(i)

    def testEmptyListMsg(self):
        self.objectListView.SetObjects(None)
        self.assertTrue(self.objectListView.stEmptyListMsg.IsShown())

        self.objectListView.SetObjects(persons)
        self.assertFalse(self.objectListView.stEmptyListMsg.IsShown())

    def testFilteringHead(self):
        self.objectListView.SetFilter(Filter.Head(1))
        self.objectListView.SetObjects(persons)
        self.assertEqual(len(self.objectListView.GetFilteredObjects()), 1)
        self.assertEqual(
            self.objectListView.GetFilteredObjects()[0],
            persons[0])

        self.objectListView.SetFilter(None)

    def testFilteringTail(self):
        self.objectListView.SetFilter(Filter.Tail(1))
        self.objectListView.SetObjects(persons)
        # The group list will have a group header at row 0 so skip it
        if isinstance(self.objectListView, GroupListView):
            firstDataIndex = 1
        else:
            firstDataIndex = 0
        self.assertEqual(len(self.objectListView.GetFilteredObjects()), 1)
        self.assertEqual(
            self.objectListView.GetFilteredObjects()[0],
            persons[-1])

        self.objectListView.SetFilter(None)

    def testFilteringPredicate(self):
        males = [x for x in persons if x.sex == "Male"]
        self.objectListView.SetFilter(
            Filter.Predicate(
                lambda person: person.sex == "Male"))
        self.objectListView.SetSortColumn(personColumns[-1])
        self.objectListView.SetObjects(persons)

        self.assertEqual(
            set(self.objectListView.GetFilteredObjects()),
            set(males))

        self.objectListView.SetFilter(None)

    def testFilteringTextSearch(self):
        containsF = [
            x for x in persons
            if "f" in x.sex.lower() or "f" in x.name.lower()]

        self.objectListView.SetFilter(
            Filter.TextSearch(
                self.objectListView,
                text="f"))
        self.objectListView.SetObjects(persons)
        self.assertEqual(
            set(self.objectListView.GetFilteredObjects()),
            set(containsF))

        self.objectListView.SetFilter(None)

    def testFilteringChain(self):
        filterMale = Filter.Predicate(lambda person: person.sex == "Male")
        filterContainsF = Filter.TextSearch(self.objectListView, text="f")
        self.objectListView.SetFilter(
            Filter.Chain(
                filterMale,
                filterContainsF))
        self.objectListView.SetObjects(persons)
        self.assertEqual(len(self.objectListView.GetFilteredObjects()), 1)
        self.assertEqual(
            self.objectListView.GetFilteredObjects()[0].name,
            "Eric Fandango")

        self.objectListView.SetFilter(None)


class TestFastObjectListView(TestObjectListView):

    def setUp(self):
        super(TestFastObjectListView, self).setUp()

        panel = wx.Panel(self.frame, -1)
        self.objectListView = FastObjectListView(
            panel, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        sizerPanel = wx.BoxSizer(wx.VERTICAL)
        sizerPanel.Add(self.objectListView, 1, wx.ALL | wx.EXPAND, 4)
        panel.SetSizer(sizerPanel)

        sizerFrame = wx.BoxSizer(wx.VERTICAL)
        sizerFrame.Add(panel, 1, wx.ALL | wx.EXPAND, 4)
        self.frame.SetSizer(sizerFrame)

        loadOLV(self.objectListView)

    #-------------------------------------------------------------------------
    # Override inherited tests

    def getBackgroundColour(self, i):
        # There is no direct way to get the background colour of an item in a virtual
        # list, so we have to cheat by approximating the process of building a
        # list item
        attr = self.objectListView.OnGetItemAttr(i)
        if attr is None or not attr.HasBackgroundColour():
            # this returns an invalid color
            return self.objectListView.GetItemBackgroundColour(i)
        else:
            return attr.GetBackgroundColour()


class TestVirtualObjectListView(TestObjectListView):

    def setUp(self):
        super(TestVirtualObjectListView, self).setUp()

        panel = wx.Panel(self.frame, -1)
        self.objectListView = VirtualObjectListView(
            panel, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        sizerPanel = wx.BoxSizer(wx.VERTICAL)
        sizerPanel.Add(self.objectListView, 1, wx.ALL | wx.EXPAND, 4)
        panel.SetSizer(sizerPanel)

        sizerFrame = wx.BoxSizer(wx.VERTICAL)
        sizerFrame.Add(panel, 1, wx.ALL | wx.EXPAND, 4)
        self.frame.SetSizer(sizerFrame)

        loadOLV(self.objectListView)
        # need to set item count for this one
        self.objectListView.SetItemCount(len(persons))

        self.objectListView.SetObjectGetter(lambda i: persons[i])
        self.objectListView.Bind(EVT_SORT, self._handleSort)

    def _handleSort(self, evt):
        col = evt.objectListView.columns[evt.sortColumnIndex]

        def _getLowerCaseSortValue(x):
            value = col.GetValue(x)
            if isinstance(value, str):
                return value.lower()
            else:
                return value

        persons.sort(
            key=_getLowerCaseSortValue,
            reverse=(
                not evt.sortAscending))
        evt.objectListView.RefreshObjects()

    #-------------------------------------------------------------------------
    # Override inherited tests

    def getBackgroundColour(self, i):
        # There is no direct way to get the background colour of an item in a virtual
        # list, so we have to cheat by approximating the process of building a
        # list item
        attr = self.objectListView.OnGetItemAttr(i)
        if attr is None or not attr.HasBackgroundColour():
            # this returns an invalid color
            return self.objectListView.GetItemBackgroundColour(i)
        else:
            return attr.GetBackgroundColour()

    def testEmptyListMsg(self):
        self.objectListView.SetItemCount(0)
        self.assertTrue(self.objectListView.stEmptyListMsg.IsShown())

        self.objectListView.SetItemCount(len(persons))
        self.assertFalse(self.objectListView.stEmptyListMsg.IsShown())

    # Virtual lists can't get or set selected objects -- Is this really true?
    # Does it have to be?
    def testSelectObject(self):
        pass

    def testGetSelectedObject(self):
        pass

    def testGetSelectedObjects(self):
        pass

    # Virtual lists can't filter since the model objects are not controlly by
    # it
    def testFilteringHead(self):
        pass

    def testFilteringTail(self):
        pass

    def testFilteringPredicate(self):
        pass

    def testFilteringTextSearch(self):
        pass

    def testFilteringChain(self):
        pass


class TestGroupObjectListView(TestObjectListView):

    def setUp(self):
        super(TestGroupObjectListView, self).setUp()

        panel = wx.Panel(self.frame, -1)
        self.objectListView = GroupListView(
            panel, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        sizerPanel = wx.BoxSizer(wx.VERTICAL)
        sizerPanel.Add(self.objectListView, 1, wx.ALL | wx.EXPAND, 4)
        panel.SetSizer(sizerPanel)

        sizerFrame = wx.BoxSizer(wx.VERTICAL)
        sizerFrame.Add(panel, 1, wx.ALL | wx.EXPAND, 4)
        self.frame.SetSizer(sizerFrame)

        loadOLV(self.objectListView)

    #-------------------------------------------------------------------------
    # Override inherited tests

    def testBasicState(self):
        self.assertEqual(
            self.objectListView.GetColumnCount(),
            len(personColumns) + 1)
        self.assertEqual(
            self.objectListView.GetItemCount(),
            len(persons) + len(self.objectListView.groups) * 2 - 1)

    def testSorting(self):
        # Sorting within a GroupListView is completely different from an
        # ObjectListView
        pass

    def testSelectAll(self):
        self.objectListView.SelectAll()
        for i in range(0, self.objectListView.GetItemCount()):
            if self.objectListView.GetObjectAt(i):
                self.assertTrue(self.objectListView.IsSelected(i))

    def testAlternateColours(self):
        # Not ever row has alternate colours -- only those for model objects
        self.objectListView.useAlternateBackColors = True
        self.objectListView.RepopulateList()
        for i in range(self.objectListView.GetItemCount()):
            if self.objectListView.GetObjectAt(i):
                if i & 1:
                    self.assertEqual(
                        self.objectListView.oddRowsBackColor,
                        self.getBackgroundColour(i))
                else:
                    self.assertEqual(
                        self.objectListView.evenRowsBackColor,
                        self.getBackgroundColour(i))

    def getBackgroundColour(self, i):
        # There is no direct way to get the background colour of an item in a virtual
        # list, so we have to cheat by approximating the process of building a
        # list item
        attr = self.objectListView.OnGetItemAttr(i)
        if attr is None or not attr.HasBackgroundColour():
            # this returns an invalid color
            return self.objectListView.GetItemBackgroundColour(i)
        else:
            return attr.GetBackgroundColour()


if __name__ == '__main__':
    unittest.main()
