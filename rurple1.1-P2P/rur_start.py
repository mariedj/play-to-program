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
# Run python in export VERSIONER_PYTHON_VERSIONER=2.5
# setenv VERSIONER_PYTHON_VERSION 2.5
# export VERSIONER_PYTHON_PREFER_32_BIT=yes

# Changes made by Robert Deloatch

# todo: consider adding support for translation of commands e.g.
# todo: ...  francais()  initialises commands equivalent like avance(), etc.
# todo: create easy install for windows (exe file)
# todo: create easy install for linux  (setup.py...)
# todo: consider adding new page in notebook for turtle graphics.

import os
import sys
import random
import wx.html as html

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

import rur_py.images as images # load all images
from rur_py.images import getImage
import rur_py.dialogs as dialogs # contains dialogs and exception classes
from rur_py.translation import _

from rur_py.sash import MySashWindow
from rur_py.lightning import EditorSashWindow
import rur_py.parser as parser
from rur_py.bouton import pythonChoiceWindow

from rur_py.cpu import rur_program
import rur_py.browser as browser
import rur_py.event_manager as event_manager
from rur_py.status_bar import rurStatusBar

# global variable defined for convenience; contains user program
code = ""
user_name = ""
user_id = 0
SUBMITTED = 1
TEST_RUN = 2
STEP = 3

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
 
    def ShowInstructions(self):
        status_bar = self.parent.status_bar
        # status_bar is dead during shutdown so check if it's alive.
        if status_bar:
            arg = status_bar.notebook_new_page, 0
            event_manager.SendCustomEvent(self.parent, arg)

class RURApp(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 
                          _("RUR: a Python Learning Environment"),
                          size = (settings.SCREEN[0], settings.SCREEN[1]),
                          style=wx.DEFAULT_FRAME_STYLE)
        self.raw_code = ""
        self.filename = ""
        self.world_filename = ""
        self.isPaused = False
        self.isRunning = False
        self.isStepped = False
        self.status_bar = rurStatusBar(self)
        self.SetStatusBar(self.status_bar)
        self.problemNumber = 0
        self.problem_choice = [0, 1, 2, 3, 4]

        # icon on top left of window
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(getImage(images.ICON))
        self.SetIcon(icon)
        #
        self.Show(True)
        self.window = RURnotebook(self)
        #
        win = browser.TestHtmlPanel(self.window, self)
        self.browser_win = browser.TestHtmlPanel(self.window, self)
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

#----Helper functions
    #Modified from original Source
    def chooseWorld(self):
        #Make a dictionary corresponding to world names
        #Choose randomly from the dictionary index
        #used to parse the path for the problem to add to the name
        startingPoint = -7


        #Two dictionaries coresspond
        #May need to may one dictionary that corresponds to a class which
        #contains the problem .wld and the directions .htm
        dict = {0:'problem1.wld', 1:'problem2.wld', 2:'problem3.wld', 3:'problem4.wld', 4:'problem5.wld'}
        dict_ins = {0:'prob1.htm', 1:'prob2.htm', 2:'prob3.htm', 3:'prob4.htm', 4:'prob5.htm'}
        if len(self.problem_choice) > 0:
            temp = random.randint(0, len(self.problem_choice) - 1)
            n = self.problem_choice[temp]
            del(self.problem_choice[temp])
        

            inst_screen = InstructionScreen(None, -1, 'Instruction Screen')
            inst_screen.setInstructions(dict_ins[n])
     
            #Based on what problem it is change the browswer screen
            #Pass n to a function that changes the browser screen
            #May need to pass the dict
            #self.browser_win.problemChanged(dict_ins, n)
            self.browser_win.name = os.path.join(self.browser_win.lessons_dir,
                                                 'intro/' + dict_ins[n])
            


            if settings.USER_WORLDS_DIR[startingPoint:] != 'samples':
                openedFileName = settings.USER_WORLDS_DIR + '/samples/' + dict[n]
            else:
                openedFileName = settings.USER_WORLDS_DIR + '/' + dict[n]
            return openedFileName
        else:
            #todo: clean this up w/ a pop-up
            sys.exit(-1)

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
                    self.Destroy()
        else:
            self.Destroy()

#---- World file methods
    def OpenWorldFile(self, dummy):
        if self.isRunning:
            return

