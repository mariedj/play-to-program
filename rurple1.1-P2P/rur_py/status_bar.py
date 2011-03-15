# -*- coding: utf-8
""" RUR-PLE: Roberge's Used Robot - a Python Learning Environment
    status_bar.py - Status bar information at bottom of Robot: Code and Learn
    Version 0.8.7
    Author: Andre Roberge    Copyright  2005
    andre.roberge@gmail.com
"""

import wx
import event_manager
from translation import _

class rurStatusBar(wx.StatusBar):
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent, -1)
        event_manager.myEVT_StatusBarChanged(parent, self.UpdateFields)
        # status bar with four fields, of equal widths
        self.SetFieldsCount(4)
        self.SetStatusWidths([-1, -1, -1, -1])

        self.no_robot = -1
        self.problem_field = 0
        self.running_field = 1
        self.beeper_field = 2
        self.world_field = 3
        self.user_field = 4

        # Initial values for the fields
        self.prob_text = _("No problem loaded")
        self.run_text = _("Program not running")
        self.beeper_text = _("Robot has %s beeper")%0
        self.world_text = _("Default world")
        self.user_text = _("Default User")

        #=== when changing language
        self.running_dict = {'0': _("Program not running"),
                             '1': _("Program is running"),
                             '2':  _("Program paused")}
        self.fields_info = { 'problem': '', 'running': '0', 'user':'',
                             'beepers' : 0, 'world': '', 'robot': 1}

        #===================================

        self.notebook_new_page = 99

    def ClearFields(self):
        for field in range(5):
            self.SetStatusText('', field)

    def WriteFields(self):
        self.SetStatusText(self.prob_text, self.problem_field)
        self.SetStatusText(self.run_text, self.running_field)
        self.SetStatusText(self.beeper_text, self.beeper_field)
        self.SetStatusText(self.world_text, self.world_field)
        self.SetStatusText(self.user_text, self.user_field)


    def UpdateFields(self, *args):
        field, info = args[0].data[0]
        if field == self.notebook_new_page:
            if info != 1:  # Code and Learn page
                self.ClearFields()
                return
        elif field == self.beeper_field:
            self.fields_info['beepers'] = info
            if info == self.no_robot:
                self.beeper_text = _("No robot in this world")
                self.fields_info['robot'] = self.no_robot
            else:
                self.fields_info['robot'] = self.no_robot+1
                if info < 2:
                    self.beeper_text = _("Robot has %s beeper") % info
                else:
                    self.beeper_text = _("Robot has %s beepers") % info
        elif field == self.running_field:
            self.run_text = info
            for n in ['0', '1', '2']:
                if info == self.running_dict[n]:
                    self.fields_info['running'] = n
        elif field == self.world_field:
            self.world_text = _("World file: %s") % info
            self.fields_info['world'] = info
        elif field == self.problem_field:
            self.prob_text = _("Problem: %s") % info
            self.fields_info['problem'] = info
        elif field == self.user_field:
            self.user_text = _("User ID: %s") % info
            self.fields_info['user'] = info
        self.WriteFields()

