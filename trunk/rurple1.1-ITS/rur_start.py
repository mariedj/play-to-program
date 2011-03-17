#!/usr/bin/env python
# -*- coding: utf-8
""" RUR-PLE: Roberge's Used Robot - a Python Learning Environment
    rur_start.py - "Main" file for RUR-PLE.
    Version 1.0
    Author: André Roberge    Copyright  2006
    andre.roberge@gmail.com
"""
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

# todo: consider adding support for translation of commands e.g.
# todo: ...  francais()  initialises commands equivalent like avance(), etc.
# todo: create easy install for windows (exe file)
# todo: create easy install for linux  (setup.py...)
# todo: consider adding new page in notebook for turtle graphics.

import os
import sys
import random
from difflib import Differ

# Change directory so that rur-ple can be started from everywhere.
try:
    appdir = os.path.dirname(sys.argv[0])
    if appdir != '':
        os.chdir(appdir)
    sys.path.append(os.getcwd())
    from rur_py import conf
    conf.getSettings()
except OSError, e:
    print 'Cannot change to rur-ple directory.'
    sys.exit(1)

from rur_py.translation import _
import rur_py.conf as conf  # a few global variables
import rur_py.wxutils as wxutils

# do not check version when make a 'bundle' of the application
# ref: http://www.wxpython.org/docs/api/wxversion-module.html
if not hasattr(sys, 'frozen'):
    if wxutils.wxversiontuple() < (2,6):
        print _("wxPython versions less than 2.6 are not supported.")
        sys.exit(1)

import wx
import wx.lib.buttons
import wx.py as py           # For the interpreter
import wx.html as html

import rur_py.images as images # load all images
from rur_py.images import getImage
import rur_py.dialogs as dialogs # contains dialogs and exception classes

from rur_py.sash import MySashWindow
from rur_py.lightning import EditorSashWindow
from rur_py.lightning import rur_editor
import rur_py.parser as parser
from rur_py.bouton import pythonChoiceWindow

from rur_py.cpu import rur_program
import rur_py.browser as browser
import rur_py.event_manager as event_manager
from rur_py.status_bar import rurStatusBar

import rur_py.questions as questions
import rur_py.problems as problems
import rur_py.student as student

# global variables defined for convenience
code = "" # contains user program
logData = True # save data from all problems attempted by user
logDataDir = conf.getUserDir() # root location to store user data and logs
user_id = 0

class RURnotebook(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, -1)
        self.parent = parent
        wx.EVT_NOTEBOOK_PAGE_CHANGED(self, -1, self.OnPageChanged)

    def OnPageChanged(self, event):
        status_bar = self.parent.status_bar
        # status_bar is dead during shutdown so check if it's alive.
        if status_bar:
            arg = status_bar.notebook_new_page, event.GetSelection()
            event_manager.SendCustomEvent(self.parent, arg)
            event.Skip()

