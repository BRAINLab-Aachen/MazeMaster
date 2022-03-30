# -*- coding: utf-8 -*-
"""
Created on Tue June 12 09:16:21 2018

@author: bexter 
"""
import tkinter as tk
import datetime
import configparser
import os
import time
import csv
import ast
from win32api import GetSystemMetrics
from PIL import Image, ImageTk
from tkinter import messagebox as mbox
from tkinter import simpledialog

from MM_trial import Trials 
import var
import Timing

class GUI:

    def __init__(self, master):
        self.connectTo = tk.StringVar()
        self.connectTo.set('Blender')
        self.LStepNo = tk.Label()
        self.eLengthTrialDist = tk.Entry()
        self.eFileBaseName = tk.Entry()
        self.saveFilesTo = tk.Entry()
        self.eDataDir = tk.Entry()
        self.eValveOpen = tk.Entry()
        self.eRunSpeed = tk.Entry()
        self.ePuffDuration = tk.Entry()
        self.expType = tk.StringVar()
        self.expType.set('Undefined')
        self.pupilCam = tk.BooleanVar()
        self.pupilCam.set(False)
        self.randReplay = tk.BooleanVar()
        self.randReplay.set(False)
        self.autoReward = tk.BooleanVar()
        self.autoReward.set(False)
        self.winConfig = configparser.ConfigParser()
        self.winConfig.read('windowconf.ini')
        self.useRules = tk.BooleanVar() ###--->not in use
        self.useRules.set(True)
        self.Exit = False
        self.useConstantSpeed = False
        self.bg = master.cget("background")
        self.x_lag = -840


        # create Canvas
        self.Canvas = tk.Canvas(master,
                            width=float(self.get('Main Window', 'w_width')),
                            height=float(self.get('Main Window', 'w_height')),
                            bg="#EDEDED")

        #load window position
        master.geometry("+"+str(self.get('Last Window Positions', 'main_x')) +
                        "+"+str(self.get('Last Window Positions', 'main_y')))

        # load icons
        self.MazePhoto = tk.PhotoImage(file="icons/Maze.gif")
        self.StartPhoto = tk.PhotoImage(file="icons/Start.gif")
        self.StopPhoto = tk.PhotoImage(file="icons/Stop.gif")
        self.Reset = tk.PhotoImage(file="icons/reset.gif")
        self.ExitPhoto = tk.PhotoImage(file="icons/Exit.gif")
        self.PlayPhoto = tk.PhotoImage(file="icons/Play.gif")
        self.TrackPhoto = tk.PhotoImage(file="icons/Track.gif")
        self.CuePhoto = tk.PhotoImage(file="icons/CueNew.gif")
        self.CueDropPhoto = tk.PhotoImage(file="icons/CueDrop.gif")
        self.OpenPhoto = tk.PhotoImage(file="icons/Open.gif")
        self.SavePhoto = tk.PhotoImage(file="icons/Save.gif")
        self.NewTrialPhoto = tk.PhotoImage(file="icons/newTrial.gif")
        self.HelpPhoto = tk.PhotoImage(file="icons/Help.gif")
        self.CamPhoto = tk.PhotoImage(file="icons/cam.gif")
        self.ScreenPhoto = tk.PhotoImage(file="icons/screen.gif")


    # =========================================================================
    # Get/Set window positions
    # =========================================================================

    def get(self, window_name, field_name):
        return self.winConfig.get(window_name, field_name)

    def set_value(self, group_name, field_name, value):
        self.winConfig[group_name][field_name] = str(value)
        with open('windowconf.ini', 'w+') as configfile:
            self.winConfig.write(configfile)
            
    # =========================================================================
    # Maze panel
    # =========================================================================

    def openMazeBuilder(self):
        from subprocess import call
        import os
        print("Open Maze Builder")
        #path_py = r"C:\Users\georgiou\Software\venv\Scripts\python.exe"
        #call(['python', '-i', "MazeBuilder/MazeBuilderV2.py"])

        call(["MazeBuilder/MazeBuilderV2.exe"])

    def MazePanel(self, config: object, MMversion: object, maze: object, 
                  Data: object,

                  
                  GUIRules: object, windows):
        """
        :param maze: object
        :param var.MMversion: object
        """
        button_height = 50
        button_y = 70

        # session Time
        self.LSessionTime = tk.Label(
            self.Canvas, 
            text="Session Time: 00:00:00",
            font='Verdana 10')
        self.LSessionTime.place(
            x=float(self.get('maze_grid', 'xpos')), 
            y=float(self.get('maze_grid', 'ypos'))-15)

        # set Maze Master title
        self.MM_logo_pic = tk.PhotoImage(file="icons/MM_logo_small.png")
        tk.Label(
            self.Canvas, 
            image=self.MM_logo_pic).place(
                x=float(self.get('maze_grid', 'xpos')) +180, y=0)

        # set title in window
        self.LmTitle = tk.Label(
            self.Canvas, 
            text="Maze: " + config.get('Files', 'MazeFile'), 
            font='Verdana 12')
        self.LmTitle.place(
            x=float(self.get('maze_grid', 'xpos')), 
            y=float(self.get('maze_grid', 'ypos'))+10)

        # version
        tk.Label(
            self.Canvas,
            text="v. " + var.MMversion, 
            font="Verdana 8").place(
                x=float(self.get('maze_grid', 'xpos')) - 2000,
                y=float(self.get('maze_grid', 'ypos')) - 60)

        tk.Button(
            self.Canvas, 
            text="Load Maze", 
            image=self.OpenPhoto, 
            compound="bottom",
            command=lambda: maze.load_maze(self, GUIRules, config)).place(
                x=15,
                y=button_y, width=100, height=button_height)

        tk.Button(
            self.Canvas, 
            text="Maze Designer", 
            image=self.MazePhoto, 
            compound="bottom",
            command=self.openMazeBuilder).place(
                x=15+110,
                y=button_y, width=100, height=button_height)
        

        tk.Button(
            self.Canvas, 
            text="Exit", 
            image=self.ExitPhoto, 
            compound="bottom",
            command=lambda: self.quitMM(Data)).place(
                x=15+110+120,
                y=button_y, width=100, height=button_height)


    # =========================================================================
    # Server Panel
    # =========================================================================
    def MoveBlender(self):
        import win32gui

        def enumHandler(hwnd, lParam):
            """

            :type hwnd: object
            """
            if self.expType.get() == "VirtualTunnel":
                win_x = 3840
                win_y = 0
                win_x_end = 3840
                win_y_end = 1080 + 10
            else:
                win_x = 1920
                win_y = 0
                win_x_end = 5400
                win_y_end = 2100
            if win32gui.IsWindowVisible(hwnd):
                if 'Blender' in win32gui.GetWindowText(hwnd):
                    win32gui.MoveWindow(hwnd, win_x, win_y, win_x_end,
                                        win_y_end, True)

        win32gui.EnumWindows(enumHandler, None)

    def resetWindows(self, windows):
        x = int(GetSystemMetrics(0)-float(self.get('Main Window', 
                'w_width')))-10
        windows[0].geometry("+"+str(x)+"+0")

        x = 0
        windows[1].geometry("+"+str(x)+"+0")

    def saveWindows(self, windows):
        def parsegeometry(geometry):
            geometry = geometry.replace('x', ' ').replace('+', ' ').replace('-', ' ').split()
            return [int(geometry[i]) for i in range(4)]
        
        pos = list(parsegeometry(windows[0].geometry()))
        self.set_value('Last Window Positions', 'main_x', pos[2])
        self.set_value('Last Window Positions', 'main_y', pos[3])
        
        pos = list(parsegeometry(windows[1].geometry()))
        self.set_value('Last Window Positions', 'maze_x', pos[2])
        self.set_value('Last Window Positions', 'maze_y', pos[3])
        
        print("Window positions saved")
        
    def ServerControlPanel(self, server, data, trial, config, stim, maze, 
                           rules, GUIrules):
        button_height = 50
        tk.LabelFrame(self.Canvas,
                      text=self.get(' Server Control ', 'name'), 
                      font="Verdana 8 bold", fg='black', bd=6,
                      width=float(self.get(' Server Control ', 'width')),
                      height=float(self.get(' Server Control ', 'height')),
                      labelanchor='n',
                      relief=tk.RIDGE
                      ).place(x=float(self.get(' Server Control ', 'xpos')),
                              y=float(self.get(' Server Control ', 'ypos')))

        self.connectTo.set('Blender')
        
        tk.Label(
            self.Canvas,
            text="Engine:"
            ).place(
                x=float(self.get(' Server Control ', 'xpos')) \
                + float(self.get('Main Window', 'h_dist_inframe')) + 115,
                y=float(self.get(' Server Control ', 'ypos')) + 20)
        optMenu = tk.OptionMenu(
            self.Canvas, self.connectTo, "PsychoPy", "Blender"
            )
        optMenu.place(
                x=float(self.get(' Server Control ', 'xpos')) \
                + float(self.get('Main Window', 'h_dist_inframe'))+115,
                y=float(self.get(' Server Control ', 'ypos')) + 40,
                width=100, height=button_height/2)
        optMenu.configure(state=tk.DISABLED)
        

        tk.Label(self.Canvas,
            text="Server Status", font="Verdana 10",
            ).place(
                x=float(self.get(' Server Control ', 'xpos')) \
                + float(self.get('Main Window', 'h_dist_inframe')),
                y=float(self.get(' Server Control ', 'ypos')) + 15)

        self.LOnline = tk.Label(
            self.Canvas,
            text="offline", foreground='RED', font="Verdana 12")
        self.LOnline.place(
            x=float(self.get(' Server Control ', 'xpos')) \
            + float(self.get('Main Window', 'h_dist_inframe')),
            y=float(self.get(' Server Control ', 'ypos')) + 35)

        tk.Button(
            self.Canvas,
            text="Connect", 
            image=self.StartPhoto, 
            compound="bottom",
            command=lambda: server.start_server(self, data[2], 
                                                self.autostartBlender.get(),
                                                stim, config, maze,
                                                rules, GUIrules)
            ).place(
                x=float(self.get(' Server Control ', 'xpos')) \
                + float(self.get(' Server Control ', 'width')) / 2+70,
                y=float(self.get(' Server Control ', 'ypos')) + 20,
                width=100, height=button_height)

        tk.Button(self.Canvas,
            image=self.StopPhoto,
            text="Disconnect",
            compound="bottom",
            command=lambda: server.stopServer(data, self, trial)
            ).place(
                x=float(self.get(' Server Control ', 'xpos')) \
                + float(self.get(' Server Control ', 'width')) / 2+70,
                y=float(self.get(' Server Control ', 'ypos')) + 20 + 70,
                width=100, height=button_height)

        tk.Label(
            self.Canvas,
            text="Position"
            ).place(
                x=float(self.get(' Server Control ', 'xpos')) \
                + float(self.get('Main Window', 'h_dist_inframe')) ,
                y=float(self.get(' Server Control ', 'ypos')) + 60)
        tk.Label(
            self.Canvas,
            text="Blender window:"
            ).place(
                x=float(self.get(' Server Control ', 'xpos')) \
                + float(self.get('Main Window', 'h_dist_inframe')),
                y=float(self.get(' Server Control ', 'ypos')) + 75)

        tk.Button(
            self.Canvas,
            image=self.ScreenPhoto,
            compound="bottom",
            command=self.MoveBlender
            ).place(
                x=float(self.get(' Server Control ', 'xpos')) \
                + float(self.get('Main Window', 'h_dist_inframe')),#105,
                y=float(self.get(' Server Control ', 'ypos')) + 20 +80,
                width=100, height=button_height-10)
        
        

        self.autostartBlender = tk.BooleanVar(self.Canvas)
        self.autostartBlender.set(
                config.get('conf','autostartBlender')=='True')
        tk.Checkbutton(
            self.Canvas, 
            text="Autostart Blender", 
            command=lambda: self.bStartBlender.configure(
                    state=self.boolToState(not self.autostartBlender.get())),     
            variable=self.autostartBlender).place(
                x=float(self.get(' Server Control ', 'xpos')) \
                + float(self.get('Main Window', 'h_dist_inframe'))+115,
                y=float(self.get(' Server Control ', 'ypos')) + 20 +60)
        
        def startBlender():
            import os
            os.startfile('startBlender.bat')
     
        self.bStartBlender = tk.Button(
            self.Canvas,
            text="Start Blender",
            compound="bottom",
            command=startBlender)
        
        self.bStartBlender.place(
                x=float(self.get(' Server Control ', 'xpos')) \
                + float(self.get('Main Window', 'h_dist_inframe'))+115,
                y=float(self.get(' Server Control ', 'ypos')) + 20 +90,
                width=100, height=button_height/2+5)
        
        self.bStartBlender.configure(state=self.boolToState(
                not self.autostartBlender.get()))


    # =========================================================================
    # General Settings Panel
    # =========================================================================

    def get_task_list(self, settings_config):
        '''
        gives list of possible task depending on the experiment type
        '''
        return ast.literal_eval(settings_config.get('exp',self.expType.get()))

    def _get_file_basename(self):
        """
        Returns an automatic generated file_basename for the running dataset.
        """
        file_basename_list = []

        if self.expType.get() == "VirtualTunnel":
            file_basename_list += ["vt"]
        elif self.expType.get() == "VirtualMaze":
            file_basename_list += ["vm"]

        if self.taskType.get() != "undefined":
            file_basename_list += [self.taskType.get()]

        if self.eMouseID.get() != "":
            file_basename_list += [self.eMouseID.get()]

        file_basename_list += [datetime.date.today().isoformat()]

        if self.eBlockID.get() != "":
            file_basename_list += ["bl-%02d" % int(self.eBlockID.get())]
        #print(file_basename_list) #mdebug
        return "_".join(file_basename_list)
    
    def createSetting(self, task, settings_config):
        """creates a new entry, either for a task or an experiment setting, 
        update the option menu and saves it to the settings file
        task: str (can be "e" for experiment, or "t" for task)
        settings_config : config object"""
        answer = simpledialog.askstring("Input", "Enter name for new entry")

        if task == "e":
            settings_config.set_value("exp", answer, "['undefined']")
            self.exp_type['menu'].add_command(label=answer, 
                         command=tk._setit(self.expType, answer))
        elif task == "t":
            _tasks = ast.literal_eval(settings_config.get('exp', 
                                                          self.expType.get()))
            if answer not in _tasks:
                _tasks.append(answer)
                settings_config.set_value("exp", self.expType.get(), 
                                          str(_tasks))
                settings_config.add_section(answer)
                self.eTaskName['menu'].add_command(label=answer,
                              command=tk._setit(self.taskType, answer))
            else:
                print("tasks already exists, choose new name")

    def deleteSetting(self, task, settings_config):
        """deletes entry in menu and in settings config file
        task: str (can be "e" for experiment, or "t" for task)
        settings_config : config object"""
        if task == "e":
            if self.expType.get() != 'undefined':
                if mbox.askokcancel("Delete", "Do you want to delete %s and all \
                                    associated tasks?" % (self.expType.get())):
                    _exp = settings_config.winConfig.options('exp')
                    
                    indx = _exp.index(self.expType.get())
                    taskname = self.expType.get()
                    #delete entry in menu
                    self.expType.set(_exp[0])
                    self.exp_type['menu'].delete(indx)
                    
                    #delete all associated tasks
                    for task in ast.literal_eval(settings_config.get('exp', 
                                                                    taskname)):
                        settings_config.delete_section(task)
                    
                    #delete entry in config file
                    settings_config.delete_value('exp', taskname)
            else:
                mbox.showerror("Error", "undefined cannot be deleted")
                
        elif task == "t":
            if self.taskType.get() != 'undefined':
                if mbox.askokcancel("Delete", "Do you want to delete %s ?" % 
                                    (self.taskType.get())):
                    _tasks = ast.literal_eval(settings_config.get('exp', 
                                                        self.expType.get()))
                    indx = _tasks.index(self.taskType.get())
                    taskname = self.taskType.get()
                    #delete entry in menu
                    self.taskType.set(_tasks[0])
                    self.eTaskName['menu'].delete(indx)
                    #delete entry in config file
                    if taskname in _tasks:
                        _tasks.remove(taskname)
                        settings_config.set_value("exp", self.expType.get(), 
                                                  str(_tasks))
                    settings_config.delete_section(taskname)
            else:
                mbox.showerror("Error", "undefined cannot be deleted")
        
    def saveSettings(self, settings_config):
        
        if not self.setGenSetManually.get():
                self._update_entry(self.eSILogDir)
                print("helooooo")
                print(self.eSILogDir)
                print("helooooo")
        
        
        options = {
                "useStartTrigger":self.useStartTrigger.get(),        
                "saveTimedTicks":self.saveTimedTicks.get(),
                "autoReward":self.autoReward.get(),
                "biasCorr":self.biasCorr.get(),
                "eRunSpBlender":self.eRunSpBlender.get(),
                "eCueTime":self.eCueTime.get(),
                "autorun":self.autorun.get(),
                "useConstantSpeed":self.useConstantSpeed.get(),
                "eRunSpeed": self.eRunSpeed.get(),
                "eValveOpen": self.eValveOpen.get(),
                "eRewProba": self.eRewProba.get()
                }
        
        #testing for overwrite
        if settings_config.winConfig.has_option(self.taskType.get(), 
                                             "useStartTrigger"):
            if not mbox.askyesno("overwrite?", 
                             "Do you want to overwrite the settings?"):
                return    
                
                
        for key, value in options.items():
            settings_config.set_value(self.taskType.get(), key, 
                                      str(value))
        print("Settings saved!")    
        
    def loadSettings(self, settings_config):
        
        for option in settings_config.winConfig.options(self.taskType.get()):
            value = settings_config.get(self.taskType.get(), option)
            try:
                eval("self."+option).set(value)
            except:
                eval("self."+option).delete(0,tk.END)
                eval("self."+option).insert(0, value)
            
        
    def general_settings_panel(self, meta_data, master, settings_config, config):
        tk.LabelFrame(
            self.Canvas,
            text=self.get(' General Settings ', 'name'), font="Verdana 8 bold",
            fg='black', bd=6,
            width=float(self.get(' General Settings ', 'width')),
            height=float(self.get(' General Settings ', 'height')),
            labelanchor='n',
            relief=tk.RIDGE
            ).place(
                x=float(self.get(' General Settings ', 'xpos')),
                y=float(self.get(' General Settings ', 'ypos')))

        self.saveFilesTo = tk.StringVar(self.Canvas)
        self.saveFilesTo.set('Nowhere')
        self.saveFilesTo.trace("w", lambda *args: self.update_datadir(
                                                    meta_data, config, *args))
        save_to_list = ("Network", "LocalComp", "Nowhere")
        tk.Label(
            self.Canvas,
            text="Save files to:"
            ).place(
                x=float(self.get(' General Settings ', 'xpos')) \
                + float(self.get('Main Window', 'h_dist_inframe')),
                y=float(self.get(' General Settings ', 'ypos')) \
                + float(self.get('Main Window', 'h_dist_inframe')))

        tk.OptionMenu(
            self.Canvas, 
            self.saveFilesTo, 
            *save_to_list
            ).place(
                x=float(self.get(' General Settings ', 'xpos')) + 150,
                y=float(self.get(' General Settings ', 'ypos'))  \
                + float(self.get('Main Window', 'h_dist_inframe')),
                width=float(self.get(' General Settings ', 'width')) / 3 \
                - float(self.get('Main Window', 'h_dist_inframe')),
                height=23)

        self.expType = tk.StringVar(self.Canvas)
        self.expType.set('undefined')
        self.expType.trace(
            "w", 
            lambda *args: self.update_expType_settings(meta_data, 
                                                       settings_config, 
                                                       config, *args))
        #self.exp_type = self.expType.get()
        exp_list = settings_config.winConfig['exp']
        tk.Label(
            self.Canvas,
            text="Choose Experiment:"
            ).place(
                x=float(self.get(' General Settings ', 'xpos')) \
                + float(self.get('Main Window', 'h_dist_inframe')),
                y=float(self.get(' General Settings ', 'ypos')) + 45)
        self.exp_type = tk.OptionMenu(self.Canvas, self.expType, *exp_list)
        self.exp_type.place(
            x=float(self.get(' General Settings ', 'xpos')) + 150,
            y=float(self.get(' General Settings ', 'ypos')) + 45,
            width=float(self.get(' General Settings ', 'width')) / 3 \
            - float(self.get('Main Window', 'h_dist_inframe')),
            height=23)


        tk.Button(
            self.Canvas,
            text="+", fg="black",
            command=lambda: self.createSetting("e", settings_config)
            ).place(
                x=float(self.get(' General Settings ', 'xpos')) + 270,
                y=float(self.get(' General Settings ', 'ypos')) + 45,
                width=20, height=20)
        tk.Button(
            self.Canvas,
            text="x",fg="red",
            command = lambda: self.deleteSetting("e", settings_config)
            ).place(
                x=float(self.get(' General Settings ', 'xpos')) + 295,
                y=float(self.get(' General Settings ', 'ypos')) + 45,
                width=20, height=20)


        self.taskType = tk.StringVar(self.Canvas)
        self.taskType.set('undefined')
        self.taskType.trace_variable(
            "w", 
            lambda *args: self.update_tasktype_settings(meta_data, 
                                                    settings_config,
                                                    config, *args))

        task_list = self.get_task_list(settings_config)
        tk.Label(
            self.Canvas,
            text="Choose Task:"
            ).place(
                x=float(self.get(' General Settings ', 'xpos')) + 20,
                y=float(self.get(' General Settings ', 'ypos')) + 70)
        self.eTaskName = tk.OptionMenu(self.Canvas, self.taskType, *task_list)
        self.eTaskName.place(
            x=float(self.get(' General Settings ', 'xpos')) + 150,
            y=float(self.get(' General Settings ', 'ypos')) + 70,
            width=float(self.get(' General Settings ', 'width')) / 3 \
            - float(self.get('Main Window', 'h_dist_inframe')),
            height=23)

        tk.Button(
            self.Canvas,
            text="+", fg="black",
            command=lambda: self.createSetting("t", settings_config)
            ).place(
                x=float(self.get(' General Settings ', 'xpos')) + 270,
                y=float(self.get(' General Settings ', 'ypos')) + 70,
                width=20, height=20)
        tk.Button(
            self.Canvas,
            text="x",fg="red",
            command= lambda: self.deleteSetting("t", settings_config)
            ).place(
                x=float(self.get(' General Settings ', 'xpos')) + 295,
                y=float(self.get(' General Settings ', 'ypos')) + 70,
                width=20, height=20)

        tk.Button(
            self.Canvas,
            text="save \n settings",
            command = lambda: self.saveSettings(settings_config)
            ).place(
                x=float(self.get(' General Settings ', 'xpos')) + 325,
                y=float(self.get(' General Settings ', 'ypos')) + 45,
                width=50, height=45)
        

        mouse_ID = ""
        tk.Label(
            self.Canvas,
            text="ID Test Subject:"
            ).place(
                x=float(self.get(' General Settings ', 'xpos')) + 20,
                y=float(self.get(' General Settings ', 'ypos')) + 100)
        self.MouseID = tk.StringVar(self.Canvas)
        self.MouseID.trace(
            "w", 
            lambda *args: self.update_metadata__datadir("MouseID", 
                                            self.MouseID, meta_data,
                                            config, *args))

        self.eMouseID = tk.Entry(
            self.Canvas, 
            textvariable=self.MouseID, 
            insertofftime=0, 
            relief=tk.GROOVE, 
            bg="white",
            width=20)
        self.eMouseID.place(
            x=float(self.get(' General Settings ', 'xpos')) + 152,
            y=float(self.get(' General Settings ', 'ypos')) + 100)
        self.eMouseID.insert(0, mouse_ID)

        # ### set_manually_checkbox_frame ####################################
        self.setGenSetManually = tk.BooleanVar()
        self.setGenSetManually.set(False)
        _cSetGenSetManually = tk.Checkbutton(
            self.Canvas,
            text=self.get('set manually', 'name'),
            variable=self.setGenSetManually)
        tk.LabelFrame(
            self.Canvas,
            labelwidget=_cSetGenSetManually, bd=2,
            width=float(self.get('set manually', 'width')), 
            height=float(self.get('set manually', 'height')),
            labelanchor='n', relief=tk.RIDGE
            ).place(
                x=float(self.get('set manually', 'xpos')),
                y=float(self.get('set manually', 'ypos')))

        tk.Label(
            self.Canvas,
            text="Data directory:"
            ).place(
                x=float(self.get('set manually', 'xpos')) + 10,
                y=float(self.get('set manually', 'ypos')) + 20)

        self.eDataDir = tk.Entry(
            self.Canvas,
            insertofftime=0, 
            relief=tk.GROOVE, 
            bg="white", width=38)
        self.eDataDir.place(
            x=float(self.get('set manually', 'xpos')) + 15,
            y=float(self.get('set manually', 'ypos')) + 40)

        data_dir = ''
        self.eDataDir.insert(0, data_dir)
        self.eDataDir.configure(state='readonly')

        tk.Label(self.Canvas,
                 text="SI log directory:"
                 ).place(x=float(self.get('set manually', 'xpos')) + 10,
                         y=float(self.get('set manually', 'ypos')) + 60)

        self.SILogDir = tk.StringVar(master)
        self.SILogDir.trace(
            "w", lambda *args: self.updateSILogDir(meta_data, *args))

        self.eSILogDir = tk.Entry(
            self.Canvas, 
            textvariable=self.SILogDir, 
            insertofftime=0, 
            relief=tk.GROOVE,
            bg="white", width=38)
        self.eSILogDir.place(
            x=float(self.get('set manually', 'xpos')) + 15,
            y=float(self.get('set manually', 'ypos')) + 80)
        self.eSILogDir.insert(0, '')
        self.eSILogDir.configure(state='readonly')

        tk.Label(
            self.Canvas,
            text="Data block ID:"
            ).place(
                x=float(self.get('set manually', 'xpos')) + 10,
                y=float(self.get('set manually', 'ypos')) + 145)
        self.BlockID = tk.StringVar(master)
        self.BlockID.trace(
            "w", 
            lambda *args: self.update_metadata__datadir("BlockID", 
                                            self.BlockID, meta_data,
                                            config, *args))
        self.eBlockID = tk.Entry(
            self.Canvas, 
            textvariable=self.BlockID, 
            insertofftime=0, 
            relief=tk.GROOVE, 
            bg="white", width=19)
        self.eBlockID.place(
            x=float(self.get('set manually', 'xpos')) \
            + float(self.get('set manually', 'width')) / 2,
            y=float(self.get('set manually', 'ypos')) + 145)
        self.eBlockID.insert(0, str(0))
        if self.setGenSetManually.get():
            state_eBlockID = tk.NORMAL
        else:
            state_eBlockID = 'readonly'
        self.eBlockID.configure(state=state_eBlockID)

        tk.Label(
            self.Canvas,
            text="File basename:"
            ).place(
                x=float(self.get('set manually', 'xpos')) + 10,
                y=float(self.get('set manually', 'ypos')) + 100)
        self.eFileBaseName = tk.Entry(
            self.Canvas,
            insertofftime=0, 
            relief=tk.GROOVE, 
            bg="white", width=38)
        self.eFileBaseName.place(
            x=float(self.get('set manually', 'xpos')) + 15,
            y=float(self.get('set manually', 'ypos')) + 120)
        self.eFileBaseName.insert(0, self._get_file_basename())
        if self.setGenSetManually.get():
            state_eFileBaseName = tk.NORMAL
        else:
            state_eFileBaseName = 'readonly'
        self.eFileBaseName.configure(state=state_eFileBaseName)
        
        
    # =========================================================================
    # Cues
    # =========================================================================           
    def CuesPanel(self, master, config, stim, maze):
        
        def setFlashCues(stim):
            pass
            #if self.flashCues.get():
                #if rules.rules != [] :
                  #  print("Rules overwritten")
                   # rules.rules = []
                   # GUIrules.window.destroy()

            ##    stim.loadFlash(maze.data.get('settings', 'endless') == 'True',
            ##                   rules, self, GUIrules, maze)

        self.frames = []
        self.cuePic = [[] for i in range(stim.noCuesTotal)]
        self.CueTexturePhoto = [[] for i in range(stim.noCuesTotal)]
        
        tk.LabelFrame(
            self.Canvas, 
            text=self.get('FLASH CUES', 'name'), 
            font="Verdana 8 bold", fg='black', bd=6, 
            width=float(self.get('FLASH CUES', 'width')),
            height=float(self.get('FLASH CUES', 'height')), 
            labelanchor='n',
            relief=tk.RIDGE).place(
                x=float(self.get('FLASH CUES', 'xpos')),
                y=float(self.get('FLASH CUES', 'ypos')))

        # Select cue ID and load corresponding cue
        self.cue_dict = {
            'int': (float(self.get('FLASH CUES', 'width')) - 20) / 5,
            'width': ((float(self.get('FLASH CUES', 'width')) - 20) / 5) - 4,
            'height': (((float(self.get('FLASH CUES',
                                        'width')) - 20) / 5)- 4) * 1.2,
            'pic_y_pos': {},
            'pic_x_pos': {}}
        for i in range(stim.noCuesTotal):
            
            if i < 5:
                self.cue_dict['pic_x_pos'][i] = \
                    float(self.get('FLASH CUES', 'xpos')) \
                    + 10 + (i * self.cue_dict['int'])
                self.cue_dict['pic_y_pos'][i] = \
                    float(self.get('FLASH CUES', 'ypos')) + 35
            else:
                self.cue_dict['pic_x_pos'][i] = \
                    float(self.get('FLASH CUES', 'xpos')) \
                    + 10 + ((i - 5) * self.cue_dict['int'])
                self.cue_dict['pic_y_pos'][i] = \
                    float(self.get('FLASH CUES', 'ypos')) + 35 \
                    + self.cue_dict['height']

            self.frames.append(tk.LabelFrame(
                self.Canvas, 
                text=str(i),bd=2, 
                width=self.cue_dict['width'],
                height=self.cue_dict['height'], 
                labelanchor='n', relief=tk.RIDGE))
            self.frames[-1].place(
                    x=self.cue_dict['pic_x_pos'][i], 
                    y=self.cue_dict['pic_y_pos'][i] - 20)
            
            # search for existing textures:
            self.loadCue(i, self.frames[i])
 

        # Flash cues
        self.flashCues = tk.BooleanVar(self.Canvas)
        self.flashCues.set(False)
        tk.Checkbutton(
            self.Canvas, 
            text="Flash Cues", 
            command=lambda: setFlashCues(stim), 
            variable=self.flashCues).place(
                x=float(self.get('FLASH CUES', 'xpos')) + 140,#15,
                y=float(self.get('FLASH CUES', 'ypos'))+215)#186)
        
        
        # cues background
        self.cuesBackground = tk.BooleanVar(self.Canvas)
        self.cuesBackground.set(config.get('conf', 'cuesWall')=='True')
        tk.Checkbutton(
            self.Canvas, 
            text="Cues on Walls", 
            command=lambda: config.set_value('conf', 'cuesWall', 
                                             str(self.cuesBackground.get())),
            variable=self.cuesBackground).place(
                x=float(self.get('FLASH CUES', 'xpos')) + 260,#15,
                y=float(self.get('FLASH CUES', 'ypos'))+215)#186)        
        
        self.sequFileName = tk.Label(self.Canvas, text="Seq file:")
        self.sequFileName.place(
                x=float(self.get('FLASH CUES', 'xpos')) + 120,
                y=float(self.get('FLASH CUES', 'ypos'))+186)
        
        # load Sequence
        tk.Button(
            self.Canvas, text="Load Sequence", compound=tk.RIGHT,
            anchor="w", command=lambda: stim.openStimListWindow(self),
            justify="left").place(
            x=float(self.get('FLASH CUES', 'xpos')) + 260,
                y=float(self.get('FLASH CUES', 'ypos'))+186,
            width=100, 
            height=25)

        # load cue set
        tk.Button(
            self.Canvas, text="Load Cue Set", compound=tk.RIGHT,
            anchor="w", command=lambda: stim.loadCueSet(self),
            justify="left").place(
            x=float(self.get('FLASH CUES', 'xpos')) + 15,
                y=float(self.get('FLASH CUES', 'ypos'))+210,
            width=100, 
            height=25)
        
        # save cue set
        tk.Button(
            self.Canvas, text="Save Cue Set", compound=tk.RIGHT,
            anchor="w", command=lambda: stim.saveCueSet(),
            justify="left").place(
            x=float(self.get('FLASH CUES', 'xpos')) + 15,
                y=float(self.get('FLASH CUES', 'ypos'))+240,
            width=100, 
            height=25)

        self.LCueSet = tk.Label(self.Canvas, 
                                text="Cue Set: " + str(stim.cueSet))
        self.LCueSet.place(x=float(self.get('FLASH CUES', 'xpos')) +15,# 140,
                y=float(self.get('FLASH CUES', 'ypos'))+186)#215)
        
        # how long should the cues be flashed?
        tk.Label(self.Canvas, text="flash duration").place(
            x=float(self.get('FLASH CUES', 'xpos')) + 140,
            y=float(self.get('FLASH CUES', 'ypos'))+245)
        self.eCueTime = tk.Entry(self.Canvas, insertofftime=0, 
                            relief=tk.GROOVE, bg="white", width=5)
        self.eCueTime.place(x=float(self.get('FLASH CUES', 'xpos')) + 220,
            y=float(self.get('FLASH CUES', 'ypos'))+245)
        self.eCueTime.insert(0, "1")
        tk.Label(self.Canvas, text="sec").place(
                x=float(self.get('FLASH CUES', 'xpos')) + 250,
                y=float(self.get('FLASH CUES', 'ypos'))+245)
        

    # =========================================================================
    # MAZE INFORMATION
    # =========================================================================

    def MazeInfoPanel(self, maze):
        """
        created the info panel in the GUI
        """
        tk.LabelFrame(
            self.Canvas, text=self.get(' Maze Info ', 'name'), 
            font="Verdana 8 bold",
            fg='black', bd=6, width=float(self.get(' Maze Info ', 'width')),
            height=float(self.get(' Maze Info ', 'height')), labelanchor='n',
            relief=tk.RIDGE).place(
            x=float(self.get(' Maze Info ', 'xpos'))+self.x_lag,
            y=float(self.get(' Maze Info ', 'ypos')))

        self.LEndlessCorridor = tk.Label(self.Canvas, 
                                         text="Endless Corridor:  " + \
                                         maze.get('settings', 'endless'))
        self.LEndlessCorridor.place(x=float(self.get(' Maze Info ', 
                                                    'xpos')) + self.x_lag + 10,
                               y=float(self.get(' Maze Info ', 'ypos')) + 15)
        
        
        try:
            self.lLengthEndl = tk.Label(self.Canvas, 
                                        text="Length of Endless Corridor:  " +\
                                        maze.get('settings', 
                                                   'endless_length'))
            
            self.lLengthEndl.place(x=float(self.get(' Maze Info ','xpos')) + \
                                           self.x_lag + 10,
                                           y=float(self.get(' Maze Info ', 
                                                            'ypos')) + 35)
        except:
            self.lLengthEndl = tk.Label(self.Canvas, 
                                        text="Length of Endless Corridor: 0")
            
            self.lLengthEndl.place(x=float(self.get(' Maze Info ','xpos')) + \
                                           self.x_lag + 10,
                                           y=float(self.get(' Maze Info ', 
                                                            'ypos')) + 35)
        
        
            
       
                         
        try:                      
            self.lEndlFact = tk.Label(self.Canvas, 
                                      text="Endless Corridor Factor:  " + \
                                      maze.get('settings', 
                                                   'endless_factor'))
            self.lEndlFact.place(x=float(self.get(' Maze Info ','xpos')) + \
                                         self.x_lag + 10,
                                         y=float(self.get(' Maze Info ', 
                                                          'ypos')) + 55)
        except:
            self.lEndlFact = tk.Label(self.Canvas, 
                                      text="Endless Corridor Factor: 0")
            self.lEndlFact.place(x=float(self.get(' Maze Info ','xpos')) + \
                                         self.x_lag + 10,
                                         y=float(self.get(' Maze Info ', 
                                                          'ypos')) + 55)
        for i in maze.data:
            print(i)
        for i in maze.data['Sensors']:
            print(i)

        self.lNoOfSens = tk.Label(self.Canvas, text="Number of Sensors:  "
                                    + str(len(maze.data['Sensors'])))
        self.lNoOfSens.place(x=float(self.get(' Maze Info ','xpos')) + \
                                                          self.x_lag + 250,
                                               y=float(self.get(' Maze Info ',
                                                             'ypos')) + 15)
                                   
    # =========================================================================
    # TRIAL CONTROL PANEL
    # =========================================================================
    def randrepl(self):
        import random
        if Trials.speedfiles != []:
            if self.randReplay.get() == False:
                Trials.speedfiles = sorted(Trials.speedfiles)
            else:
                random.shuffle(Trials.speedfiles)
            self.tSpeedfile.delete('1.0', tk.END)
            for _path in Trials.speedfiles:
                self.tSpeedfile.insert(tk.END, os.path.basename(_path) + '\n')

    def add_comment(self, meta_data, trial_meta_data):
        """
        add the text in the comment textbox as a comment for the trial 
        and saves it in the datafile and mark the trial as commented in the 
        metadata file
        """
        import re
        comment_id = "_".join(
            ["Comment", time.strftime("%H:%M:%S"),"tr-%03d" % Trials.trial_no])
        SaveFilePath = self.eDataDir.get()
        FileName = '_'.join([self.eFileBaseName.get(), "mdata"])
        if not os.path.exists(SaveFilePath + FileName + ".csv"):
            meta_data.data_to_csv(
                self.saveFilesTo.get(),
                self.eDataDir.get(), 
                self.eFileBaseName.get())
        fd = open(SaveFilePath + FileName + ".csv", "a")
        metadata_file = csv.writer(
            fd, dialect='excel', quotechar='"', quoting=csv.QUOTE_ALL,
            lineterminator='\n', delimiter=';')
        metadata_file.writerow(
            [comment_id, re.sub('\s+', ' ', self.tComment.get("1.0", tk.END))]) 
        ###--->self.tComment and re.sub not defined
        fd.close()
        trial_meta_data.add(commented = "yes")
        #trial_meta_data["commented"] = ["yes"]
        self.tComment.delete("1.0", tk.END)

            
    def trialControlPanel(self, config, tracking_device, data, GUI_behavior, 
                          GUI_config, master, maze, rules, server, stim, TTL, 
                          trial, GUIrules, GUI_FT):
        """
        creates panel for trial control
        :param Data: object
        :param master: Tkinter object
        :param stim: object
        :param maze: object
        """

        # define panel label
        x_lag = self.x_lag
        tk.LabelFrame(
            self.Canvas, text=" Trial Control ",
            font="Verdana 8 bold", fg='black', bd=6,
            width=float(self.get(' Trial Control ', 'width')),
            height=float(self.get(' Trial Control ', 'height')), 
            labelanchor='n',
            relief=tk.RIDGE).place(
                x=float(self.get(' Trial Control ', 'xpos')) + x_lag,
                y=float(self.get(' Trial Control ', 'ypos')))

        self.LStartLED = tk.Label(
            self.Canvas,
            text="Trial not Running", 
            font="Verdana 12", 
            borderwidth=3, 
            relief="groove", 
            width=20)
        self.LStartLED.place(
            x = float(self.get(' Trial Control ', 'xpos')) \
                + float(self.get(' Trial Control ', 'width')) /2 - 100 + x_lag,
            y=float(self.get(' Trial Control ', 'ypos')) + 20)
        
        # added StringVar to be able to change the Button text later on
        self.startTrialsButton_text = tk.StringVar()
        self.startTrialsButton = tk.Button(
            self.Canvas, 
            textvariable=self.startTrialsButton_text,
            image=self.PlayPhoto, 
            compound="bottom",
            command=lambda: self.startTrialsButton_callback(
                trial, config, tracking_device, data, rules, GUIrules, 
                GUI_behavior, maze, server, TTL, stim, GUI_FT))
        self.startTrialsButton_text.set("Start block\nof trials")
        self.startTrialsButton.place(
                x=float(self.get(' Trial Control ', 'xpos')) + 20 + x_lag,
                y=float(self.get(' Trial Control ', 'ypos')) + 55, width=90,
                height=90)
        #
        
        tk.Button(
            self.Canvas, 
            text="New Trial", 
            image=self.NewTrialPhoto, 
            compound="bottom",
            command=lambda: trial.new_trial(
                config, tracking_device, data, rules, GUIrules, self, 
                GUI_behavior, maze, server, TTL, stim, GUI_FT)
            ).place(
                x=float(self.get(' Trial Control ', 'xpos')) \
                    + 120 + (float(self.get(' Trial Control ',
                                            'width')) - 30) / 2 + x_lag,
                y=float(self.get(' Trial Control ', 'ypos')) + 55, width=90,
                height=90)    

        # ### Autorun #########################################################
        tk.LabelFrame(
            self.Canvas, 
            text=self.get('Autorun', 'name'), 
            font="Verdana 8", fg='black', bd=2,
            width=float(self.get('Autorun', 'width')),
            height=float(self.get('Autorun', 'height')), labelanchor='n',
            relief=tk.RIDGE).place(
                x=float(self.get('Autorun', 'xpos')) + x_lag,
                y=float(self.get('Autorun', 'ypos')))

        self.autorun = tk.BooleanVar()
        self.autorun.set(False)
        tk.Checkbutton(
            master, text="Autorun with", variable=self.autorun).place(
                x=float(self.get('Autorun', 'xpos')) + 10 + x_lag,
                y=float(self.get('Autorun', 'ypos')) + 23)

        self.useConstantSpeed = tk.StringVar()
        self.useConstantSpeed.set("constant")
        tk.Radiobutton(
            self.Canvas, 
            text="constant", 
            variable=self.useConstantSpeed, 
            value='constant').place(
                x=float(self.get('Autorun', 'xpos')) + 120 + x_lag,
                y=float(self.get('Autorun', 'ypos')) + 15)

        self.eRunSpeed = tk.Entry(
            self.Canvas, 
            insertofftime=0, 
            relief=tk.GROOVE, 
            bg="white", width=5)
        self.eRunSpeed.place(
            x=float(self.get('Autorun', 'xpos')) + 200 + x_lag,
            y=float(self.get('Autorun', 'ypos')) + 18)
        self.eRunSpeed.insert(3, "1.0")
        tk.Label(
            self.Canvas, text="cm/s").place(
                x=float(self.get('Autorun', 'xpos')) + 250 + x_lag,
                y=float(self.get('Autorun', 'ypos')) + 15)

        tk.Radiobutton(
            self.Canvas, 
            text="variable", 
            variable=self.useConstantSpeed, 
            value='variable').place(
                x=float(self.get('Autorun', 'xpos')) + 120 + x_lag,
                y=float(self.get('Autorun', 'ypos')) + 38)

        tk.Button(
            self.Canvas, 
            text="Speed", 
            anchor="c", 
            command=lambda: self.openReplay(True, trial),
            # Exp.load_speed(window),
            justify="left").place(
                x=float(self.get('Autorun', 'xpos')) + 200 + x_lag,
                y=float(self.get('Autorun', 'ypos')) + 38, 
                width=50, height=25)

        tk.Label(
            self.Canvas, 
            text="Length of 1 square").place(
                x=float(self.get('Autorun', 'xpos')) + 15 + x_lag,
                y=float(self.get('Autorun', 'ypos')) + 70)
        self.eRunSpBlender = tk.Entry(
            self.Canvas, 
            insertofftime=0, 
            relief=tk.GROOVE, 
            bg="white", 
            width=5)
        self.eRunSpBlender.place(
            x=float(self.get('Autorun', 'xpos')) + 130 + x_lag,
            y=float(self.get('Autorun', 'ypos')) + 70)
        self.eRunSpBlender.insert(3, "10.0")
        tk.Label(self.Canvas, text="cm").place(
            x=float(self.get('Autorun', 'xpos')) + 180 + x_lag,
            y=float(self.get('Autorun', 'ypos')) + 70)

        tk.Checkbutton(
            self.Canvas, 
            text="random", 
            variable=self.randReplay,
            command=lambda: self.randrepl()).place(
                x=float(self.get('Autorun', 'xpos')) + 275 + x_lag,
                y=float(self.get('Autorun', 'ypos')) + 38)

        # ### info running trial frame ########################################
        tk.LabelFrame(
            self.Canvas, 
            text=self.get('info running trial', 'name'), 
            font="Verdana 8",
            fg='black', bd=2, 
            width=float(self.get('info running trial', 'width')),
            height=float(self.get('info running trial', 'height')), 
            labelanchor='n',
            relief=tk.RIDGE).place(
                x=float(self.get('info running trial', 'xpos')) + x_lag,
                y=float(self.get('info running trial', 'ypos')))

        self.LTrialNo = tk.Label(
            self.Canvas, 
            text="Trial Idx:\t " + str(Trials.trial_no),
            font="Verdana 8 bold")
        self.LTrialNo.place(
            x=float(self.get('info running trial', 'xpos')) + 15 + x_lag,
            y=float(self.get('info running trial', 'ypos')) + 18)

        self.timeDisplay = 0.0
        self.LTimeDisplay = tk.Label(
            self.Canvas, 
            text="Time:\t 0.0 sec",
            font="Verdana 8 bold")
        self.LTimeDisplay.place(
            x=float(self.get('info running trial', 'xpos')) + 15 + x_lag,
            y=float(self.get('info running trial', 'ypos')) + 38)

        self.LSpeed = tk.Label(
            self.Canvas, 
            text="Speed:\t" + str(round(var.speed, 1)) + " cm/s", 
            font="Verdana 8 bold")
        self.LSpeed.place(
            x=float(self.get('info running trial', 'xpos')) + 15 + x_lag,
            y=float(self.get('info running trial', 'ypos')) + 58)

        self.LStepNo = tk.Label(
            self.Canvas, 
            text="Steps:\t " + "0", 
            font="Verdana 8 bold")
        self.LStepNo.place(
            x=float(self.get('info running trial', 'xpos')) + 15 + x_lag,
            y=float(self.get('info running trial', 'ypos')) + 78)

        # ### start tracking subframe #########################################
        tk.LabelFrame(
            self.Canvas, 
            text=self.get('start tracking', 'name'), 
            font="Verdana 8", fg='black',
            bd=2, 
            width=float(self.get('start tracking', 'width')),
            height=float(self.get('start tracking', 'height')), 
            labelanchor='n',
            relief=tk.RIDGE).place(
                x=float(self.get('start tracking', 'xpos')) + x_lag,
                y=float(self.get('start tracking', 'ypos')))


        # ### add position sub-subframe #######################################
        
        tk.Label(self.Canvas, text="Track position in the maze").place(
            x=float(self.get('start tracking', 'xpos')) + 5 + x_lag,
            y=float(self.get('start tracking', 'ypos')) + 20)
        
        tk.Label(self.Canvas, text="when using ball as input device").place(
            x=float(self.get('start tracking', 'xpos')) + 5 + x_lag,
            y=float(self.get('start tracking', 'ypos')) + 40)
        
        self.saveTimedTicks = tk.BooleanVar()
        self.saveTimedTicks.set(True)
        self.trackMode = tk.Checkbutton(
            self.Canvas, 
            text="every", 
            variable=self.saveTimedTicks)
        self.trackMode.place(
            x=float(self.get('start tracking', 'xpos')) + 5 + x_lag,
            y=float(self.get('start tracking', 'ypos')) + 70)

        self.eTrackTick = tk.Entry(
            self.Canvas, 
            insertofftime=0, 
            relief=tk.GROOVE, 
            bg="white", 
            width=5)
        self.eTrackTick.place(
            x=float(self.get('start tracking', 'xpos')) + 70 + x_lag,
            y=float(self.get('start tracking', 'ypos')) + 75)
        self.eTrackTick.insert(1, "1.0")
        tk.Label(self.Canvas, text="sec").place(
            x=float(self.get('start tracking', 'xpos')) + 95 + x_lag,
            y=float(self.get('start tracking', 'ypos')) + 75)
        
        self.path = tk.PhotoImage(file="icons/path.gif")
        tk.Label(self.Canvas, image=self.path).place(
            x=float(self.get('start tracking', 'xpos')) + 130 + x_lag,
            y=float(self.get('start tracking', 'ypos')) + 65)
        

        # ### start cameras subframe ##########################################
        tk.LabelFrame(
            self.Canvas, 
            text=self.get('start cameras', 'name'), 
            font="Verdana 8", 
            fg='black',
            bd=2, 
            width=float(self.get('start cameras', 'width')),
            height=float(self.get('start cameras', 'height')), 
            labelanchor='n',
            relief=tk.RIDGE).place(
                x=float(self.get('start cameras', 'xpos')) + x_lag,
                y=float(self.get('start cameras', 'ypos')))
        
        self.trigger = []
        for _n in range(4):
            self.trigger.append(tk.StringVar())
            self.trigger[-1].set('never')
        
        triggerList = ("never", "start of experiment", "start of trial", 
                       "end of trial")
        tk.Label(
            self.Canvas,
            text="trigger A"
            ).place(
                x=float(self.get('start cameras', 'xpos')) + 5 + x_lag,
                y=float(self.get('start cameras', 'ypos')) + 15)

        tk.OptionMenu(
            self.Canvas, 
            self.trigger[0], 
            *triggerList
            ).place(
                x=float(self.get('start cameras', 'xpos')) + 65 + x_lag,
                y=float(self.get('start cameras', 'ypos')) + 15,
                width=float(self.get(' General Settings ', 'width')) / 3 \
                - float(self.get('Main Window', 'h_dist_inframe'))+10,
                height=23)
        
        
        tk.Label(
            self.Canvas,
            text="trigger B"
            ).place(
                x=float(self.get('start cameras', 'xpos')) + 5 + x_lag,
                y=float(self.get('start cameras', 'ypos')) + 35)

        tk.OptionMenu(
            self.Canvas, 
            self.trigger[1], 
            *triggerList
            ).place(
                x=float(self.get('start cameras', 'xpos')) + 65 + x_lag,
                y=float(self.get('start cameras', 'ypos')) + 35,
                width=float(self.get(' General Settings ', 'width')) / 3 \
                - float(self.get('Main Window', 'h_dist_inframe'))+10,
                height=23)     
        
        
        tk.Label(
            self.Canvas,
            text="trigger C"
            ).place(
                x=float(self.get('start cameras', 'xpos')) + 5 + x_lag,
                y=float(self.get('start cameras', 'ypos')) + 55)

        tk.OptionMenu(
            self.Canvas, 
            self.trigger[2], 
            *triggerList
            ).place(
                x=float(self.get('start cameras', 'xpos')) + 65 + x_lag,
                y=float(self.get('start cameras', 'ypos')) + 55,
                width=float(self.get(' General Settings ', 'width')) / 3 \
                - float(self.get('Main Window', 'h_dist_inframe'))+10,
                height=23)        
        
        
        tk.Label(
            self.Canvas,
            text="trigger D"
            ).place(
                x=float(self.get('start cameras', 'xpos')) + 5 + x_lag,
                y=float(self.get('start cameras', 'ypos')) + 75)

        tk.OptionMenu(
            self.Canvas, 
            self.trigger[3], 
            *triggerList
            ).place(
                x=float(self.get('start cameras', 'xpos')) + 65 + x_lag,
                y=float(self.get('start cameras', 'ypos')) + 75,
                width=float(self.get(' General Settings ', 'width')) / 3 \
                - float(self.get('Main Window', 'h_dist_inframe'))+10,
                height=23)   
        
    
        # ### start recording subframe ########################################
        tk.LabelFrame(
            self.Canvas, 
            text=self.get('start recording', 'name'), 
            font="Verdana 8", 
            fg='black',
            bd=2, 
            width=float(self.get('start recording', 'width')),
            height=float(self.get('start recording', 'height')), 
            labelanchor='n',
            relief=tk.RIDGE).place(
                x=float(self.get('start recording', 'xpos')) + x_lag,
                y=float(self.get('start recording', 'ypos')))
        self.useStartTrigger = tk.StringVar()
        self.useStartTrigger.set('Auto')
        tk.Radiobutton(
            self.Canvas, 
            text="directly", 
            variable=self.useStartTrigger, 
            value='Auto').place(
                x=float(self.get('start recording', 'xpos')) + 10 + x_lag,
                y=float(self.get('start recording', 'ypos')) + 15)

        tk.Radiobutton(
            self.Canvas, 
            text="@ trigger", 
            variable=self.useStartTrigger, 
            value='Trigger').place(
                x=float(self.get('start recording', 'xpos')) + 95 + x_lag,
                y=float(self.get('start recording', 'ypos')) + 15)

        tk.Label(
            self.Canvas, 
            text="trigger speed:").place(
                x=float(self.get('start recording', 'xpos')) + 15 + x_lag,
                y=float(self.get('start recording', 'ypos')) + 40)
        self.eRunTrigger = tk.Entry(
            self.Canvas, 
            insertofftime=0, 
            relief=tk.GROOVE, 
            bg="white", 
            width=5)
        self.eRunTrigger.place(
            x=float(self.get('start recording', 'xpos')) + 100 + x_lag,
            y=float(self.get('start recording', 'ypos')) + 40)
        self.eRunTrigger.insert(3, "1.0")
        tk.Label(
            self.Canvas, 
            text="cm/s").place(
                x=float(self.get('start recording', 'xpos')) + 130 + x_lag,
                y=float(self.get('start recording', 'ypos')) + 40)

        if self.useStartTrigger == "Auto":
            self.eRunTrigger.configure(state=tk.DISABLED)

        # ### supply reward subframe ##########################################
        tk.LabelFrame(
            self.Canvas, 
            text=self.get('supply reward', 'name'), 
            font="Verdana 8", 
            fg='black',
            bd=2, 
            width=float(self.get('supply reward', 'width')),
            height=float(self.get('supply reward', 'height')), 
            labelanchor='n',
            relief=tk.RIDGE).place(
                x=float(self.get('supply reward', 'xpos')) + x_lag,
                y=float(self.get('supply reward', 'ypos')))
        tk.Checkbutton(
            master, 
            text="enabled", 
            variable=self.autoReward).place(
                x=float(self.get('supply reward', 'xpos')) + 10 + x_lag,
                y=float(self.get('supply reward', 'ypos')) + 15)

        tk.Label(
            self.Canvas, 
            text="dur:").place(
                x=float(self.get('supply reward', 'xpos')) + 10 + x_lag,
                y=float(self.get('supply reward', 'ypos')) + 40)
        self.eValveOpen = tk.Entry(
            self.Canvas, 
            insertofftime=0, 
            relief=tk.GROOVE, 
            bg="white", 
            width=5)
        self.eValveOpen.place(
            x=float(self.get('supply reward', 'xpos')) + 40 + x_lag,
            y=float(self.get('supply reward', 'ypos')) + 40)
        self.eValveOpen.insert(0, "0.1")
        tk.Label(
            self.Canvas, 
            text="sec").place(
                x=float(self.get('supply reward', 'xpos')) + 70 + x_lag,
                y=float(self.get('supply reward', 'ypos')) + 40)

        tk.Label(
            self.Canvas, 
            text="at").place(
                x=float(self.get('supply reward', 'xpos')) + 10 + x_lag,
                y=float(self.get('supply reward', 'ypos')) + 65)
        self.eRewProba = tk.Entry(
            self.Canvas, 
            insertofftime=0, 
            relief=tk.GROOVE, 
            bg="white", 
            width=5)
        self.eRewProba.place(
            x=float(self.get('supply reward', 'xpos')) + 40 + x_lag,
            y=float(self.get('supply reward', 'ypos')) + 65)
        self.eRewProba.insert(0, "100")
        tk.Label(
            self.Canvas, 
            text="% probability").place(
                x=float(self.get('supply reward', 'xpos')) + 70 + x_lag,
                y=float(self.get('supply reward', 'ypos')) + 65)

        self.flushButton = tk.Button(
            self.Canvas, 
            text="flush\nmanually", 
            compound="bottom", 
            command=lambda: stim.flushSpouts(self),
            bg=None)
        
        self.flushButton.place(
                x=float(self.get('supply reward', 'xpos')) + 108 + x_lag,
                y=float(self.get('supply reward', 'ypos')) + 20,
                width=70, height=40)

        
        ########################SAVE A COMMENT SUBFRAME########################

        tk.LabelFrame(
            self.Canvas, 
            text=self.get('SAVE A COMMENT', 'name'), 
            font="Verdana 8", 
            fg='black', bd=2, 
            width=float(self.get('SAVE A COMMENT', 'width')),
            height=float(self.get('SAVE A COMMENT', 'height')),labelanchor='n',
            relief=tk.RIDGE).place(
                x=float(self.get('SAVE A COMMENT', 'xpos')) + x_lag,
                y=float(self.get('SAVE A COMMENT', 'ypos')))

        self.tComment = tk.Text(
            self.Canvas, 
            insertofftime=0, 
            relief=tk.SUNKEN, 
            bg="white", wrap=tk.WORD)
        self.tComment.place(
            x=float(self.get('SAVE A COMMENT', 'xpos')) + 15 + x_lag,
            y=float(self.get('SAVE A COMMENT', 'ypos')) + 20,
            width=float(self.get('SAVE A COMMENT', 'width')) - 30, 
            height=45)

        Bcomment = tk.Button(
            self.Canvas, 
            text="ADD COMMENT", 
            font="Verdana 8 bold", 
            anchor=tk.CENTER,
            command=lambda: self.add_comment(data[2], data[1]))
        Bcomment.place(
                x=float(self.get('SAVE A COMMENT', 'xpos')) + 15 + x_lag,
                y=float(self.get('SAVE A COMMENT', 'ypos')) + 70,
                width=float(self.get('SAVE A COMMENT', 'width')) - 30, 
                height=30)
        

        # ### block and trial settings subframe ###############################
        tk.LabelFrame(
            self.Canvas, 
            text=self.get('block and trial settings', 'name'), 
            font="Verdana 8",
            fg='black', bd=2, 
            width=float(self.get('block and trial settings','width')), 
            height=float(self.get('block and trial settings','height')), 
            labelanchor='n',
            relief=tk.RIDGE).place(
                x=float(self.get('block and trial settings', 'xpos')) + x_lag,
                y=float(self.get('block and trial settings', 'ypos')))

        tk.Label(
            self.Canvas, 
            text="max no. of trial / block:").place(
                x=float(self.get('block and trial settings', 'xpos')) + 10 \
                + x_lag,
                y=float(self.get('block and trial settings', 'ypos')) + 25)
        self.eNoTrials = tk.Entry(
            self.Canvas, 
            insertofftime=0, 
            relief=tk.GROOVE, 
            bg="white", 
            width=5)
        self.eNoTrials.place(
            x=float(self.get('block and trial settings', 'xpos')) + 140 + \
            x_lag,
            y=float(self.get('block and trial settings', 'ypos')) + 25)
        self.eNoTrials.insert(1, "0")

        tk.Label(
            self.Canvas, 
            text="min inter-trial-interval:").place(
                x=float(self.get('block and trial settings', 'xpos')) + 10 + \
                x_lag,
                y=float(self.get('block and trial settings', 'ypos')) + 50)
        self.eDelayTrial = tk.Entry(
            self.Canvas, 
            insertofftime=0, 
            relief=tk.GROOVE, 
            bg="white", 
            width=5)
        self.eDelayTrial.place(
            x=float(self.get('block and trial settings', 'xpos')) + 140 + \
            x_lag,
            y=float(self.get('block and trial settings', 'ypos')) + 50)
        self.eDelayTrial.insert(1, "1")
        tk.Label(
            self.Canvas, 
            text="sec").place(
                x=float(self.get('block and trial settings', 'xpos')) + 175 + \
                x_lag,
                y=float(self.get('block and trial settings', 'ypos')) + 50)

        tk.Label(
            self.Canvas, 
            text="max trial duration:").place(
                x=float(self.get('block and trial settings', 'xpos')) \
                    +float(self.get('block and trial settings', 'width')) / 2 \
                    + 10 + x_lag,
                y=float(self.get('block and trial settings', 'ypos')) + 25)
        self.eLengthTrial = tk.Entry(
            self.Canvas, 
            insertofftime=0, 
            relief=tk.GROOVE, 
            bg="white", 
            width=5)
        self.eLengthTrial.place(
            x=float(self.get('block and trial settings', 'xpos')) \
                + float(self.get('block and trial settings', 'width')) / 2 + \
                115 + x_lag,
            y=float(self.get('block and trial settings', 'ypos')) + 25)
        self.eLengthTrial.insert(1, "0")
        tk.Label(
            self.Canvas, 
            text="sec").place(
            x=float(self.get('block and trial settings', 'xpos')) \
                + float(self.get('block and trial settings', 'width')) / 2 + \
                150 + x_lag,
            y=float(self.get('block and trial settings', 'ypos')) + 25)

        tk.Label(
            self.Canvas, 
            text="max trial distance:").place(
                x=float(self.get('block and trial settings', 'xpos')) \
                    + float(self.get('block and trial settings', 
                                     'width')) / 2 + 10 + x_lag,
                y=float(self.get('block and trial settings', 'ypos')) + 50)
        self.eLengthTrialDist = tk.Entry(
            self.Canvas, 
            insertofftime=0, 
            relief=tk.GROOVE, 
            bg="white", 
            width=5)
        self.eLengthTrialDist.place(
            x=float(self.get('block and trial settings', 'xpos')) \
                + float(self.get('block and trial settings', 
                                 'width')) / 2 + 115 + x_lag,
            y=float(self.get('block and trial settings', 'ypos')) + 50)
        self.eLengthTrialDist.insert(1, "0")
        tk.Label(
            self.Canvas, 
            text="steps").place(
                x=float(self.get('block and trial settings', 'xpos')) \
                    + float(self.get('block and trial settings', 
                                     'width')) / 2 + 150 + x_lag,
                y=float(self.get('block and trial settings', 'ypos')) + 50)

        # ### T-maze settings subframe ########################################
        tk.LabelFrame(
            self.Canvas, 
            text=self.get('T-maze control', 'name'), 
            font="Verdana 8", fg='black', bd=2, 
            width=float(self.get('T-maze control', 'width')),
            height=float(self.get('T-maze control', 'height')),labelanchor='n',
            relief=tk.RIDGE).place(
                x=float(self.get('T-maze control', 'xpos')) + x_lag,
                y=float(self.get('T-maze control', 'ypos')))

        self.biasCorr = tk.BooleanVar()
        self.biasCorr.set(True)
        tk.Checkbutton(
            master, 
            text="Bias Correction", 
            variable=self.biasCorr).place(
                x=float(self.get('T-maze control', 'xpos')) + 10 + x_lag,
                y=float(self.get('T-maze control', 'ypos')) + 25)

        tk.Label(
            self.Canvas, 
            text="End after:").place(
                x=float(self.get('T-maze control', 'xpos')) + 10 + x_lag,
                y=float(self.get('T-maze control', 'ypos')) + 50)
        self.eTMazeEndTime = tk.Entry(
            self.Canvas, 
            insertofftime=0, 
            relief=tk.GROOVE, 
            bg="white", 
            width=5)
        self.eTMazeEndTime.place(
            x=float(self.get('T-maze control', 'xpos')) + 90 + x_lag,
            y=float(self.get('T-maze control', 'ypos')) + 50)
        self.eTMazeEndTime.insert(1, "1")
        tk.Label(
            self.Canvas, 
            text="sec").place(
                x=float(self.get('T-maze control', 'xpos')) + 125 + x_lag,
                y=float(self.get('T-maze control', 'ypos')) + 50)

        # ### Air-puff subframe ###############################################
        tk.LabelFrame(
            self.Canvas, 
            text=self.get('Air-Puff', 'name'), 
            font="Verdana 8", fg='black', bd=2,
            width=float(self.get('Air-Puff', 'width')),
            height=float(self.get('Air-Puff', 'height')), 
            labelanchor='n',
            relief=tk.RIDGE).place(
                x=float(self.get('Air-Puff', 'xpos')) + x_lag,
                y=float(self.get('Air-Puff', 'ypos')))

        tk.Label(
            self.Canvas, 
            text="Duration:").place(
                x=float(self.get('Air-Puff', 'xpos')) + 10 + x_lag,
                y=float(self.get('Air-Puff', 'ypos')) + 50)
        self.ePuffDuration = tk.Entry(
            self.Canvas, 
            insertofftime=0, 
            relief=tk.GROOVE, 
            bg="white", 
            width=5)
        self.ePuffDuration.place(
            x=float(self.get('Air-Puff', 'xpos')) + 90 + x_lag,
            y=float(self.get('Air-Puff', 'ypos')) + 50)
        self.ePuffDuration.insert(1, "0.01")
        tk.Label(
            self.Canvas, 
            text="sec").place(
                x=float(self.get('Air-Puff', 'xpos')) + 125 + x_lag,
                y=float(self.get('Air-Puff', 'ypos')) + 50)

        tk.Button(
            self.Canvas, 
            text="Give Air Puff", 
            compound="bottom",
            command=lambda: stim.apply_air_puff(self,data), #mdebug command=lambda: stim.apply_air_puff(self),
            bg=None).place(
                x=float(self.get('Air-Puff', 'xpos')) + 45 + x_lag,
                y=float(self.get('Air-Puff', 'ypos')) + 15, 
                width=80, height=30)
    #

    # Added this callback function to mediate the pausing and block init.
    def startTrialsButton_callback(self, trial, config, tracking_device, data,
                                   rules, GUIrules, GUI_behavior, maze, server,
                                   TTL, stim, GUI_FT):
        # current_text = self.startTrialsButton['text']
        # if "Pause" in current_text:
        #     self.startTrialsButton_text.set("Pausing")
        #     # self.startTrialsButton_text.set("Resume")
        # elif "Pausing" in current_text:
        #     pass
        # elif 'Resume' in current_text:
        #     self.startTrialsButton_text.set("Pause")
        # elif 'Start block' in current_text:
        #     # On first call delete the start button
        #     self.startTrialsButton_text.set("Pause")

        #     trial.new_trial(
        #         config, tracking_device, data, rules, GUIrules, self,
        #         GUI_behavior, maze, server, TTL, stim, GUI_FT, save=True)
        #     #
        # #
        
        trial.new_trial(
            config, tracking_device, data, rules, GUIrules, self,
            GUI_behavior, maze, server, TTL, stim, GUI_FT, save=True)
    #

    # =========================================================================
    # replay window (list)
    # =========================================================================
    def openReplay(self, load_speed, trial):
        if load_speed == True:
            def openwindow():
                self.windowReplay = tk.Tk()
                self.windowReplay.title("Replay Files")
                self.tSpeedfile = tk.Text(
                    self.windowReplay, 
                    insertofftime=0, 
                    relief=tk.SUNKEN,
                    bg="white", 
                    wrap=tk.WORD)
                self.tSpeedfile.grid(row=0, column=0)
                self.tSpeedfile.config(state=tk.DISABLED)
                
                speedFiles = trial.loadSpeed_files(self.randReplay.get()) 
                
                if speedFiles != '':
                    self.tSpeedfile.config(state=tk.NORMAL)
                    for _path in speedFiles:
                        self.tSpeedfile.insert(
                                tk.END,os.path.basename(_path)+'\n')

            if hasattr(self, 'masterReplay'):
                if not self.isOpen(self.windowReplay):
                    openwindow()
            else:
                openwindow()

    # =========================================================================
    # other stuff
    # =========================================================================

    def quitMM(self, data):
        if mbox.askokcancel("Quit", "Do you want to quit?"):
            print("Quittttt")
            print(self.saveFilesTo.get())
            print(self.eDataDir.get())
            print(self.eFileBaseName.get())
            print(self.timeDisplay)
            print(Timing.get_time())
            data[0].save_data(data, self.saveFilesTo.get(), 
                self.eDataDir.get(), self.eFileBaseName.get(), 
                self.timeDisplay, Timing.get_time(), self)
            self.Exit = True

    def updateSessionTime(self):
        self.LSessionTime.config(
            text="Session Time: " \
            + str(datetime.timedelta(
                    seconds=round(Timing.times['session_time']))))

    def isOpen(self, windowclass):
        try:
            if 'normal' == windowclass.window.state():
                return True
            else:
                return False
        except:
            return False
            
    def on_click_load(self, event=None):
        """Event will trigger when left mouse button is clicked on a 
        cue field. It will call the loadCue function"""
        no = int(event.widget._nametowidget(
                event.widget.winfo_parent()).cget("text"))
        self.loadCue(no, self.frames[no], loadFile=True)
        
    def on_click_delete(self, event=None):
        """Event will trigger when right mouse button is clicked on a 
        cue field. It will call the loadCue function"""
        no = int(event.widget._nametowidget(
                event.widget.winfo_parent()).cget("text"))
        self.deleteCue(no, self.frames[no])        
        
    def onEnter(self, event=None):
        event.widget._nametowidget(
                event.widget.winfo_parent()).config(bg='#399040')
        
    def onLeave(self, event=None):
        event.widget._nametowidget(
                event.widget.winfo_parent()).config(bg=self.bg)
        
    def loadCue(self, cueNo, frame, loadFile=False):
        if loadFile:
            cue_tex = tk.filedialog.askopenfilename()
            if cue_tex != '':
                
                #resize and save picture
                try:
                    img = Image.open(cue_tex)
                   
                    
                    img = img.resize((512,512), Image.ANTIALIAS)
                    if not os.path.isdir(var.cuePath):
                        os.makedirs(var.cuePath)
                    img.save(var.cuePath + "cue_" + str(cueNo) + ".png") 
                except:
                    mbox.showerror("Error","Image could not be loaded")

        
        if os.path.isfile(var.cuePath + "cue_" + str(cueNo) + ".png"):
            loadedCueFile = var.cuePath + "cue_" + str(cueNo) + ".png"
        else:
            loadedCueFile = 'Data/wall_textures/_emptyCue.png'
            
        with open(loadedCueFile, 'rb') as image_file:
            with Image.open(image_file) as image:
                image.thumbnail((self.cue_dict['width']-10,
                                self.cue_dict['height']-10),
                                Image.ANTIALIAS)
                self.CueTexturePhoto[cueNo] = ImageTk.PhotoImage(image)
                self.cuePic[cueNo] = tk.Label(
                        frame, image=self.CueTexturePhoto[cueNo])
                self.cuePic[cueNo].place(x=0,y=0)
                self.cuePic[cueNo].bind('<Button-1>', self.on_click_load)
                self.cuePic[cueNo].bind('<Button-3>', self.on_click_delete)
                self.cuePic[cueNo].bind('<Enter>', self.onEnter)
                self.cuePic[cueNo].bind('<Leave>', self.onLeave)
         

    def deleteCue(self, cueNo, frame):    
        """Deletes the cue file with the number of cueNo and overwrites the 
        image with the default image"""
        
        #Check if user wants to delte the cue via a message box
        if mbox.askokcancel("Delete", "Do you want to delete this cue?"):      
            if os.path.isfile(var.cuePath + "cue_" + str(cueNo) + ".png"): 
                os.remove(var.cuePath + "cue_" + str(cueNo) + ".png")
            if os.path.isfile(var.cuePath + "cue_" + str(cueNo) + "_mirr.png"): 
                os.remove(var.cuePath + "cue_" + str(cueNo) + "_mirr.png")    
            
            loadedCueFile = 'Data/wall_textures/_emptyCue.png'
                
            with open(loadedCueFile, 'rb') as image_file:
                with Image.open(image_file) as image:
                    image.thumbnail((self.cue_dict['width']-10,
                                    self.cue_dict['height']-10),
                                    Image.ANTIALIAS)
                    self.CueTexturePhoto[cueNo] = ImageTk.PhotoImage(image)
                    self.cuePic[cueNo] = tk.Label(
                            frame, image=self.CueTexturePhoto[cueNo])
                    self.cuePic[cueNo].place(x=0,y=0)
                    self.cuePic[cueNo].bind('<Button-1>', self.on_click_load)
                    self.cuePic[cueNo].bind('<Button-3>', self.on_click_delete)
                    self.cuePic[cueNo].bind('<Enter>', self.onEnter)
                    self.cuePic[cueNo].bind('<Leave>', self.onLeave)
            
  
    def setCue(self, cueNo, image):
        """Load a cue with the stimulus class function
        and store in as a picture"""
        x_lag = self.x_lag
        self.CueTexturePhoto[cueNo] = ImageTk.PhotoImage(image)
        self.cuePic[cueNo] = tk.Label(
                self.Canvas, image=self.CueTexturePhoto[cueNo])
        self.cuePic[cueNo].place(
            x=self.cue_dict['pic_x_pos'][cueNo]+(
                    self.cue_dict['width']-38)/2 +x_lag,
            y=self.cue_dict['pic_y_pos'][cueNo])        
        
    def _get_data_dir(self, config):
        """
        Returns an automatically generated data directory.
        """
        data_dir_list = []
        if self.saveFilesTo.get() == 'Network':            
            data_dir_list += [config.get('Files', 'SavePathNetwork') , 
                              "Data"]
        elif self.saveFilesTo.get() == 'LocalComp':
            data_dir_list += [config.get('Files', 'SavePathLocal'), 
                              "Data"]
        else:
            return ""

        if self.expType.get() != "undefined":
            data_dir_list += [self.expType.get()]

        if self.taskType.get() != "undefined":
            data_dir_list += [self.taskType.get()]

        if self.eMouseID.get() != "":
            data_dir_list += [self.eMouseID.get()]

        data_dir_list += [datetime.date.today().isoformat()]

        return "\\".join(data_dir_list + [""])
   
    def _update_entry(self, entry, new_entry=None): 
        reset = False
        if entry['state'] in ['readonly', tk.DISABLED]:
            reset = True
            entry.configure(state=tk.NORMAL)
        if new_entry:
            entry.delete(0, tk.END)
            entry.insert(0, new_entry)
        else:
            entry.delete(0, tk.END)
        if reset:
            entry.configure(state='readonly')
            
    def _update_optionmenu(self, new_list, sel_opt="undefined"):
        self.eTaskName['menu'].delete(0, 'end')
        for item_i in new_list:
            self.eTaskName['menu'].add_command(
                label=item_i,
                command=lambda new_item=item_i: self.taskType.set(new_item))
        self.taskType.set(sel_opt)
        
    def update_expType_settings(self, meta_data, settings_config, config, *args):
        """update of experiment type specific settings"""
        meta_data.update(ExperimentType=self.expType.get())
        self._update_optionmenu(self.get_task_list(settings_config))
        self.update_datadir(meta_data, config)  # update data dir
        self.update_basename(meta_data)  # update file basename


    def update_tasktype_settings(self, meta_data, settings_config, config, 
                                 *args):
        """update of metadata and filepath for saving data. Loading the
        settings, which are stored in the settings config file."""
        meta_data.update(TaskType=self.taskType.get())
        self.update_datadir(meta_data, config)  # update data dir
        self.update_basename(meta_data)  # update file basename
        
        self.loadSettings(settings_config)
 

    def updateSILogDir(self, meta_data, *args):
        if len(self.eSILogDir.get().strip()) > 0:
            meta_data.update(SILogDirectory=self.eSILogDir.get())
        else:
            meta_data.update(SILogDirectory=None)

    def update_metadata__datadir(self, replaceVar, newVar, meta_data, config,
                                 *args):
        """update metadata and datadir"""
        self.kw={replaceVar: newVar.get()}
        #meta_data.update(replaceVar=newVar)
        meta_data.update(**self.kw) #mdebug

        self.update_datadir(meta_data, config)

    def update_datadir(self, meta_data, config, *args):
        """update datadir"""
        if not self.setGenSetManually.get():
            print(self.eDataDir)
            print(self._get_data_dir(config))
            self._update_entry(self.eDataDir, self._get_data_dir(config))
        meta_data.update(DataDirectory=self._get_data_dir(config))

    def update_basename(self, meta_data, *args):
        """update basename"""
        if not self.setGenSetManually.get():
            self._update_entry(self.eFileBaseName, self._get_file_basename())
        meta_data.update(FileBaseName=self._get_file_basename())

    def _refresh_settings(self):
        if self.expType.get() == "VirtualTunnel":
            self.cUseDeviceM.deselect()
            self.cUseDeviceC.select()
            self.SetMouse1Button.configure(state=tk.DISABLED)
            self.SetMouse2Button.configure(state=tk.DISABLED)
            self.useStartTrigger.set("Auto")
            self.saveTimedTicks.set(False)
            self.eTrackTick.configure(state=tk.DISABLED)
            self.trackMode.configure(state=tk.DISABLED)
        elif self.expType.get() == "VirtualMaze":
            self.cUseDeviceM.select()
            self.cUseDeviceC.deselect()
            self.SetMouse1Button.configure(state=tk.NORMAL)
            self.SetMouse2Button.configure(state=tk.NORMAL)
            self.useStartTrigger.set("Auto")
            self.saveTimedTicks.set(True)
            self.autoReward.set(True)
            self.startCameradirectly.set(False)
            self.eTrackTick.configure(state=tk.NORMAL)
            self.trackMode.configure(state=tk.NORMAL)
        else:
            self.cUseDeviceM.deselect()
            self.cUseDeviceC.deselect()
            self.SetMouse1Button.configure(state=tk.DISABLED)
            self.SetMouse2Button.configure(state=tk.DISABLED)
            self.useStartTrigger.set("Auto")

    def _update_set_manually(self, state):
        self.eDataDir.configure(state=state)
        self.eSILogDir.configure(state=state)
        self.eBlockID.configure(state=state)
        self.eFileBaseName.configure(state=state)

    def loadConfig(self):
        self.flashCues.set(self.mmconfig.get('conf', 'flashCues'))
        self.RandomSequence.set(bool(self.mmconfig.get('conf', 
                                                       'RandomSequence')))

    def cueNo(self, stim, mousePos, server):
        """call set Cue function with selected cue and selected duration.
        The selcted cue is presented on the wall side 
        which was selected in the GUI"""
        if self.cueDirection.get() == 'right':                   
            _cueL = None
            _cueR = self.cueSelected.get()
        elif self.cueDirection.get() == 'left':
            _cueL = self.cueSelected.get()
            _cueR = None
        elif self.cueDirection.get() == 'both':
            _cueL = self.cueSelected.get()
            _cueR = self.cueSelected.get()
            
        stim.set_cue(
          mousePos, server, float(self.eCueTime.get()), 
          cueNoL=_cueL, cueNoR=_cueR)


    def boolToState(self, boolIn):
        if boolIn == False:
            return tk.DISABLED
        else:    
            return tk.NORMAL
        
