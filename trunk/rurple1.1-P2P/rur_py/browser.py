# -*- coding: utf-8
""" RUR-PLE: Roberge's Used Robot - a Python Learning Environment
    browser.py - Simple html browser
        Adapted from wxPython demo code
    Version 1.0
    Author: Andre Roberge    Copyright  2005
    andre.roberge@gmail.com
    Edited by: Robert Deloatch
"""
import os.path
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import os
import conf
import wx
import wx.html as  html
import wx.lib.wxpTag
import translation
from  translation import _
import images
from images import getImage
import dialogs

#----------------------------------------------------------------------

def relPathOfPage(page):
    '''Returns the part of the URL after the language path. Used to
    switch between corresponding lessons of different languages.
    '''
    # Make sure that lessonbase has a http like path separator
    lessonbase = conf.getSettings().LESSONS_DIR.replace(os.path.sep, '/')
    if (page.startswith(lessonbase)):
        lbcount = len(lessonbase.split('/'))
        pageparts = page.split('/')
        return '/'.join(pageparts[lbcount +1:])
    else:
        return ''

class TestHtmlPanel(wx.Panel):
    def __init__(self, parent, grand_parent):

        wx.Panel.__init__(self, parent, -1, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        self.lessons_dir = conf.getLessonsNlDir()
        
        self.parent = parent
        self.grand_parent = grand_parent

        self.html = html.HtmlWindow(self, -1, style=wx.NO_FULL_REPAINT_ON_RESIZE)

        self.box = wx.BoxSizer(wx.VERTICAL)
        subbox = wx.BoxSizer(wx.HORIZONTAL)

        self.box.Add(subbox, 0, wx.GROW)
        self.box.Add(self.html, 1, wx.GROW)
        self.SetSizer(self.box)
        self.SetAutoLayout(True)

        self.name = os.path.join(self.lessons_dir, 'instr.htm')
        self.html.LoadPage(self.name)