#        openedFileName = dialogs.openDialog(_("Choose a file"),
#            _("World files (*.wld)|*.wld| All files (*.*)|*.*"),
#            "", settings.USER_WORLDS_DIR)

        #Will be some function that handles problem selection
        openedFileName = self.chooseWorld()
        self.problemNumber += 1

        if openedFileName != "":
            self.world_filename = openedFileName
            self.ReadWorldFile()
            self.UpdateWorld()
            self.user_program.clear_trace()
            settings.USER_WORLDS_DIR = os.path.dirname(self.world_filename)
            arg = self.status_bar.world_field, \
                  os.path.basename(self.world_filename)
            event_manager.SendCustomEvent(self, arg)

    def ReadWorldFile(self):
        if self.isRunning:
            return
        txt = open(self.world_filename, 'r').read()
        txt = parser.FixLineEnding(txt)
        flag = parser.ParseWorld(txt)
        if flag:
            self.backup_dict = {} # used to 'reset' the world
            exec txt in self.backup_dict # extracts avenues, streets, robot,
                                     # walls and beepers

    def Reset(self, dummy):
        if self.isRunning:
            return
        self.UpdateWorld()

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

    #Added to submit the code and proceed to next question
    #Modified from original source
    def Submit(self, dummy):
        if self.isRunning:
            return
        self.SaveProgramFile(SUBMITTED)
        self.SaveWorldFile(SUBMITTED)
        self.OpenWorldFile(0)

        self.ProgramEditor.SetText("")

    def SaveWorldFile(self, dummy):
        '''Saves in .config
        '''
        if self.isRunning:
            return
        txt = self.WorldDisplay.UpdateEditor()

        self.world_filename = str(user_id) + '_world_' + str(self.problemNumber) + '.txt'
        
        dirHome = os.getcwd()
        dir = self.getUserDir()
#        student_dirs = dir + "/StudentFiles/Worlds/"
        student_dirs = os.path.join(dir, 'StudentFiles', 'Worlds')
        try:
            os.makedirs(student_dirs)
        except OSError:
            pass

        os.chdir(student_dirs)
        file = open(self.world_filename, "a+")
        file.write(txt + "\n\n------------End of Run-----------\n\n")
        file.close()

        os.chdir(dirHome)


        arg = self.status_bar.world_field, \
              os.path.basename(self.world_filename)
        event_manager.SendCustomEvent(self, arg)
        settings.SAMPLE_WORLDS_DIR = os.path.dirname(self.world_filename)
        # save a backup copy to 'reset world'
        self.backup_dict = {}
        exec txt in self.backup_dict



#----- Program files methods

    def OpenProgramFile(self, dummy):
        if self.isRunning:
            return

#        openedFileName = dialogs.openDialog(_("Choose a file"),
#           _("Program files (*.rur)|*.rur| All files (*.*)|*.*"),
#            "", settings.USER_PROGS_DIR)

        openedFileName = ""

        if openedFileName != "":
            global code
            self.filename = openedFileName
            arg = self.status_bar.program_field, \
                  os.path.basename(self.filename)
            event_manager.SendCustomEvent(self, arg)
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
    
    def getUserDir(self):
        '''Returns the user directory, i.e. the place where user specific
        data are stored.
        @return (str): the platform dependent user directory.
        '''
        platform = sys.platform

        userdir = ''
        if platform in ('linux2', 'darwin', 'cygwin') or os.name == 'posix':
            home = os.path.expanduser('~')
            if home != '~':
                userdir = os.path.join(home, '.config', 'rurple')
        elif platform == 'win32':
            if 'APPDATA' in  os.environ:
                userdir = os.path.join(os.environ['APPDATA'], 'rurple')

        if userdir == '':
            userdir =  os.path.join(tempfile.gettempdir(), 'rurple')

        return userdir


    def SaveProgramFile(self, dummy):
        #IF NOT in step mode. Useful so that each step doesnt append
        if self.isRunning or self.user_program.isStepped:
            return
        global code
        code = self.ProgramEditor.GetText()
        no_error, mesg = parser.ParseProgram(code)
        if no_error:
#            savedFileName = savedFileName = dialogs.checkedSaveDialog(
#                code,
#                _("Save new program as"),
#                _("Program files (*.rur)|*.rur| All files (*.*)|*.*"),
#                self.filename, settings.USER_PROGS_DIR)
            