class RURApp(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 
                          _("RUR: a Python Learning Environment"),
                          size = (settings.SCREEN[0], settings.SCREEN[1]),
                          style=wx.DEFAULT_FRAME_STYLE)
        self.raw_code = ""
        self.filename = ""
        self.world_filename = ""
        self.status_bar = rurStatusBar(self)
        self.SetStatusBar(self.status_bar)

        # icon on top left of window
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(getImage(images.ICON))
        self.SetIcon(icon)
        #
        self.Show(True)
        self.window = RURnotebook(self)
        #
        win = browser.TestHtmlPanel(self.window, self)
        self.window.AddPage(win, _("  RUR: Read and Learn  "))
        #
        self.sash = MySashWindow(self.window, self)
        
        self.outputWindow = self.sash.output_window
        
        self.window.AddPage(self.sash, _("Robot: Code and Learn"))
        # See MySashWindow for the following 'shortcut' notation
        self.world = self.WorldDisplay.world
        # create a backup copy that will be used to "reset" the world
        self.backup_dict = {}
        self.backup_dict['avenues'] = self.world.av
        self.backup_dict['streets'] = self.world.st
        self.backup_dict['beepers'] = {}
        self.backup_dict['walls'] = []
        # add a robot to start
        self.world.addOneRobot(name='robot')
        self.backup_dict['robot'] = self.world.robot_dict[
                                                    'robot']._getInfoTuple()
        # create user_program object as a two-step process: create Singleton
        self.user_program = rur_program()
        # binds attributes explicitly
        self.user_program.myInit(self, self.world, self.WorldDisplay,
                               self.ProgramEditor, self.world.robot_dict)
        # We will then be able to "link" to the one rur_program() without
        # having to worry about changing attributes
        # recreate the image so that the robot shows up.
        self.world.DoDrawing()
        self.WorldDisplay.drawImage()
        self.WorldDisplay.Refresh()
        #
        if logData:
            self.wlddir = os.path.join(logDataDir, 'StudentFiles', 'Worlds')
            self.rurdir = os.path.join(logDataDir, 'StudentFiles', 'SourceCode')
            self.predir = os.path.join(logDataDir, 'StudentFiles', 'Predictions')
            self.logdir = os.path.join(logDataDir, 'StudentFiles', 'Logs')
            self.tstdir = os.path.join(logDataDir, 'StudentFiles', 'Tests')
            for dir in (self.wlddir, self.rurdir, self.predir, self.logdir, self.tstdir):
                try:
                    os.makedirs(dir)
                except OSError:
                    pass
            self.logfile = open(os.path.join(self.logdir, str(user_id) + '_problems.txt'), 'w')
        #
        self.traceMode = False
        if 'aps' in sys.argv:
            self.stud = student.APS_Student(problems.tracing)
        elif 'fps' in sys.argv:
            self.stud = student.FPS_Student(problems.tracing)
        else:
            self.stud = student.Student(problems.tracing)
        self.prepost = False
        if not 'skip' in sys.argv:
            self.prepost = True
            if logData:
                f1 = open(os.path.join(self.logdir, str(user_id) + '_pretest.txt'), 'w')
                f2 = open(os.path.join(self.tstdir, str(user_id) + '_pretest.txt'), 'w')
            for i, question in enumerate(questions.pre):
                self.stud.external(question)
                correct = question.check()
                if correct:
                    self.stud.succ()
                else:
                    self.stud.fail()
                if logData:
                    f1.write(str(i) + ',' + str(correct) + '\n')
                    f2.write(repr(question.answer) + '\n')
            if logData:
                f1.close()
                f2.close()
        self.problemNumber = 0
        arg = self.status_bar.user_field, str(user_id)
        event_manager.SendCustomEvent(self, arg)
        #
        win = py.shell.Shell(self.window, -1,
                            introText = "")
        self.window.AddPage(win, _("Python: Code and Learn"))

        self.sash2 = EditorSashWindow(self.window, grand_parent=self,
                                      controller=pythonChoiceWindow,
                 top_control=True, top_control_height=40)    
                # 40 = bouton "." btn_size[1] + 8
        self.window.AddPage(self.sash2, _("Python: simple editor"))

        self.SetSize((settings.SCREEN[0], settings.SCREEN[1]))
        self.window.SetFocus()
        self.SendSizeEvent()  # added to attempt to solve problem on MacOS
        wx.EVT_CLOSE(self, self.OnClose)

    def OnClose(self, event):
        if self.ProgramEditor.GetModify():
                ret = dialogs.messageDialog(_(u'Save changes to %s?')
                    % unicode(self.filename), _("About to close"), wx.YES
                    | wx.NO | wx.CANCEL | wx.ICON_QUESTION | wx.STAY_ON_TOP)
                if ret == wx.ID_YES:
                    if len(self.filename) > 0:
                        try:
                            f = open(self.filename, 'w')
                            f.write(content)
                            f.close()
                        except IOError, e:
                            messageDialog(unicode(e[1]), (u'IO Error'),
                                wx.OK | wx.STAY_ON_TOP)
                    else:
                        self.SaveProgramFile(event)
                elif ret == wx.ID_NO:
                    self.OnExit(event)
        else:
            ret = dialogs.messageDialog(_('Are you sure you want to exit?'), _("About to close"), wx.YES | wx.NO)
            if ret == wx.ID_YES:
                self.OnExit(event)

    def OnExit(self, event):
        if logData:
            self.logfile.close()
        if self.prepost:
            dlg = wx.MessageDialog(self, "You will now be given a post-test.", style = wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            TestScreen(None, -1, 'Post-Test', questions.post, 0)
        self.Destroy()
        event.Skip()

#----Helper functions
    def setTraceMode(self, trace=True):
        self.traceMode = trace
        if trace:
            self.ch.showTraceButtons()
            self.ch.showRunButtons(False)
        else:
            self.ch.showTraceButtons(False)
            self.ch.showRunButtons()

    def SubmitNext(self, dummy): # submit the answer or move to next problem
        if self.user_program.isRunning:
            return

        if self.traceMode:
            prediction = self.outputWindow.GetText()
            self.outputWindow.ClearAll()
            self.WorldDisplay.controlMode = False
            self.ResetWorld(None)
            if logData: # log problem and solution
                storewld = str(user_id) + '_world_' + str(self.problemNumber) + '.txt'
                self.SaveWorldFile(None, os.path.join(self.wlddir, storewld))
                storerur = str(user_id) + '_code_' + str(self.problemNumber) + '.txt'
                self.SaveProgramFile(None, os.path.join(self.rurdir, storerur))
                storepre = str(user_id) + '_prediction_' + str(self.problemNumber) + '.txt'
                try:
                    f = open(os.path.join(self.predir, storepre), 'w')
                    f.write(prediction)
                    f.close()
                except IOError:
                    pass

            # run the program and check the prediction
            self.RunProgram(None)
            while self.user_program.isRunning:
                wx.Yield()
            actual = self.outputWindow.GetText()
            d = Differ()
            diff = d.compare(prediction.splitlines(1), actual.splitlines(1))
            self.outputWindow.ClearAll()
            correct = True
            for line in diff:
                out = ''
                if line[0] == '-':
                    out += "IN"
                    correct = False
                out += "CORRECT"
                if line[0] == '+':
                    out += "ED"
                    correct = False
                out += ":\t" + line[1:]
                print out,
            if correct:
                dialogs.messageDialog("Your prediction was correct!", ":o)")
                self.stud.succ()
            else:
                dialogs.messageDialog("Error found in your prediction.", ":o(")
                self.stud.fail()
                self.backup_dict['robot2'] = self.backup_dict['robot']
            if logData: # log problem success or failure
                self.logfile.write(str(self.problemNumber) + ',' + str(self.stud.num) + ',' + str(correct) + '\n')
            self.setTraceMode(False)
            self.outputWindow.setHighlightMode(True)
            # TODO: visual diff: beepers? & visual glitch (correct->incorrect)
            return

        self.outputWindow.ClearAll()

        prob = self.stud.next()
        env, prog = prob()
        self.problemNumber += 1
        self.backup_dict = env
        self.ProgramEditor.SetReadOnly(False)
        self.ProgramEditor.SetText(prog)
        self.ProgramEditor.SetSavePoint() 
        self.ProgramEditor.SetReadOnly(True)
        arg = self.status_bar.problem_field, str(self.stud.num) + ": " + prob.__name__
        event_manager.SendCustomEvent(self, arg)
        self.WorldDisplay.controlMode = True
        self.setTraceMode()
        self.ch.showEditButtons(False)
        
        self.ResetWorld(None)
        self.outputWindow.setHighlightMode(False)
        self.WorldDisplay.SetFocus()

#---- Robot action methods
    def UndoRobotAction(self, dummy):
        if self.user_program.isRunning:
            return
        self.outputWindow.Undo()
        self.outputWindow.Undo()
        self.world.robot_dict['robot']._undo()
        self.world.DoDrawing()
        self.WorldDisplay.scrollWorld('robot')
        self.BeepersUpdateStatusBar()
        if self.world.updateImage:
            self.WorldDisplay.drawImage()
            self.WorldDisplay.Refresh()
        self.WorldDisplay.SetFocus()
    
    def DropBeeper(self, dummy):
        if self.user_program.isRunning:
            return
        if 'robot' in self.world.robot_dict:
            try:
                self.world.robot_dict['robot'].put_beeper()
                self.world.DoDrawing()
                self.BeepersUpdateStatusBar()
                if self.WorldDisplay.editor:
                    self.WorldDisplay.editor.DestroyChildren()
                    wx.StaticText(self.WorldDisplay.editor, -1, self.WorldDisplay.UpdateEditor(), (10, 10))
            except dialogs.PutBeeperException, mesg:
                dialogs.DialogPutBeeperError(mesg)
            if self.world.updateImage:
                self.WorldDisplay.drawImage()
                self.WorldDisplay.Refresh()
        self.WorldDisplay.SetFocus()
    
    def GrabBeeper(self, dummy):
        if self.user_program.isRunning:
            return
        if 'robot' in self.world.robot_dict:
            try:
                self.world.robot_dict['robot'].pick_beeper()
                self.world.DoDrawing()
                self.BeepersUpdateStatusBar()
                if self.WorldDisplay.editor:
                    self.WorldDisplay.editor.DestroyChildren()
                    wx.StaticText(self.WorldDisplay.editor, -1, self.WorldDisplay.UpdateEditor(), (10, 10))
            except dialogs.PickBeeperException, mesg:
                dialogs.DialogPickBeeperError(mesg)
            if self.world.updateImage:
                self.WorldDisplay.drawImage()
                self.WorldDisplay.Refresh()
        self.WorldDisplay.SetFocus()
    
    def PrintText(self, dummy):
        if self.user_program.isRunning:
            return
        dlg = wx.TextEntryDialog(self, _("What do you want to print?"), _("Print text"), '')
        user_response = ''
        if dlg.ShowModal() == wx.ID_OK:
            user_response = dlg.GetValue()
        dlg.Destroy()
        if user_response:
            print user_response
            self.world.robot_dict['robot']._stay_put()
        self.WorldDisplay.SetFocus()

    def TurnOffRobot(self, dummy):
        if self.user_program.isRunning:
            return
        try:
            self.world.robot_dict['robot'].turn_off()
        except dialogs.NormalEnd, mesg:
            dialogs.NormalEndDialog(mesg)
        self.WorldDisplay.SetFocus()
    
#---- World file methods
    def OpenWorldFile(self, dummy, openedFileName=""):
        if self.user_program.isRunning:
            return

        if openedFileName == "":
            openedFileName = dialogs.openDialog(_("Choose a file"),
                _("World files (*.wld)|*.wld| All files (*.*)|*.*"),
                "", settings.USER_WORLDS_DIR)

        if openedFileName != "":
            self.world_filename = openedFileName
            self.ReadWorldFile()
            self.UpdateWorld()
            self.user_program.clear_trace()
            settings.USER_WORLDS_DIR = os.path.dirname(self.world_filename)

    def ReadWorldFile(self):
        if self.user_program.isRunning:
            return
        f = open(self.world_filename, 'r')
        txt = f.read()
        f.close()
        txt = parser.FixLineEnding(txt)
        flag = parser.ParseWorld(txt)
        if flag:
            self.backup_dict = {} # used to 'reset' the world
            exec txt in self.backup_dict # extracts avenues, streets, robot,
                                     # walls and beepers

    def ResetWorld(self, dummy):
        if self.user_program.isRunning:
            return
        self.UpdateWorld()
        self.outputWindow.redirect()
        self.world.robot_dict['robot']._setDebug(True)
        self.WorldDisplay.SetFocus()

    def UpdateWorld(self):
        try:
            av = self.backup_dict['avenues']
        except:
            dialogs.messageDialog(
                   _("Problem with %s\nPlease recreate world file.")%
                   _("avenues"), 
                   _("Invalid world file format"))
            return
        try:
            st = self.backup_dict['streets']
        except:
            dialogs.messageDialog(
                   _("Problem with %s\nPlease recreate world file.")%
                   _("streets"), 
                   _("Invalid world file format"))
            return
        self.world.resetDimensions(av, st)
        try:
            if 'robot' in self.backup_dict:
                x, y, key, beep = self.backup_dict['robot']
                arg = self.status_bar.beeper_field, beep
                event_manager.SendCustomEvent(self, arg)
        except:
            dialogs.messageDialog(
                   _("Problem with %s\nPlease recreate world file.")%
                   _("robot"), 
                   _("Invalid world file format"))
            return
        # We might be reloading the world, to which robots may have been added
        # Remove all robots that have been added, if any; 
        # recall that "named" robots are added through a user-defined program, 
        # not in a world file.
        self.world.robot_dict = {}
        # Recreate the robot that was in the original file
        if 'robot' in self.backup_dict:
            self.world.addOneRobot(x, y, key, beep, name='robot')
        if 'robot2' in self.backup_dict:
            self.world.addOneRobot(x, y, key, beep, name='robot2', colour='blue')

        # world characteristics
        # note: we make shallow copies of rurApp.backup_dict as we 
        # may need it if we call ResetWorld().
        try:
            for corner in self.world.beepers_dict:
                del self.world.beepers_dict[corner] # empty, but keep reference
            for corner in self.backup_dict['beepers']:
                self.world.beepers_dict[corner] = self.backup_dict[
                                                            'beepers'][corner]
        except:
            dialogs.messageDialog(
                   _("Problem with %s\nPlease recreate world file.")%
                   _("beepers"), 
                   _("Invalid world file format"))
            return
        # We need to keep one reference only to walls_list
        try:
            for col, row in self.world.walls_list:
                self.world.walls_list.remove((col, row)) # empty, but keep ref.
            for col, row in self.backup_dict['walls']:
                self.world.walls_list.append((col, row))
        except:
            dialogs.messageDialog(
                   _("Problem with %s\nPlease recreate world file.")%
                   _("walls"), 
                   _("Invalid world file format"))
            return

        # prepare to recreate the background images
        self.world.background_images_created = False
        self.world.AdjustWorldSize()
        self.world.InitTileSizes()
        self.WorldDisplay.InitialiseVariables()
        self.world.DoDrawing()
        # create a new bitmap image
        self.WorldDisplay.buffer = wx.EmptyBitmap(self.world.maxWidth,
                                               self.world.maxHeight)
        self.WorldDisplay.drawImage()
	self.WorldDisplay.Refresh() # added to fix refresh bug (issue #23)
        if self.traceMode:
            self.outputWindow.ClearAll()

    def SaveWorldFile(self, dummy, savedFileName=""):
        if self.user_program.isRunning:
            return
        txt = self.WorldDisplay.UpdateEditor()
        if savedFileName == "":
            savedFileName = dialogs.checkedSaveDialog(txt,
                _("Save new world as"),
                _("World files (*.wld)|*.wld| All files (*.*)|*.*"),
                self.world_filename, settings.USER_WORLDS_DIR)
        else:
            try:
                f = open(savedFileName, 'w')
                f.write(txt)
                f.close()
            except IOError:
                pass

        self.world_filename = savedFileName

        settings.SAMPLE_WORLDS_DIR = os.path.dirname(self.world_filename)
        # save a backup copy to 'reset world'
        self.backup_dict = {}
        exec txt in self.backup_dict

#----- Program files methods

    def OpenProgramFile(self, dummy, openedFileName=""):
        if self.user_program.isRunning:
            return

        if openedFileName == "":
            openedFileName = dialogs.openDialog(_("Choose a file"),
                _("Program files (*.rur)|*.rur| All files (*.*)|*.*"),
                "", settings.USER_PROGS_DIR)

        if openedFileName != "":
            global code
            self.filename = openedFileName
            code = open(self.filename, 'r').read()
            code = parser.FixLineEnding(code)
            self.ProgramEditor.SetText(code)
            no_error, mesg = parser.ParseProgram(code)
            settings.USER_PROGS_DIR = os.path.dirname(self.filename)
            if no_error:
                self.raw_code = code
                self.ProgramEditor.SetSavePoint()
            else:
                code = ""
                dialogs.messageDialog(mesg, _("Program will not be used."))
    
    def SaveProgramFile(self, dummy, savedFileName=""):
        if self.user_program.isRunning or self.user_program.isStepped:
            return
        global code
        code = self.ProgramEditor.GetText()
        no_error, mesg = parser.ParseProgram(code)
        if no_error:
            if savedFileName == "":
                savedFileName = dialogs.checkedSaveDialog(
                    code,
                    _("Save new program as"),
                    _("Program files (*.rur)|*.rur| All files (*.*)|*.*"),
                    self.filename, settings.USER_PROGS_DIR)
            else:
                try:
                    f = open(savedFileName, 'w')
                    f.write(code)
                    f.close()
                except IOError:
                    pass

            self.filename = savedFileName
            settings.USER_PROGS_DIR = os.path.dirname(self.filename)
            self.ProgramEditor.SetSavePoint()
        else:
            code = ""
            dialogs.messageDialog(mesg, _("Program will not be saved."))

#--- Program controls

    def RunProgram(self, dummy):
        if self.user_program.isRunning:
            if self.user_program.isPaused or self.user_program.isStepped:
                self.user_program.isStepped = False
                self.Pause(None)
            return
        if not self.WorldDisplay.editMode:
            self.ResetWorld(None)
        self.user_program.isRunning = True
        self.user_program.restart(self.world.robot_dict)

    def Pause(self, dummy):
        if not (self.user_program.isRunning or self.user_program.isStepped):
            return
        if self.user_program.isPaused:
            self.user_program.isPaused = False
            arg = self.status_bar.running_field, _("Program is running")
            event_manager.SendCustomEvent(self, arg)
        else:
            self.user_program.isPaused = True
            arg = self.status_bar.running_field, _("Program paused")
            event_manager.SendCustomEvent(self, arg)

    def Step(self, dummy):
        self.user_program.isStepped = True
        if not self.user_program.isRunning:
            self.RunProgram(None)
        else:
            self.Pause(None)

    def StopProgram(self, dummy):
        self.user_program.StopProgram()
        arg = self.status_bar.running_field, _("Program not running")
        event_manager.SendCustomEvent(self, arg)
        self.user_program.stopped_by_user = True

#--- World controls

    def EditWalls(self, event):
        if self.user_program.isRunning:
            return
        self.user_program.clear_trace()
        if self.world.editWalls:
            self.world.editWalls = False
            self.world.DoDrawing()
        else:
            self.world.editWalls = True
            self.world.DoDrawing()
        self.WorldDisplay.drawImage()
        self.WorldDisplay.Refresh()

    def BeepersToRobot(self, dummy):
        if self.user_program.isRunning:
            return
        self.user_program.clear_trace()
        try:
            dummy = self.backup_dict['robot']
        except KeyError:
            msg = _("No robot in world to give beepers to.")
            dialogs.messageDialog(msg, 'error')
            return
        dialogs.RobotBeeperDialog(self, -1, _("Beepers!"))

    def BeepersUpdateStatusBar(self):
        arg = self.status_bar.beeper_field, \
              self.world.robot_dict['robot']._beeper_bag
        event_manager.SendCustomEvent(self, arg)
        # update the world window text at the same time
        self.rightWindow.DestroyChildren() # removes the old wx.StaticText
        wx.StaticText(self.rightWindow, -1,
                        self.WorldDisplay.UpdateEditor(), (10, 10))
                        
    def ResizeWorld(self, dummy):
        if self.user_program.isRunning:
            return
        self.user_program.clear_trace()
        dialogs.ResizeWorldDialog(self, -1, _("World size!"))

    def ToggleHighlight(self, dummy):
        if self.user_program.isRunning:
            return
        global code
        if settings.line_number_flag:
            settings.line_number_flag = False
            code = self.raw_code
        else:
            settings.line_number_flag = True
            code = parser.add_line_number_info(code)

    def ToggleWorldWindow(self, dummy):
        if self.user_program.isRunning:
            return
        if self.rightWindow.isVisible:
            self.rightWindow.SetDefaultSize(wx.Size(0, 600))
            self.rightWindow.isVisible = False
        else:
            self.rightWindow.SetDefaultSize(wx.Size(200, 600))
            self.rightWindow.isVisible = True

        wx.LayoutAlgorithm().LayoutWindow(self.sash, self.WorldDisplay)
        self.rightWindow.DestroyChildren() # removes the old wx.StaticText
        wx.StaticText(self.rightWindow, -1,
                        self.WorldDisplay.UpdateEditor(), (10, 10))

    def AddRemoveRobot(self, dummy, robot_name='robot', robot_info=None):
        if self.user_program.isRunning:
            return
        if self.world.robot_dict:
            # remove all robots from non-empty dict
            self.world.robot_dict = {}
            arg = self.status_bar.beeper_field, self.status_bar.no_robot
        else:
            self.world.robot_dict = {}
            self.world.addOneRobot(name=robot_name)
            if not robot_info:
                self.backup_dict[robot_name] = self.world.robot_dict[
                    robot_name]._getInfoTuple()
            else:
                self.backup_dict[robot_name] = robot_info
            arg = self.status_bar.beeper_field, \
                  self.world.robot_dict['robot']._beeper_bag
        event_manager.SendCustomEvent(self, arg)
        self.world.DoDrawing()
        self.WorldDisplay.drawImage()
        self.WorldDisplay.Refresh()
        
    def load_images(self, event):
        for heading in ("South", "North", "East", "West"):
            openedFileName = dialogs.openDialog(
                _("Choose an image: robot facing " + heading),
                _("All files (*.*)|*.*"),
                "", os.getcwd())
            if openedFileName != "":
                setattr(self, "file" + heading, openedFileName)
            else:
                return()

        image_south = getImage(images.GREY_ROBOT_S)
        image_north = getImage(images.GREY_ROBOT_N)
        image_east = getImage(images.GREY_ROBOT_E)
        image_west = getImage(images.GREY_ROBOT_W)
        try:
            image_south = wx.Image(self.fileSouth).ConvertToBitmap()
            image_north = wx.Image(self.fileNorth).ConvertToBitmap()
            image_east = wx.Image(self.fileEast).ConvertToBitmap()
            image_west = wx.Image(self.fileWest).ConvertToBitmap()
        except Exception, info:
            print "Conversion or loading problems: can not use new images."
            print "info = %", info
        images.setImage(images.GREY_ROBOT_S, image_south)
        images.setImage(images.GREY_ROBOT_N, image_north)
        images.setImage(images.GREY_ROBOT_E, image_east)
        images.setImage(images.GREY_ROBOT_W, image_west)
        self.AddRemoveRobot(event) # remove robot with old image
        self.AddRemoveRobot(event) # and add new one


##New User Screen
class NewUserScreen(wx.Frame):
    def __init__(self, parent, id, title):
        frameX = 900
        frameY = 700
        wx.Frame.__init__(self, parent, id, title, size=(frameX, frameY))
        largeFont = wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_BOLD)        
        buttonFont = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_BOLD)
        labelFont = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_BOLD)

        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour('WHEAT')

        label = wx.StaticText(panel, -1, 'Welcome to the Playing')
        label2 = wx.StaticText(panel, -1, 'to Program System!')
        promptLabel = wx.StaticText(panel, -1, 'Please Enter your information below.')
 #       firstNameLabel =  wx.StaticText(panel, -1, 'First Name: ')
 #       lastNameLabel = wx.StaticText(panel, -1, 'Last Name: ')
        ageLabel = wx.StaticText(panel, -1, 'Age: ')
        umbcEmailLabel = wx.StaticText(panel, -1, 'UMBC Email: ')
        domainLabel =  wx.StaticText(panel, -1, '@umbc.edu')
        sexLabel = wx.StaticText(panel, -1, 'Sex: ')
        creditLabel = wx.StaticText(panel, -1, 'Credit Count: ')
        transferLabel = wx.StaticText(panel, -1, 'Are you a transfer student? ')
        courseLabel = wx.StaticText(panel, -1, "Please enter the computer science courses that you")
        courseLabel2 = wx.StaticText(panel, -1, "have completed and the grade that you earned in each.")
        courseNameLabel = wx.StaticText(panel, -1, "Course")
        courseGradeLabel = wx.StaticText(panel, -1, "Grade")
        languagesLabel = wx.StaticText(panel, -1, "Please list the programming languages that you")
        languagesLabel2 = wx.StaticText(panel, -1, "have experience with and how long: ")
        languageNameLabel = wx.StaticText(panel, -1, "Language")
        yearsLabel = wx.StaticText(panel, -1, "Years")
        majorLabel = wx.StaticText(panel, -1, "What is your major or intended major?")

        label2.SetFont(largeFont)
        label.SetFont(largeFont)
        promptLabel.SetFont(buttonFont)
