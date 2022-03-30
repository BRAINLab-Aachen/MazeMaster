# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 15:30:49 2019

@author: bexter
"""

import tkinter
import ast
from tkinter import ttk

class GUISettings():
    def __init__(self, config):
        self.mmconfig = config

    def openWindow(self):    
        self.window = tkinter.Tk()
        self.window.title("Settings")
        
        tabControl = ttk.Notebook(self.window)    # Create Tab Control
        
        tab_Blender = ttk.Frame(tabControl)    # Create a tab
        tab_SavePath = ttk.Frame(tabControl)    # Create a tab
        tab_DigitalTriggers = ttk.Frame(tabControl)    # Create a tab
        
   
        tabControl.add(tab_Blender, text='Blender Window')     # Add tab
        tabControl.add(tab_SavePath, text='Data Directories')     # Add tab
        tabControl.add(tab_DigitalTriggers, text='Digital Ports')     # Add tab

        tabControl.grid(row=0, column=0)  # Pack to make visible

        tkinter.Label(
            tab_Blender,
            text="Blender Window X Position:"
            ).grid(row=0, column=0, sticky=tkinter.W)
        
        self.eWindowBlenderPosX = tkinter.Entry(
            tab_Blender,
            insertofftime=0, 
            relief=tkinter.GROOVE, 
            bg="white", width=10)
        
        self.eWindowBlenderPosX.grid(row=1, column=0, 
                                    padx=(5, 0), pady=(5, 0))
        
        tkinter.Label(
            tab_Blender,
            text="Blender Window Y Position:"
            ).grid(row=0, column=1, sticky=tkinter.W)
        
        self.eWindowBlenderPosY = tkinter.Entry(
            tab_Blender,
            insertofftime=0, 
            relief=tkinter.GROOVE, 
            bg="white", width=10)
        
        self.eWindowBlenderPosY.grid(row=1, column=1, 
                                    padx=(5, 0), pady=(5, 0))
        
        tkinter.Label(
            tab_Blender,
            text="Blender Window Width:"
            ).grid(row=2, column=0, sticky=tkinter.W)
        
        self.eWindowBlenderW = tkinter.Entry(
            tab_Blender,
            insertofftime=0, 
            relief=tkinter.GROOVE, 
            bg="white", width=10)
        
        self.eWindowBlenderW.grid(row=3, column=0)
        
        tkinter.Label(
            tab_Blender,
            text="Blender Window Height:"
            ).grid(row=2, column=1, sticky=tkinter.W)
        
        self.eWindowBlenderH = tkinter.Entry(
            tab_Blender,
            insertofftime=0, 
            relief=tkinter.GROOVE, 
            bg="white", width=10)
        
        self.eWindowBlenderH.grid(row=3, column=1)        
        
        self.blenderFullscreen = tkinter.BooleanVar(tab_Blender)
        self.blenderFullscreen.set(False)
        cFullscreen = tkinter.Checkbutton(
            tab_Blender, 
            text="fullscreen", 
            variable=self.blenderFullscreen)
        cFullscreen.grid(row=4,column=0)
    
        self.monitorSetup = tkinter.StringVar(tab_Blender)
        self.monitorSetup.set("1 monitor")
        
        
        tkinter.Label(
            tab_Blender,
            text="Number of monitors in setup:"
            ).grid(row=5, column=0, sticky=tkinter.W)
        
        monitorSetupButton1 = tkinter.Radiobutton(
            tab_Blender, 
            text="1 monitor", 
            variable=self.monitorSetup, 
            value='1 monitor')
        monitorSetupButton1.grid(row=6,column=0)
        
        monitorSetupButton2 = tkinter.Radiobutton(
            tab_Blender, 
            text="2 monitors", 
            variable=self.monitorSetup, 
            value='2 monitors')
        monitorSetupButton2.grid(row=6,column=1)

        monitorSetupButtonMult = tkinter.Radiobutton(
            tab_Blender, 
            text="semicircle", 
            variable=self.monitorSetup, 
            value='semicircle')
        monitorSetupButtonMult.grid(row=6,column=2)
        
        
        #save paths    
        tkinter.Label(
            tab_SavePath,
            text="Save Data Path Network:"
            ).grid(row=6, column=0, sticky=tkinter.W)
        
        self.ePathNet = tkinter.Entry(
            tab_SavePath,
            insertofftime=0, 
            relief=tkinter.GROOVE, 
            bg="white", width=30)
        
        self.ePathNet.grid(row=6, column=1)   

        tkinter.Label(
            tab_SavePath,
            text="Save Data Path Local:"
            ).grid(row=7, column=0, sticky=tkinter.W)
        
        self.ePathLoc = tkinter.Entry(
            tab_SavePath,
            insertofftime=0, 
            relief=tkinter.GROOVE, 
            bg="white", width=30)
        
        self.ePathLoc.grid(row=7, column=1)      
        
        
        #digital trigger ports
        
        
        tkinter.Label(
            tab_DigitalTriggers,
            text="Task"
            ).grid(row=0, column=0, sticky=tkinter.W)
        tkinter.Label(
            tab_DigitalTriggers,
            text="Digital Line"
            ).grid(row=0, column=1, sticky=tkinter.W)
        
        #lick left
        tkinter.Label(
            tab_DigitalTriggers,
            text="lick left"
            ).grid(row=1, column=0, sticky=tkinter.W)
        
        self.eLickL = tkinter.Entry(
            tab_DigitalTriggers,
            insertofftime=0, 
            relief=tkinter.GROOVE, 
            bg="white", width=30)    
        self.eLickL.grid(row=1, column=1)   

        #lick right
        tkinter.Label(
            tab_DigitalTriggers,
            text="lick right"
            ).grid(row=2, column=0, sticky=tkinter.W)
        
        self.eLickR = tkinter.Entry(
            tab_DigitalTriggers,
            insertofftime=0, 
            relief=tkinter.GROOVE, 
            bg="white", width=30)
        self.eLickR.grid(row=2, column=1)   
   
        #trigger A
        tkinter.Label(
            tab_DigitalTriggers,
            text="trigger A"
            ).grid(row=3, column=0, sticky=tkinter.W)
        
        self.eTriggerA = tkinter.Entry(
            tab_DigitalTriggers,
            insertofftime=0, 
            relief=tkinter.GROOVE, 
            bg="white", width=30)
        self.eTriggerA.grid(row=3, column=1)      
        
        #trigger B
        tkinter.Label(
            tab_DigitalTriggers,
            text="trigger B"
            ).grid(row=4, column=0, sticky=tkinter.W)
        
        self.eTriggerB = tkinter.Entry(
            tab_DigitalTriggers,
            insertofftime=0, 
            relief=tkinter.GROOVE, 
            bg="white", width=30)
        self.eTriggerB.grid(row=4, column=1)  
        
        #trigger C
        tkinter.Label(
            tab_DigitalTriggers,
            text="trigger C"
            ).grid(row=5, column=0, sticky=tkinter.W)
        
        self.eTriggerC = tkinter.Entry(
            tab_DigitalTriggers,
            insertofftime=0, 
            relief=tkinter.GROOVE, 
            bg="white", width=30)
        self.eTriggerC.grid(row=5, column=1) 
        
        #trigger D
        tkinter.Label(
            tab_DigitalTriggers,
            text="trigger D"
            ).grid(row=6, column=0, sticky=tkinter.W)
        
        self.eTriggerD = tkinter.Entry(
            tab_DigitalTriggers,
            insertofftime=0, 
            relief=tkinter.GROOVE, 
            bg="white", width=30)
        self.eTriggerD.grid(row=6, column=1)          

        #reward right
        tkinter.Label(
            tab_DigitalTriggers,
            text="reward right"
            ).grid(row=7, column=0, sticky=tkinter.W)
        
        self.eRewR = tkinter.Entry(
            tab_DigitalTriggers,
            insertofftime=0, 
            relief=tkinter.GROOVE, 
            bg="white", width=30)
        self.eRewR.grid(row=7, column=1) 
        
        #reward left
        tkinter.Label(
            tab_DigitalTriggers,
            text="reward left"
            ).grid(row=8, column=0, sticky=tkinter.W)
        
        self.eRewL = tkinter.Entry(
            tab_DigitalTriggers,
            insertofftime=0, 
            relief=tkinter.GROOVE, 
            bg="white", width=30)
        self.eRewL.grid(row=8, column=1) 
        
        #air puff
        tkinter.Label(
            tab_DigitalTriggers,
            text="air-puff manual"
            ).grid(row=9, column=0, sticky=tkinter.W)
        
        self.eAirPuff = tkinter.Entry(
            tab_DigitalTriggers,
            insertofftime=0, 
            relief=tkinter.GROOVE, 
            bg="white", width=30)
        self.eAirPuff.grid(row=9, column=1)         
        
        
        #air puff left
        tkinter.Label(
            tab_DigitalTriggers,
            text="air-puff left"
            ).grid(row=10, column=0, sticky=tkinter.W)
        
        self.eAirPuffL = tkinter.Entry(
            tab_DigitalTriggers,
            insertofftime=0, 
            relief=tkinter.GROOVE, 
            bg="white", width=30)
        self.eAirPuffL.grid(row=10, column=1)  
        
        #air puff right
        tkinter.Label(
            tab_DigitalTriggers,
            text="air-puff right"
            ).grid(row=11, column=0, sticky=tkinter.W)
        
        self.eAirPuffR = tkinter.Entry(
            tab_DigitalTriggers,
            insertofftime=0, 
            relief=tkinter.GROOVE, 
            bg="white", width=30)
        self.eAirPuffR.grid(row=11, column=1)  
               

        #Save button
        SaveButton = tkinter.Button(
            self.window, 
            text = "Save", command = self.saveConfig, width = 15,)
        SaveButton.grid(row=14,column=2, padx=(0, 10), pady=(0,10))
                
        self.loadConfig()
        
    def saveConfig(self):
        pos = [self.eWindowBlenderW.get(), self.eWindowBlenderH.get(), 
                   self.eWindowBlenderPosX.get(), 
                   self.eWindowBlenderPosY.get(),
                   self.blenderFullscreen.get()]
    
        self.mmconfig.set_value('conf', 'blenderWin', str(pos))
        
        self.mmconfig.set_value('Files', 'SavePathNetwork', 
                                self.ePathNet.get())
        self.mmconfig.set_value('Files', 'SavePathLocal', self.ePathLoc.get())
        
        if pos[4]:
            screen = '-f'
        else:
            screen = '-w'

        batFile = open('startBlender.bat','w+')
        batFile.write('blenderplayer.exe %s %s %s %s %s 3DMazeEngine.blend' % (screen, pos[0],pos[1],pos[2],pos[3]))
        batFile.close()
        
        self.mmconfig.set_value('conf', 'monitors', self.monitorSetup.get())
        
        
        #triggers
        self.mmconfig.set_value('NIlines', 'lick l', self.eLickL.get())
        self.mmconfig.set_value('NIlines', 'lick r', self.eLickR.get())
        self.mmconfig.set_value('NIlines', 'trigger A', self.eTriggerA.get())
        self.mmconfig.set_value('NIlines', 'trigger B', self.eTriggerB.get())
        self.mmconfig.set_value('NIlines', 'trigger C', self.eTriggerC.get())
        self.mmconfig.set_value('NIlines', 'trigger D', self.eTriggerD.get())
        self.mmconfig.set_value('NIlines', 'reward r', self.eRewR.get())
        self.mmconfig.set_value('NIlines', 'reward l', self.eRewL.get())
        self.mmconfig.set_value('NIlines', 'air puff', self.eAirPuff.get())
        self.mmconfig.set_value('NIlines', 'air puff left', self.eAirPuffL.get())
        self.mmconfig.set_value('NIlines', 'air puff right', self.eAirPuffR.get())
        
    def loadConfig(self):
        pos = ast.literal_eval(self.mmconfig.get('conf', 'blenderWin'))
        self.eWindowBlenderW.insert(0, pos[0])
        self.eWindowBlenderH.insert(0, pos[1])
        self.eWindowBlenderPosX.insert(0, pos[2])
        self.eWindowBlenderPosY.insert(0, pos[3])
        self.blenderFullscreen.set(pos[4]=='True')
        self.monitorSetup.set(self.mmconfig.get('conf', 'monitors'))
        
        self.ePathNet.insert(0, self.mmconfig.get('Files', 'SavePathNetwork'))
        self.ePathLoc.insert(0, self.mmconfig.get('Files', 'SavePathLocal'))
        
        self.eLickL.insert(0, self.mmconfig.get('NIlines', 'lick l'))
        self.eLickR.insert(0, self.mmconfig.get('NIlines', 'lick r'))
        self.eTriggerA.insert(0, self.mmconfig.get('NIlines', 'trigger A'))
        self.eTriggerB.insert(0, self.mmconfig.get('NIlines', 'trigger B'))
        self.eTriggerC.insert(0, self.mmconfig.get('NIlines', 'trigger C'))
        self.eTriggerD.insert(0, self.mmconfig.get('NIlines', 'trigger D'))  
        self.eRewL.insert(0, self.mmconfig.get('NIlines', 'reward l'))
        self.eRewR.insert(0, self.mmconfig.get('NIlines', 'reward r'))       
        self.eAirPuff.insert(0, self.mmconfig.get('NIlines', 'air puff'))
        self.eAirPuffL.insert(0, self.mmconfig.get('NIlines', 'air puff left'))
        self.eAirPuffR.insert(0, self.mmconfig.get('NIlines', 'air puff right'))
        print(pos[4]=='True')
        