#            self.filename = savedFileName
#            print settings.USER_PROGS_DIR
            self.filename = str(user_id) + '_code_' + str(self.problemNumber) + '.txt'


            
            dirHome = os.getcwd()
            dir = self.getUserDir()
            student_dirs = os.path.join(dir, 'StudentFiles', 'SourceCode')
#            student_dirs = dir + "/StudentFiles/SourceCode/"
            try:
                os.makedirs(student_dirs)
            except OSError:
                pass

            os.chdir(student_dirs)
            if dummy == SUBMITTED:
                proc = "Submitted"
            elif dummy == TEST_RUN:
                proc = "Test Run"
            else:
                proc = "Step"
            file = open(self.filename, "a+")
            file.write(code + "\n\n--------------" + proc + "----------\n")
            file.write("--------------End of Run-----------\n\n")
            file.close()

            os.chdir(dirHome)
            arg = self.status_bar.program_field, \
                  os.path.basename(self.filename)
#            print arg
            event_manager.SendCustomEvent(self, arg)
            settings.USER_PROGS_DIR = os.path.dirname(self.filename)
            self.ProgramEditor.SetSavePoint()
        else:
            code = ""
            dialogs.messageDialog(mesg, _("Program will not be saved."))

#--- Program controls

    def RunProgram(self, dummy):
        self.SaveProgramFile(TEST_RUN)
        if self.user_program.isRunning:
            if self.user_program.isPaused or self.user_program.isStepped:
                self.user_program.isStepped = False
                self.Pause(None)
            return
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
        self.SaveProgramFile(STEP)
        self.user_program.isStepped = True
        if not self.user_program.isRunning:
            self.RunProgram(None)
        else:
            self.Pause(None)
        self.SaveWorldFile(TEST_RUN)

    def StopProgram(self, dummy):
        self.user_program.StopProgram()
        arg = self.status_bar.running_field, _("Program not running")
        event_manager.SendCustomEvent(self, arg)
        self.user_program.stopped_by_user = True

    def StartSession(self, dummy):
        if self.isRunning:
            return
        self.OpenWorldFile(0)
        self.ProgramEditor.SetText("")

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

    def AddRemoveRobot(self, dummy):
        if self.user_program.isRunning:
            return
        if self.world.robot_dict:
            # remove all robots from non-empty dict
            self.world.robot_dict = {}
            arg = self.status_bar.beeper_field, self.status_bar.no_robot
        else:
            self.world.robot_dict = {}
            self.world.addOneRobot(name='robot')
            self.backup_dict['robot'] = self.world.robot_dict[
                                                       'robot']._getInfoTuple()
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
        frameX = 500
        frameY = 800
        wx.Frame.__init__(self, parent, id, title, size=(frameX, frameY))
        largeFont = wx.Font(36, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_BOLD)        
        buttonFont = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_BOLD)
        labelFont = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_BOLD)

        label = wx.StaticText(self, -1, 'Welcome to the Playing', (30, 10))
        label2 = wx.StaticText(self, -1, 'to Program System!', (60, 50))
        label.SetFont(largeFont)
        label2.SetFont(largeFont)


        promptLabel = wx.StaticText(self, -1, 'Please Enter your information below.',
                                    (20, 150))
        firstNameLabel =  wx.StaticText(self, -1, 'First Name: ',
                                    (20, 180))
        lastNameLabel = wx.StaticText(self, -1, 'Last Name: ',
                                    (20, 210))
        ageLabel = wx.StaticText(self, -1, 'Age: ', (20, 240))
        #courseLevelLabel =  wx.StaticText(self, -1, 'Highest CMSC Course Completed: ',
        #                            (20, 240))
        umbcEmailLabel = wx.StaticText(self, -1, 'UMBC Email: ',
                                    (20, 270))
        domainLabel =  wx.StaticText(self, -1, '@umbc.edu',
                                    (300, 270))
        sexLabel = wx.StaticText(self, -1, 'Sex: ', (20, 300))
        creditLabel = wx.StaticText(self, -1, 'Credit Count: ', (20, 330))
        transferLabel = wx.StaticText(self, -1, 'Are you a transfer student? ', (20, 360))
        courseLabel = wx.StaticText(self, -1, "Please enter the courses you have completed and the", 
                                    (20, 390))
        courseLabel2 = wx.StaticText(self, -1, "grade that you earned in each.",
                                     (20, 420))

        courseNameLabel = wx.StaticText(self, -1, "Course", 
                                        (20, 450))
        courseGradeLabel = wx.StaticText(self, -1, "Grade",
                                         (250, 450))

        promptLabel.SetFont(buttonFont)
        firstNameLabel.SetFont(labelFont)
        lastNameLabel.SetFont(labelFont)