#        firstNameLabel.SetFont(labelFont)
#        lastNameLabel.SetFont(labelFont)
        umbcEmailLabel.SetFont(labelFont)
        ageLabel.SetFont(labelFont)
        sexLabel.SetFont(labelFont)
        creditLabel.SetFont(labelFont)
        transferLabel.SetFont(labelFont)
        courseLabel.SetFont(labelFont)
        courseLabel2.SetFont(labelFont)
        courseNameLabel.SetFont(labelFont)
        courseGradeLabel.SetFont(labelFont)
        domainLabel.SetFont(labelFont)
        languagesLabel.SetFont(labelFont)
        languagesLabel2.SetFont(labelFont)
        yearsLabel.SetFont(labelFont)
        languageNameLabel.SetFont(labelFont)
        majorLabel.SetFont(labelFont)        

#        self.firstName = wx.TextCtrl(panel, -1, '')
#        self.lastName = wx.TextCtrl(panel, -1, '')
        self.email = wx.TextCtrl(panel, -1, '')
        self.age = wx.TextCtrl(panel, -1, '')
        self.sex = wx.Choice(panel, -1, choices = ["Male", "Female"])
        self.creditCount = wx.TextCtrl(panel, -1, '')
        self.isTransfer = wx.Choice(panel, -1, choices = ["Yes", "No"])
        self.major = wx.TextCtrl(panel, -1, '')

        self.course1 = wx.TextCtrl(panel, -1, '')
        self.course2 = wx.TextCtrl(panel, -1, '')
        self.course3 = wx.TextCtrl(panel, -1, '')
        self.course4 = wx.TextCtrl(panel, -1, '')
        self.course5 = wx.TextCtrl(panel, -1, '')
        self.course6 = wx.TextCtrl(panel, -1, '')

        grades = ["", "A", "B", "C", "D", "F", "P", "I", "Currently Enrolled"]
        #could loop
        self.grade1 = wx.Choice(panel, -1, choices = grades)
        self.grade2 = wx.Choice(panel, -1, choices = grades)
        self.grade3 = wx.Choice(panel, -1, choices = grades)
        self.grade4 = wx.Choice(panel, -1, choices = grades)
        self.grade5 = wx.Choice(panel, -1, choices = grades)
        self.grade6 = wx.Choice(panel, -1, choices = grades)

        #could loop
        self.language1 = wx.TextCtrl(panel, -1, '')
        self.language2 = wx.TextCtrl(panel, -1, '')
        self.language3 = wx.TextCtrl(panel, -1, '')
        self.language4 = wx.TextCtrl(panel, -1, '')
        self.language5 = wx.TextCtrl(panel, -1, '')
        self.language6 = wx.TextCtrl(panel, -1, '')

        years = ["", "1 or less", "1 year", "2 years", "3 years", "4 or more"] 
        self.year1 = wx.Choice(panel, -1, choices = years)
        self.year2 = wx.Choice(panel, -1, choices = years)
        self.year3 = wx.Choice(panel, -1, choices = years)
        self.year4 = wx.Choice(panel, -1, choices = years)
        self.year5 = wx.Choice(panel, -1, choices = years)
        self.year6 = wx.Choice(panel, -1, choices = years)
        

        button1 = wx.Button(panel, -1, 'Create')
        button1.SetFont(buttonFont)

        button2 = wx.Button(panel, -1, 'Back')
        button2.SetFont(buttonFont)

        vbox = wx.BoxSizer(wx.VERTICAL)
        
        vbox.Add(label, 0, wx.ALIGN_CENTER | wx.ALL | wx.ALIGN_TOP, 5)
        vbox.Add(label2, 0, wx.ALIGN_CENTER | wx.BOTTOM | wx.ALIGN_TOP, 5)
        vbox.AddSpacer(20)
        vbox.Add(promptLabel, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.BOTTOM | wx.LEFT | wx.ALIGN_TOP, 5)
        vbox.Add(majorLabel, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.BOTTOM | wx.LEFT | wx.ALIGN_TOP, 5)
        vbox.Add(self.major, 0, wx.ALIGN_LEFT | wx.BOTTOM | wx.LEFT | wx.ALIGN_TOP, 5)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3.Add(ageLabel, 0, wx.ALIGN_LEFT | wx.BOTTOM | wx.RIGHT | wx.LEFT, 5)
        hbox3.Add(self.age, 0, wx.ALIGN_LEFT | wx.BOTTOM | wx.RIGHT, 5)
        vbox.Add(hbox3)

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4.Add(sexLabel, 0, wx.ALIGN_LEFT | wx.BOTTOM | wx.RIGHT | wx.LEFT, 5)
        hbox4.Add(self.sex, 0, wx.ALIGN_LEFT | wx.BOTTOM | wx.RIGHT, 5)
        vbox.Add(hbox4)

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        hbox5.Add(umbcEmailLabel, 0, wx.ALIGN_LEFT | wx.BOTTOM | wx.RIGHT | wx.LEFT, 5)
        hbox5.Add(self.email, 0, wx.ALIGN_LEFT | wx.BOTTOM | wx.RIGHT | wx.LEFT, 5)
        hbox5.Add(domainLabel, 0, wx.ALIGN_LEFT | wx.BOTTOM | wx.RIGHT, 5)
        vbox.Add(hbox5)

        hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        hbox6.Add(creditLabel, 0, wx.ALIGN_LEFT | wx.BOTTOM | wx.RIGHT | wx.LEFT, 5)
        hbox6.Add(self.creditCount, 0, wx.ALIGN_LEFT | wx.BOTTOM | wx.RIGHT, 5)
        vbox.Add(hbox6)

        hbox7 = wx.BoxSizer(wx.HORIZONTAL)
        hbox7.Add(transferLabel, 0, wx.ALIGN_LEFT | wx.BOTTOM | wx.RIGHT | wx.LEFT, 5)
        hbox7.Add(self.isTransfer, 0, wx.ALIGN_LEFT | wx.BOTTOM | wx.RIGHT, 5)
        vbox.Add(hbox7)

        hbox8 = wx.BoxSizer(wx.HORIZONTAL)
        hbox8.Add(courseLabel, 0, wx.ALIGN_LEFT | wx.LEFT, 5)
        hbox8.Add(languagesLabel, 0, wx.ALIGN_LEFT | wx.LEFT, 100)
        vbox.Add(hbox8)

        hbox9 = wx.BoxSizer(wx.HORIZONTAL)
        hbox9.Add(courseLabel2, 0, wx.ALIGN_LEFT | wx.LEFT, 5)
        hbox9.Add(languagesLabel2, 0, wx.ALIGN_LEFT | wx.LEFT, 75)
        vbox.Add(hbox9)


        hbox10 = wx.BoxSizer(wx.HORIZONTAL)
        gSizer = wx.GridSizer(7, 2, 5, 40)
        gSizer.Add(courseNameLabel, 0, wx.ALL | wx.ALIGN_LEFT)
        gSizer.Add(courseGradeLabel, 0, wx.ALL | wx.ALIGN_LEFT)
        gSizer.Add(self.course1, 0, wx.ALL | wx.ALIGN_LEFT)
        gSizer.Add(self.grade1, 0, wx.ALL | wx.ALIGN_LEFT)
        gSizer.Add(self.course2, 0, wx.ALL | wx.ALIGN_LEFT)
        gSizer.Add(self.grade2, 0, wx.ALL | wx.ALIGN_LEFT)
        gSizer.Add(self.course3, 0, wx.ALL | wx.ALIGN_LEFT)
        gSizer.Add(self.grade3, 0, wx.ALL | wx.ALIGN_LEFT)
        gSizer.Add(self.course4, 0, wx.ALL | wx.ALIGN_LEFT)
        gSizer.Add(self.grade4, 0, wx.ALL | wx.ALIGN_LEFT)
        gSizer.Add(self.course5, 0, wx.ALL | wx.ALIGN_LEFT)
        gSizer.Add(self.grade5, 0, wx.ALL | wx.ALIGN_LEFT)
        gSizer.Add(self.course6, 0, wx.ALL | wx.ALIGN_LEFT)
        gSizer.Add(self.grade6, 0, wx.ALL | wx.ALIGN_LEFT)
        hbox10.Add(gSizer, 0, wx.ALIGN_LEFT | wx.LEFT, 5)

        gSizer2 = wx.GridSizer(7, 2, 5, 40)
        gSizer2.Add(languageNameLabel, 0, wx.ALL | wx.ALIGN_LEFT)
        gSizer2.Add(yearsLabel, 0, wx.ALL | wx.ALIGN_LEFT)
        gSizer2.Add(self.language1, 0, wx.ALL | wx.ALIGN_LEFT)
        gSizer2.Add(self.year1, 0, wx.ALL | wx.ALIGN_LEFT)
        gSizer2.Add(self.language2, 0, wx.ALL | wx.ALIGN_LEFT)
        gSizer2.Add(self.year2, 0, wx.ALL | wx.ALIGN_LEFT)
        gSizer2.Add(self.language3, 0, wx.ALL | wx.ALIGN_LEFT)
        gSizer2.Add(self.year3, 0, wx.ALL | wx.ALIGN_LEFT)
        gSizer2.Add(self.language4, 0, wx.ALL | wx.ALIGN_LEFT)
        gSizer2.Add(self.year4, 0, wx.ALL | wx.ALIGN_LEFT)
        gSizer2.Add(self.language5, 0, wx.ALL | wx.ALIGN_LEFT)
        gSizer2.Add(self.year5, 0, wx.ALL | wx.ALIGN_LEFT)
        gSizer2.Add(self.language6, 0, wx.ALL | wx.ALIGN_LEFT)
        gSizer2.Add(self.year6, 0, wx.ALL | wx.ALIGN_LEFT)
        hbox10.Add(gSizer2, 0, wx.ALIGN_LEFT | wx.LEFT, 140)

        vbox.Add(hbox10)


        vbox.Add(button1, 0, wx.ALIGN_CENTER | wx.ALL | wx.ALIGN_BOTTOM, 5)
        vbox.Add(button2, 0, wx.ALIGN_CENTER | wx.ALL | wx.ALIGN_BOTTOM, 5)

        panel.SetSizer(vbox)
        self.Bind(wx.EVT_BUTTON, self.OnCreate, button1)
        self.Bind(wx.EVT_BUTTON, self.OnBack, button2)

        self.Show(True)
    
    def OnCreate(self, event):
        global user_id

        int_age = -1
        int_creditCount = -1
        try:
            int_age = int(self.age.GetValue())
        except ValueError:
            int_age = -1
        try:
            int_creditCount = int(self.creditCount.GetValue())
        except ValueError:
            int_creditCount = -1


        profiles = {}
        names = []
        allValid = False
        ageValid = False
        creditValid = False
        emailValid = False

        try:
            logfile = open(os.path.join(logDataDir, "key.txt"), "r")
            for line in logfile:
                name, id = line.strip().split()
                try:
                    id = int(id)
                except ValueError:
                    continue
                profiles[id] = name
            logfile.close()
        except IOError:
            pass

        names = profiles.values()
        ids = profiles.keys()



        if self.email.GetValue().strip() in names:
            dlg = wx.MessageDialog(self, "This username is already in use.", 
                                       "Invalid username.")
            dlg.ShowModal()
            dlg.Destroy()
            event.Skip()
            return
        if int_age != -1 and int_age < 100:
            ageValid = True
        if int_creditCount != -1 and int_creditCount < 200:
            creditValid = True
        if  self.email.GetValue() != "":
            emailValid = True
        
        allValid = ageValid and creditValid and emailValid


        if not ageValid:
            dlg = wx.MessageDialog(self, "Age must be a number below 100",
                                   "Invalid Information!",  style = wx.OK)            
            dlg.ShowModal()
            dlg.Destroy()
            event.Skip()
        elif not creditValid:
            dlg = wx.MessageDialog(self, "Credit Count must be a number below 200",
                                       "Invalid Information!", style = wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            event.Skip()
        elif not emailValid:
            dlg = wx.MessageDialog(self, "You must enter a UMBC email.",
                                   "Invalid Information!", style = wx.OK)            
            dlg.ShowModal()
            dlg.Destroy()
            event.Skip()

        if not allValid:
            return

        #Create the key file with the user_id for lookup

        user_id = random.randint(1, 10 * (len(ids) + 1))
        while user_id in ids:
            user_id = random.randint(1, 10 * (len(ids) + 1))

        try:
            logfile = open(os.path.join(logDataDir, "key.txt"), "a+")
            logfile.write(self.email.GetValue() + "\t" + str(user_id) + "\n")
            logfile.close()
        except IOError:
            dlg = wx.MessageDialog(self, "Cannot write to user data file.",
                                   "File error!", style = wx.OK)            
            dlg.ShowModal()
            dlg.Destroy()
            event.Skip()
            return
        
        #Create the demographic file
        student_dir = os.path.join(logDataDir, 'StudentFiles', 'Demographics')
        demo_filename = str(user_id) + '_demo' + '.txt'
            
        try:
            os.makedirs(student_dir)
        except OSError:
            pass
            
        f = open(os.path.join(student_dir, demo_filename), "w")
        #f.write(self.lastName.GetValue().strip() + '\n')
        #f.write(self.firstName.GetValue().strip() + '\n')
        f.write(self.email.GetValue().strip() + '\n')
        f.write(self.age.GetValue().strip() + '\n')
        f.write(self.sex.GetString(self.sex.GetSelection()).strip() + '\n')
        f.write(self.creditCount.GetValue().strip() + '\n')
        f.write(self.isTransfer.GetString(self.isTransfer.GetSelection()).strip() + '\n')
        f.write(self.major.GetValue().strip() + '\n')

        #Temporary way for storing the couses and grades
        #May change to a separate panel to store each of these in an extendable array
        f.write(self.course1.GetValue().strip() + '\n')
        f.write(self.grade1.GetString(self.grade1.GetSelection()).strip() + '\n')
        f.write(self.course2.GetValue().strip() + '\n')
        f.write(self.grade2.GetString(self.grade2.GetSelection()).strip() + '\n')
        f.write(self.course3.GetValue().strip() + '\n')
        f.write(self.grade3.GetString(self.grade3.GetSelection()).strip() + '\n')
        f.write(self.course4.GetValue().strip() + '\n')
        f.write(self.grade4.GetString(self.grade4.GetSelection()).strip() + '\n')
        f.write(self.course5.GetValue().strip() + '\n')
        f.write(self.grade5.GetString(self.grade5.GetSelection()).strip() + '\n')
        f.write(self.course6.GetValue().strip() + '\n')
        f.write(self.grade6.GetString(self.grade6.GetSelection()).strip() + '\n')

        f.write(self.language1.GetValue().strip() + '\n')
        f.write(self.year1.GetString(self.grade1.GetSelection()).strip() + '\n')
        f.write(self.language2.GetValue().strip() + '\n')
        f.write(self.year2.GetString(self.grade2.GetSelection()).strip() + '\n')
        f.write(self.language3.GetValue().strip() + '\n')
        f.write(self.year3.GetString(self.grade3.GetSelection()).strip() + '\n')
        f.write(self.language4.GetValue().strip() + '\n')
        f.write(self.year4.GetString(self.grade4.GetSelection()).strip() + '\n')
        f.write(self.language5.GetValue().strip() + '\n')
        f.write(self.year5.GetString(self.grade5.GetSelection()).strip() + '\n')
        f.write(self.language6.GetValue().strip() + '\n')
        f.write(self.year6.GetString(self.grade6.GetSelection()).strip() + '\n')

        f.close()

        dlg = wx.MessageDialog(self, "You will now begin a pre-test exercise.", style = wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

        TestScreen(None, -1, 'Pre-Test', questions.pre, 0, False) 
        self.Destroy()
        event.Skip()
        
    
    def OnBack(self, event):
        self.Close(True)
        LoginScreen(None, -1, 'Login Screen')
        
        
class ReturnUserScreen(wx.Frame):
    def __init__(self, parent, id, title):
        frameX = 500
        frameY = 500
        wx.Frame.__init__(self, parent, id, title, size=(frameX, frameY))
        largeFont = wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_BOLD)        
        buttonFont = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_BOLD)
        labelFont = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_BOLD)

        
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour('WHEAT')
        label = wx.StaticText(panel, -1, 'Welcome to the Playing')
        label2 = wx.StaticText(panel, -1, 'to Program System!')
        label.SetFont(largeFont)
        label2.SetFont(largeFont)

        promptLabel = wx.StaticText(panel, -1, 'Please Enter your information below.')
        umbcEmailLabel = wx.StaticText(panel, -1, 'UMBC Email: ')
        domainLabel =  wx.StaticText(panel, -1, '@umbc.edu')
        promptLabel.SetFont(buttonFont)
        umbcEmailLabel.SetFont(labelFont)
        domainLabel.SetFont(labelFont)
        
        self.email = wx.TextCtrl(panel, -1, '')        
        button1 = wx.Button(panel, -1, 'Login')
        button2 = wx.Button(panel, -1, 'Back')
        button1.SetFont(buttonFont)
        button2.SetFont(buttonFont)

        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox.Add(label, 0, wx.ALIGN_CENTER | wx.ALL | wx.ALIGN_TOP, 5)
        vbox.Add(label2, 0, wx.ALIGN_CENTER | wx.BOTTOM | wx.ALIGN_TOP, 5)
        vbox.Add(promptLabel, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.BOTTOM | wx.LEFT | wx.ALIGN_TOP, 5)
        vbox.AddSpacer(20)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(umbcEmailLabel, 0, wx.ALIGN_LEFT | wx.BOTTOM | wx.RIGHT | wx.LEFT, 5)
        hbox1.Add(self.email, 0, wx.ALIGN_LEFT | wx.RIGHT, 5)
        hbox1.Add(domainLabel, 0, wx.ALIGN_LEFT | wx.RIGHT, 300)
        vbox.Add(hbox1)

        vbox.Add(button1, 0, wx.ALIGN_CENTER | wx.ALL | wx.ALIGN_BOTTOM, 5)
        vbox.Add(button2, 0, wx.ALIGN_CENTER | wx.ALL | wx.ALIGN_BOTTOM, 5)

        panel.SetSizer(vbox)


        self.Bind(wx.EVT_BUTTON, self.OnLogin, id=button1.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnBack, id=button2.GetId())
        
        self.email.SetFocus()
        self.Show(True)

    def OnBack(self, event):
        LoginScreen(None, -1, 'Login')
        self.Destroy()
        event.Skip()
    
    def OnLogin(self, event):
        global user_id

        #Check if umbc name is in logfile
        try:
            f = open(os.path.join(logDataDir, "key.txt"), "r")
            studentFound = False
            for line in f:
                student = line.split()
                if student[0] == self.email.GetValue():
                    studentFound = True
                    user_id = int(student[1])
                    break
            f.close()
        except IOError:
            dlg = wx.MessageDialog(self, "You are not registered.", 
                                   "Please create a new account first.")
            dlg.ShowModal()
            dlg.Destroy()
            event.Skip()
            return
        if studentFound:
            dlg = wx.MessageDialog(self, "You will now begin a pre-test exercise.")
            dlg.ShowModal()
            dlg.Destroy()
            TestScreen(None, -1, 'Pre-Test', questions.pre, 0, False)
            self.Destroy()
            event.Skip()
        else:
            #todo: Clean this up, create a pop-up asking for a different loging
            dlg = wx.MessageDialog(self, "This username is not registered.", 
                                   "Username not found.")
            dlg.ShowModal()
            dlg.Destroy()
            event.Skip()


