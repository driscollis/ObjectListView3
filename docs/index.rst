.. -*- coding: UTF-8 -*-
.. include:: _substitutions.txt

==============
ObjectListView
==============

.. rubric:: An ObjectListView is a wrapper around the wx.ListCtrl that makes the
   list control easier to use. It also provides some useful extra functionality.

Larry Wall, the author of Perl, once wrote that the three essential character flaws of any
good programmer were sloth, impatience and hubris. Good programmers want to do the minimum
amount of work (sloth). They want their programs to run quickly (impatience). They take
inordinate pride in what they have written (hubris).

ObjectListView encourages the vices of sloth and hubris, by allowing programmers to do far
less work but still produce great looking results.

Without wasting my time, just tell me what it does!
---------------------------------------------------

OK, here's the bullet point feature list:

* Automatically transforms a collection of model objects into a fully functional wx.ListCtrl.
* Automatically sorts rows by clicking on the column header (right-click cancels sorting).
* Easily :ref:`edit the cell values <cell-editing-label>`.
* Supports all ListCtrl views (report, list, large and small icons).
* Columns can be fixed-width, have a minimum and/or maximum width, or be space-filling (:ref:`Column Widths <column-widths>`)
* Displays a :ref:`"list is empty" message <recipe-emptymsg>` when the list is empty (obviously).
* Supports :ref:`checkboxes in any column <recipe-checkbox>`
* Supports :ref:`alternate rows background colors <alternate-row-backgrounds>`.
* Supports :ref:`custom formatting of rows <recipe-formatter>`.
* Supports :ref:`searching (by typing) on any column <search-by-typing>`, even on massive lists.
* Supports custom sorting
* Supports :ref:`filtering` and :ref:`batched updates <recipe-batched-updates>`
* The ``FastObjectListView`` version can build a list of 10,000 objects in less than 0.1 seconds.
* The ``VirtualObjectListView`` version supports millions of rows through ListCtrl's virtual mode.
* The :ref:`GroupListView <using-grouplistview>` version supports arranging rows into collapsible groups.
* Effortlessly produce professional-looking reports using a :ref:`ListCtrlPrinter <using-listctrlprinter>`.

Seriously, after using an ObjectListView, you will never go back to using a plain wx.ListCtrl.

OK, I'm interested. What do I do next?
--------------------------------------

You can install it using pip::

   pip install objectlistview

or you can download a source package from |download|_, select one of the version tags or `tip`
for the current development version, if you are not a developer it is recommended that you download
the most recent version.  To install it to your installed Python version run `setup.py install` from
the base folder.

After that, you might want to look at the :ref:`Getting Started
<getting-started-label>` and the :ref:`Cookbook <cookbook-label>` sections. Please make
sure you have read and understood these sections before asking questions in the Forums.

At some point, you will want to do something with an ObjectListView and it won't be
immediately obvious how to make it happen. After dutifully scouring the :ref:`Getting
Started <getting-started-label>` and the :ref:`Cookbook <cookbook-label>` sections, you
decide that is is still not obvious.

It may even be possible that you might find some undocumented features in the code (also
known as bugs). These "features" can be reported and tracked on the |IssueTracker|.

Please do not use the old address on SourceForge which you might come across on Google or other
sources.

If you have a question you might ask on |StackExchange| or on the
`wxPython-users list <wxpython-users@googlegroups.com>`_.

Bleeding-edge source
--------------------

If you are a very keen developer, you can access the Bitbucket repository directly for this
project. The following hg command will fetch the most recent version from the repository.

Using ssh::

 hg clone ssh://hg@bitbucket.org/wbruhin/objectlistview

Using https::

  hg clone https://wbruhin@bitbucket.org/wbruhin/objectlistview

The 101 about Bitbucket can be found `here <https://confluence.atlassian.com/display/BITBUCKET/Bitbucket+101;jsessionid=880D3872C3FC71C236B6EC986C2AF5A5.node2>`_.

Please remember that code within Bitbucket is bleeding edge. It has not been well-tested and
is almost certainly full of bugs. If you just want to play with the ObjectListView, it's
better to stay with the official releases, where the bugs are (hopefully) less obvious.

Site contents
-------------

.. toctree::
   :maxdepth: 1

   whatsnew
   features
   gettingStarted
   recipes
   Recipe - Cell Editing <cellEditing>
   groupListView
   listCtrlPrinter
   faq
   majorClasses
   changelog