#        courseLevelLabel.SetFont(labelFont)
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
        
        firstName = wx.TextCtrl(self, -1, '', (120, 180), size = (150, 20))
        lastName = wx.TextCtrl(self, -1, '', (120, 210), size = (150, 20))
        #cmscLevel = wx.TextCtrl(self, -1, '', (300, 240), size = (150, 20))
        self.email = wx.TextCtrl(self, -1, '', (120, 270), size = (150, 20))
        age = wx.TextCtrl(self, -1, '', (120, 240), size = (30, 20))
        sex = wx.Choice(self, -1, (120, 300), (100, 20), ["Male", "Female"])
        creditCount = wx.TextCtrl(self, -1, '', (150, 330), size = (70, 20))
        isTransfer = wx.Choice(self, -1, (250, 360), (70, 20), ["Yes", "No"])
        
        course1 = wx.TextCtrl(self, -1, '', (20, 480), size = (70, 20))
        course2 = wx.TextCtrl(self, -1, '', (20, 510), size = (70, 20))
        course3 = wx.TextCtrl(self, -1, '', (20, 540), size = (70, 20))
        course4 = wx.TextCtrl(self, -1, '', (20, 570), size = (70, 20))
        course5 = wx.TextCtrl(self, -1, '', (20, 600), size = (70, 20))
        course6 = wx.TextCtrl(self, -1, '', (20, 630), size = (70, 20))

        grades = ["A", "B", "C", "D", "F", "P", "I", "Currently Enrolled"]
        grade1 = wx.Choice(self, -1, (250, 480), (200, 20), grades)
        grade2 = wx.Choice(self, -1, (250, 510), (200, 20), grades)
        grade3 = wx.Choice(self, -1, (250, 540), (200, 20), grades)
        grade4 = wx.Choice(self, -1, (250, 570), (200, 20), grades)
        grade5 = wx.Choice(self, -1, (250, 600), (200, 20), grades)
        grade6 = wx.Choice(self, -1, (250, 630), (200, 20), grades)

        

        button1 = wx.Button(self, -1, 'Create', pos = wx.Point(70, 700), 
                            size = wx.Size(300, 1000))
        button1.SetFont(buttonFont)

        self.Bind(wx.EVT_BUTTON, self.OnCreate, id=button1.GetId())

        self.Show(True)
    
    def OnCreate(self, event):
        global user_name
        global user_id
        directory = os.getcwd()
        os.chdir(os.getcwd())
        logfile = open("key.txt", "a+")
        user_name = self.email.GetValue()
        user_id = random.randint(0, 4000)
        logfile.write(user_name + "     " + str(user_id) + "\n")
        dummy = RURApp()
        self.Destroy()
        event.Skip()
        
class ReturnUserScreen(wx.Frame):
    def __init__(self, parent, id, title):
        frameX = 500
        frameY = 500
        wx.Frame.__init__(self, parent, id, title, size=(frameX, frameY))
        largeFont = wx.Font(36, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_BOLD)        
        buttonFont = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_BOLD)
        labelFont = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_BOLD)

        label = wx.StaticText(self, -1, 'Welcome to the Playing', (30, 10))
        label2 = wx.StaticText(self, -1, 'to Program System!', (60, 50))
        label.SetFont(largeFont)
        label2.SetFont(largeFont)

        promptLabel = wx.StaticText(self, -1, 'Please Enter your information below.',
                                    (20, 150))
        umbcEmailLabel = wx.StaticText(self, -1, 'UMBC Email: ',
                                    (20, 180))
        domainLabel =  wx.StaticText(self, -1, '@umbc.edu',
                                    (300, 180))
        promptLabel.SetFont(buttonFont)
        umbcEmailLabel.SetFont(labelFont)
        domainLabel.SetFont(labelFont)
        
        self.email = wx.TextCtrl(self, -1, '', (120, 180), size = (150, 20))
        
        button1 = wx.Button(self, -1, 'Login', pos = wx.Point(70, 400), 
                            size = wx.Size(300, 1000))
        button1.SetFont(buttonFont)

        self.Bind(wx.EVT_BUTTON, self.OnLogin, id=button1.GetId())

        self.Show(True)
    
    def OnLogin(self, event):
        #Check if umbc name is in logfile
        global user_id
        file = open("key.txt", "r")
        studentFound = False
        for line in file:
            student = line.split()
            print student
            if student[0] == self.email.GetValue():
                studentFound = True
                user_id = int(student[1])
        if studentFound:
            dummy = RURApp()
            self.Destroy()
            event.Skip()
        else:
            #todo: Clean this up, create a pop-up asking for a different loging
            sys.exit(-1)