class Notes(wx.Frame):
    def __init__(self, parent, id, title):
        frameX = 500
        frameY = 500
        wx.Frame.__init__(self, parent, id, title, size=(frameX, frameY))
        largeFont = wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_BOLD)        

        buttonFont = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_BOLD)

        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour('WHEAT')
        label = wx.StaticText(panel, -1, 'Notes')
        label2 = wx.StaticText(panel, -1, 'Please inform us of any suggestions or problems')
        self.box = wx.TextCtrl(panel, -1, '', size=(300, 300), style=wx.TE_MULTILINE)
        button = wx.Button(panel, -1, 'Submit')

        button.SetFont(buttonFont)
        label.SetFont(largeFont)
        label2.SetFont(buttonFont)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(label, 0, wx.ALIGN_CENTER | wx.ALL | wx.ALIGN_TOP, 5)
        vbox.Add(label2, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND | wx.ALIGN_TOP, 5)
        vbox.Add(self.box, 0, wx.ALIGN_CENTER | wx.ALL | wx.ALIGN_TOP, 5)
        vbox.Add(button, 0, wx.ALIGN_CENTER | wx.ALL | wx.ALIGN_BOTTOM, 20)
        panel.SetSizer(vbox)

        wx.EVT_CLOSE(self, self.OnClose)

        self.Bind(wx.EVT_BUTTON, self.Submit, id=button.GetId())

        self.box.SetFocus()

        self.Show(True)


    def OnClose(self, event):
        self.Destroy()
        event.Skip()

    def Submit(self, ins):
        global user_id

        dirHome = os.getcwd()
        dir = logDataDir
        student_dirs = os.path.join(dir, 'StudentFiles', 'Notes')
        try:
            os.makedirs(student_dirs)
        except OSError:
            pass

        os.chdir(student_dirs)
        fileName = str(user_id) + "_notes.txt"
        file = open(fileName, "w")
        file.write(self.box.GetValue())
        file.close()
        os.chdir(dirHome)

        dlg = wx.MessageDialog(self, "Complete.", 
                               "Thank you for using the P2P Sytem.", style = wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        self.Close(True)

class InstructionScreen(wx.Frame):
    def __init__(self, parent, id, title):
        frameX = 500
        frameY = 500
        wx.Frame.__init__(self, parent, id, title, size=(frameX, frameY))
        self.lessons_dir = conf.getLessonsNlDir()

        self.html = html.HtmlWindow(self, id)

        self.labelFont = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_BOLD)

        wx.EVT_CLOSE(self, self.OnClose)

        self.Show(True)

    def OnClose(self, event):
        self.Destroy()
        event.Skip()

    def setInstructions(self, ins):
        htmlFiles = os.path.join(settings.LESSONS_DIR, 'en', 'intro')
        
        page = os.path.join(htmlFiles, ins)

        self.html.LoadPage(page)
		

