# ObjectListView3

This is a fork of olv 1.3.2 from https://bitbucket.org/wbruhin/objectlistview/src/default/ 


*An ObjectListView is a wrapper around the wx.ListCtrl that makes the
list control easier to use. It also provides some useful extra functionality.*

Larry Wall, the author of Perl, once wrote that the three essential character flaws of any
good programmer were sloth, impatience and hubris. Good programmers want to do the minimum
amount of work (sloth). They want their programs to run quickly (impatience). They take
inordinate pride in what they have written (hubris).

ObjectListView encourages the vices of sloth and hubris, by allowing programmers to do far
less work but still produce great looking results.


## Without wasting my time, just tell me what it does!

OK, here's the bullet point feature list:

* Automatically transforms a collection of model objects into a fully functional wx.ListCtrl.
* Automatically sorts rows by clicking on the column header (right-click cancels sorting).
* Easily edits the cell values.
* Supports all ListCtrl views (report, list, large and small icons).
* Columns can be fixed-width, have a minimum and/or maximum width, or be space-filling.
* Displays a "list is empty" message when the list is empty (obviously).
* Supports checkboxes in any column
* Supports alternate rows background colors.
* Supports custom formatting of rows.
* Supports searching (by typing) on any column, even on massive lists.
* Supports custom sorting
* The `FastObjectListView` version can build a list of 10,000 objects in less than 0.1 seconds.
* The `VirtualObjectListView` version supports millions of rows through ListCtrl's virtual mode.
* The `GroupListView` version supports arranging rows into collapsible groups.
* Effortlessly produce professional-looking reports using a ListCtrlPrinter.

Seriously, after using an ObjectListView, you will never go back to using a plain wx.ListCtrl.


## OK, I'm interested. What do I do next?


As Phillip has not updated the Python version for a long time I created this fork as I want to
use it with wxPython 2.9+ and wxPython 3.x Phoenix on both Python 2.x and 3.x.

To install this version, you can run the following command:

```
python -m pip install ObjectListView3
```