class InstructionScreen(wx.Frame):
    def __init__(self, parent, id, title):
        frameX = 500
        frameY = 500
        wx.Frame.__init__(self, parent, id, title, size=(frameX, frameY))
        self.lessons_dir = conf.getLessonsNlDir()
        self.html = html.HtmlWindow(self, id, size=(frameX, frameY))
        #style=wx.NO_FULL_REPAINT_ON_RESIZE)

        self.labelFont = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_BOLD)

        wx.EVT_CLOSE(self, self.OnClose)
        

        self.Show(True)

    def OnClose(self, event):
        self.Destroy()
        event.Skip()

    def setInstructions(self, ins):
        htmlFiles = os.getcwd() + "/lessons/en/intro/"
                
        page = htmlFiles + ins

        self.html.LoadPage(page)
        

#        label2 = wx.StaticText(self, -1, 'Instructions', (0, 30))
#        label2.SetFont(self.labelFont)
		
        #os.path.join(self.browser_win.lessons_dir,'intro/' + dict_ins[n])
        #page = os.path.join(self.lessons_dir, 'help.htm')
        #self.html.LoadPage(page)
		


#Added for Login Screen
#Modified From original rur-ple code
class LoginScreen(wx.Frame):
    def __init__(self, parent, id, title):
        frameX = 500
        frameY = 500
        wx.Frame.__init__(self, parent, id, title, size=(frameX, frameY))
        largeFont = wx.Font(36, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_BOLD)        

        buttonFont = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_BOLD)

        label = wx.StaticText(self, -1, 'Welcome to the Playing', (30, 10))
        label2 = wx.StaticText(self, -1, 'to Program System!', (60, 50))
        label.SetFont(largeFont)
        label2.SetFont(largeFont)

        button1 = wx.Button(self, -1, 'New User', pos = wx.Point(70, 200), 
                            size = wx.Size(300, 1000))
        button2 = wx.Button(self, -1, 'Returning User', pos = wx.Point(70, 300), 
                            size = wx.Size(300, 1000))
        button1.SetFont(buttonFont)
        button2.SetFont(buttonFont)


        wx.EVT_CLOSE(self, self.OnClose)

        self.Bind(wx.EVT_BUTTON, self.OnNewUser, id=button1.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnReturnUser, id=button2.GetId())

      #  textLogin = wx.TextCtrl(self, -1, '', (10, 40), size = (frameX-20, 20))
        
        

        self.Show(True)

    def OnNewUser(self, event):
#        dummy = RURApp()
        self.Destroy()
        NewUserScreen(None, -1, 'New User')
        event.Skip()
        

    def OnReturnUser(self, event):
        self.Destroy()
        ReturnUserScreen(None, -1, 'Returning User')
        event.Skip()

    def OnClose(self, event):
        self.Destroy()
        event.Skip()


class MySplashScreen(wx.SplashScreen):
    def __init__(self):
        wx.SplashScreen.__init__(self, getImage(images.SPLASH_SCREEN),
                wx.SPLASH_CENTRE_ON_SCREEN|wx.SPLASH_TIMEOUT, 100, None, -1,
                style = wx.SIMPLE_BORDER|wx.FRAME_NO_TASKBAR|wx.STAY_ON_TOP)
        wx.EVT_CLOSE(self, self.OnClose)

    def OnClose(self, evt):
        #Change for creating loginScreen
        LoginScreen(None, -1, 'Login Screen')
        evt.Skip()

if __name__ == "__main__": 
    App = wx.PySimpleApp(0) # (1) redirects print output to window;
                            # (0) to terminal
                            
    settings = conf.getSettings()
    settings.SCREEN = wxutils.getscreen()

    Splash = MySplashScreen()
    Splash.Show()
    App.MainLoop()