class LoginScreen(wx.Frame):
    def __init__(self, parent, id, title):
        frameX = 500
        frameY = 500
        wx.Frame.__init__(self, parent, id, title, size=(frameX, frameY))

        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour('WHEAT')

        largeFont = wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_BOLD)        

        buttonFont = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_BOLD)
        

        label = wx.StaticText(panel, -1, 'Welcome to the Playing')
        label2 = wx.StaticText(panel, -1, 'to Program System!')
        label.SetFont(largeFont)
        label2.SetFont(largeFont)

        button1 = wx.Button(panel, -1, 'New User')
        button2 = wx.Button(panel, -1, 'Returning User')
        button1.SetFont(buttonFont)
        button2.SetFont(buttonFont)

        bmp = wx.BitmapFromImage(getImage(images.SPLASH_SCREEN).ConvertToImage())

        image = wx.StaticBitmap(panel, -1, size = (300,300), bitmap = bmp)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(label, 0, wx.ALIGN_CENTER | wx.ALL | wx.ALIGN_TOP, 5)
        vbox.Add(label2, 0, wx.ALIGN_CENTER | wx.BOTTOM | wx.ALIGN_TOP, 5)
        vbox.Add(image, 0, wx.ALIGN_CENTER)
        vbox.Add(button1, 0, wx.ALIGN_CENTER | wx.ALL | wx.ALIGN_BOTTOM, 5)
        vbox.Add(button2, 0, wx.ALIGN_CENTER | wx.ALL | wx.ALIGN_BOTTOM, 5)

        panel.SetSizer(vbox)

        wx.EVT_CLOSE(self, self.OnClose)

        self.Bind(wx.EVT_BUTTON, self.OnNewUser, id=button1.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnReturnUser, id=button2.GetId())

        self.Show(True)

    def OnNewUser(self, event):
        NewUserScreen(None, -1, 'New User')
        self.Destroy()
        event.Skip()
        

    def OnReturnUser(self, event):
        ReturnUserScreen(None, -1, 'Returning User')
        self.Destroy()
        event.Skip()

    def OnClose(self, event):
        self.Destroy()
        event.Skip()


class TestScreen(wx.Frame):
    def __init__(self, parent, id, title, source, i, exitOnClose=True):
        wx.Frame.__init__(self, parent, id, title + " question #" + str(i+1), size=wx.Size(944,708))

        self.title = title
        self.source = source
        self.i = i
        self.question = source[i]
        self.exitOnClose = exitOnClose
        
        labelFont = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_NORMAL)        

        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour('WHEAT')
        sizer = wx.BoxSizer(wx.VERTICAL)
        instr = wx.StaticText(panel, -1, self.question.instr)
        instr.SetFont(labelFont)
        sizer.Add(instr, 0, wx.EXPAND | wx.ALL, 5)
        code = rur_editor(panel, -1)
        code.SetText(self.question.code)
        code.SetReadOnly(True)
        sizer.Add(code, 2, wx.EXPAND)
        if len(self.question.choices) > 0:
            self.choices = wx.RadioBox(panel, -1, 'Select your answer choice', choices=self.question.choices, majorDimension=len(self.question.choices), style=wx.RA_SPECIFY_ROWS)
            if 'answer' in self.question.__dict__:
                self.choices.SetSelection(self.question.answer)
            self.choices.SetFocus()
            sizer.Add(self.choices, 0, wx.EXPAND | wx.ALL, 5)
        else:
            header = wx.StaticText(panel, -1, 'Enter your answer below')
            sizer.Add(header, 0, wx.EXPAND | wx.TOP | wx.LEFT, 5)
            self.shortAns = wx.TextCtrl(panel, -1, '', style=wx.TE_MULTILINE)
            if 'answer' in self.question.__dict__:
                self.shortAns.SetValue(self.question.answer)
            self.Bind(wx.EVT_TEXT, self.FinishStatus, self.shortAns)
            self.shortAns.SetFocus()
            sizer.Add(self.shortAns, 1, wx.EXPAND | wx.ALL, 5)

        prev = wx.Button(panel, -1, 'Previous')
        next = wx.Button(panel, -1, 'Next')
        self.done = wx.Button(panel, -1, 'Finish')
        buttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonsizer.Add(prev, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        buttonsizer.Add(next, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        buttonsizer.Add(self.done, 1, wx.ALIGN_CENTER | wx.ALL, 5)

        sizer.Add(buttonsizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
        panel.SetSizer(sizer)

        wx.EVT_CLOSE(self, self.OnClose)

        self.Bind(wx.EVT_BUTTON, self.OnPrev, prev)
        self.Bind(wx.EVT_BUTTON, self.OnNext, next)
        self.Bind(wx.EVT_BUTTON, self.OnClose, self.done)

        if i == 0:
            prev.Disable()
        if i == len(source)-1:
            next.Disable()
        self.FinishStatus()

        self.Show(True)

    def FinishStatus(self, event=None):
        self.SaveAnswer()
        if self.CheckComplete():
            self.done.Enable()
        else:
            self.done.Disable()

    def CheckComplete(self):
        complete = True
        for question in self.source:
            if 'answer' not in question.__dict__:
                complete = False
                break
        return complete

    def SaveAnswer(self):
        if len(self.question.choices) > 0:
            self.question.answer = self.choices.GetSelection()
        else:
            self.question.answer = self.shortAns.GetValue()
            if self.question.answer == "":
                del self.question.answer

    def OnPrev(self, event):
        self.SaveAnswer()
        TestScreen(None, -1, self.title, self.source, self.i-1, self.exitOnClose)
        self.Destroy()
        event.Skip()
        

    def OnNext(self, event):
        self.SaveAnswer()
        TestScreen(None, -1, self.title, self.source, self.i+1, self.exitOnClose)
        self.Destroy()
        event.Skip()

    def OnClose(self, event):
        self.SaveAnswer()
        complete = self.CheckComplete()
        if complete and not self.exitOnClose:
            dlg = wx.MessageDialog(self, "Now you will begin a RUR-PLE problem set.", style = wx.OK)
            dlg.ShowModal()
            dlg.Destroy()

            Splash = MySplashScreen()
            Splash.Show()
            self.Destroy()
            event.Skip()
        else:
            if not complete:
                ret = dialogs.messageDialog(_('Are you sure you want to exit?'),
                                            _("About to close"), wx.YES | wx.NO
                                            | wx.ICON_QUESTION | wx.STAY_ON_TOP)
            else:
                ret = wx.ID_YES
            
            if ret == wx.ID_YES:
                if self.exitOnClose and logData: # log post-test data
                    logdir = os.path.join(logDataDir, 'StudentFiles', 'Logs')
                    tstdir = os.path.join(logDataDir, 'StudentFiles', 'Tests')
                    f1 = open(os.path.join(logdir, str(user_id) + '_posttest.txt'), 'w')
                    f2 = open(os.path.join(tstdir, str(user_id) + '_posttest.txt'), 'w')
                    for i, question in enumerate(self.source):
                        if 'answer' in question.__dict__:
                            correct = question.check()
                            f1.write(str(i) + ',' + str(correct) + '\n')
                            f2.write(repr(question.answer) + '\n')
                    f1.close()
                    f2.close()
                    dlg = wx.MessageDialog(self, "You have completed all of the required problems. We invite you to give us feedback.", "Complete", style = wx.OK)
                    dlg.ShowModal()
                    dlg.Destroy()
                    Notes(None, -1, 'Notes')

                self.Destroy()
                event.Skip()


class MySplashScreen(wx.SplashScreen):
    def __init__(self):
        wx.SplashScreen.__init__(self, getImage(images.SPLASH_SCREEN),
                wx.SPLASH_CENTRE_ON_SCREEN|wx.SPLASH_TIMEOUT, 100, None, -1,
                style = wx.SIMPLE_BORDER|wx.FRAME_NO_TASKBAR|wx.STAY_ON_TOP)
        wx.EVT_CLOSE(self, self.OnClose)

    def OnClose(self, evt):
        dummy = RURApp()
        evt.Skip()

if __name__ == "__main__": 
    App = wx.PySimpleApp(0) # (1) redirects print output to window;
                            # (0) to terminal
                            
    settings = conf.getSettings()
    settings.SCREEN = wxutils.getscreen()

    if 'skip' in sys.argv:
        Splash = MySplashScreen()
        Splash.Show()
    else:
        LoginScreen(None, -1, 'Login Screen')
    App.MainLoop()
