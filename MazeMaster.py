#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Master for Virtual Reality Maze

@author: Alexander Bexter, Alexander.Bexter@rwth-aachen.de
@copyright: 2015, Alexander Bexter
"""

import sys
sys.path.append('.\modules')
sys.path.append('.\modules\GUI')

import asyncore
import time
import tkinter as tk
import Timing
import tkinter 
import var
from tkinter import messagebox as mbox
import logging

#imports for modules, when using the main as .exe file
import numpy as np
import csv
import os
import datetime
import configparser 
import socket        
import rawinputreader
import ast
from win32api import GetSystemMetrics
from PIL import Image, ImageTk, ImageOps
from tkinter import simpledialog
import shutil
from tkinter import messagebox
from tkinter import filedialog
import random
import tarfile
from tkinter import ttk
from scipy import misc
import ctypes.wintypes
#import psychopy.sound  # Not sure if I need this in here, need to test with .exe
#import _thread
import threading

try:
    import nidaqmx
    nidaqmx.Task()
    var.Lick = True
    var.NI = True
except:
    var.NI = False
    var.Lick = False
    print('No NI drivers or hardware detected')

import MM_server
import MM_tracking
from MM_behavior import Behavior
from MM_communication import Communication
from MM_config import Config
from MM_data_container import DataContainer
from MM_rules import Rules
from MM_stimulus import Stimulus
from MM_trial import Trials
from MM_digitalTrigger import TTL
from misc import calc_move

from GUI import GUI
from GUI_flash_tunnel import GUIFlashTunnel
from GUI_behavior import GUIBehavior
from GUI_maze_config import GUIMazeConfig
from GUI_maze import GUIMaze
from GUI_rules import GUIRules
from GUI_top_menu import GUITopMenu
from GUI_configure import Configure
from GUI_settings import GUISettings
from GUI_scripts import GUIScripts

print('Start Maze Master')
#initialize master for GUI
master = tk.Tk()
master.title("Maze Master")

# =============================================================================
# create basic class objects
# =============================================================================  

config = Config('config.ini')
behavior = Behavior((config.get('NIlines', 'lick r'), 
                    config.get('NIlines', 'lick l')))
TTL = TTL(config)
stim = Stimulus(config)
        
rules = Rules()
comm = Communication()
trial = Trials()
server = MM_server.Server('localhost', 10000)

data = [
    DataContainer('trialData'),
    DataContainer('trialMetadata'),
    DataContainer('blockMetadata')]

GUI = GUI(master)

#maze = Maze(GUI.get('maze_grid','xpos'), GUI.get('maze_grid','ypos'))

settings_config = Config('settings.ini')

#logging.basicConfig(level=logging.DEBUG)
# =============================================================================
# Starting the NI Tasks
# =============================================================================

#Create tracking device
if config.get('conf', 'useWheel') == 'True':
    print("MazeMaster Wheel") #mdebug
    tracking_device = MM_tracking.Counter(config.get('NIlines','counter'))
elif config.get('conf', 'useBall') == 'True':
    print("MAzeMAster Ball")  #mdebug
    tracking_device = MM_tracking.Ball()
#

try:
    circumference_in_cm = float(config.get('tracking_device', 'circumference_in_cm'))
    if circumference_in_cm < 0.:
        circumference_in_cm = 62.  # That is our default circumference
except:
    circumference_in_cm = 62.
    print('Overwriting tracking_device circumference with: '+str(circumference_in_cm))
    if 'tracking_device' not in config.winConfig.sections():
        config.winConfig.add_section('tracking_device')
    config.set_value('tracking_device', 'circumference_in_cm', str(circumference_in_cm))
#
tracking_device.circumference_in_cm = float(circumference_in_cm)

# Initialize the digital output
if var.NI:
    var.digital_output = True
else:
    var.digital_output = False


# =============================================================================
# Generate GUI Panels
# =============================================================================
GUI_Rules = GUIRules()
maze = GUIMaze(config, GUIRules)

GUI.ServerControlPanel(server, data, trial, config, stim, maze, rules, 
                       GUI_Rules)
GUI.general_settings_panel(data[2], master, settings_config, config)


GUI.CuesPanel(master, config, stim, maze)
GUI.MazeInfoPanel(maze)

# seperate windows (via Topmenu)
GUI_FT = GUIFlashTunnel(config)
GUI_Conf = Configure(config, GUI)
GUI_MazeConf = GUIMazeConfig(config)
GUI_Settings = GUISettings(config)
GUIScripts = GUIScripts(config)

#maze = GUIMaze(config, maze, GUIRules)
    
GUI_Behavior = GUIBehavior()

GUI_TopMenu = GUITopMenu(
    master, data, GUI, GUI_FT, GUI_Conf, GUI_Behavior, GUI_Rules, 
    GUI_MazeConf, GUI_Settings, GUIScripts, maze, rules)
GUI.MazePanel(config, var.MMversion, maze, data, GUI_Rules, 
              (master,maze.window))

GUI.trialControlPanel(
    config, tracking_device, data, GUI_Behavior, GUI_Conf, master, maze, rules, 
    server, stim, TTL, trial, GUI_Rules, GUI_FT)

# =============================================================================
# INITIALIZE MAZE
# =============================================================================

maze.initialization()


# start Lickdetector
#if var.Lick:
#    behavior.licktask.start() 

Timing.times['session_time_start'] = time.time()
GUI.Canvas.pack()
GUI.Canvas.update()

# Open the scripts at initialization
#GUI_FT.openWindow(maze)
#GUI_Behavior.openWindow()
GUIScripts.openWindow()
GUIScripts.window.lift()
GUI.Canvas.update()
GUIScripts.on_close()

# load last sequence
#stim.openStimListWindow(GUI=GUI, load_from_configs=True)

# Bring the windows back on top
maze.window.lift()
master.lift()

# =============================================================================
# THREAD
# =============================================================================

def airpuff_update_loop():
    #logging.debug("Airpuff loop starts (called in MazeMaster)")
    while True:
        stim.airpuff_update()

airpuffthread = threading.Thread(target=airpuff_update_loop)
start_airpuff_update = True




# =============================================================================
# MAINLOOP
# =============================================================================
while GUI.Exit is False and GUI.Canvas.winfo_exists():

    asyncore.loop(timeout=0.00000001, count=1)

    # update session time
    Timing.times['session_time'] = time.time() - \
        Timing.times['session_time_start']
    GUI.updateSessionTime()

    # update sensor_delay
    if Timing.times['sensor_delay'] > 0 and time.time() >= \
    Timing.times['sensor_delay']:
        Timing.times['sensor_delay'] = 0.0

    # update GUI settings
    if GUI.useStartTrigger.get() == "Auto":
        GUI.eRunTrigger.configure(state=tk.DISABLED)
    else:
        GUI.eRunTrigger.configure(state=tk.NORMAL)

    # reset to correct entry states of general settings
    if GUI.setGenSetManually.get():
        GUI._update_set_manually(tk.NORMAL)
    else:
        GUI._update_set_manually('readonly')

    # update trial time
    if Trials.trial_running:
        GUI.timeDisplay = time.time() - Timing.times['tracking_time']
        GUI.LTimeDisplay.config(text="Time:\t %.1f sec" % GUI.timeDisplay)

    # mousetracking
    #if MM_tracking.Tracking.tracking:
    if Trials.trial_running and GUI.saveTimedTicks.get():
        Timing.times['sec'] = time.time() - Timing.times['sec_time']
        try:
            trial.trial_time = int(GUI.eLengthTrial.get())
        except:
            print("ERROR: no number in Length of trial")
            trial.trial_time = 0

        try:
            track_tick = float(GUI.eTrackTick.get())
        except:
            print("ERROR: no number in Tracking Tick")
            track_tick = 5
        if Timing.times['sec'] >= track_tick and \
        GUI.connectTo.get() == 'Blender':
            calc_move(GUI, maze, data[0])
            Timing.times['sec'] = 0
            Timing.times['sec_time'] = time.time()

        # check for trial end
        if GUI.timeDisplay >= trial.trial_time and trial.trial_time > 0:
            pause_button_text = GUI.startTrialsButton['text']
            if "Pausing" in pause_button_text:
                GUI.startTrialsButton_text.set("Resume")
            elif "Resume" in pause_button_text:
                pass
            else:
                GUI.startTrialsButton_text.set("Pause")
                # only if not paused initiate new trial
                print("Timeout")
                Trials.trial_running = False
                TTL.TTLTrigger(1)
                if GUI.TMaze.get():
                    data[1].add(Answer_side=None)
                    Trials.answers.append(["None", False])
                trial.new_trial(
                    config, tracking_device, data, rules, GUI_Rules, GUI,
                    GUI_Behavior, maze, server, TTL, stim, GUI_FT)
        #
    
    # =========================================================================
    # Network communication
    # =========================================================================
    if server.running:
        if server.handler.readData != '':  # input from blender or psychopy
            Communication.read_TCP_input(
                config, tracking_device, data, GUI, GUI_Rules, GUI_Behavior, 
                maze, rules, server, stim, trial, TTL,
                config.get('conf','newTrialTeleport'), GUI_FT, behavior, 
                GUI_Rules.isOpen())

        tracking_device.send_mouse_data(
            config, data, rules, GUI, GUI_Behavior, maze, server, trial, TTL, 
            GUI_Rules, stim, GUI_FT)

    # calculate speed
    if Timing.times['act_sec'] != \
    int(str(round(Timing.times['session_time'], 1))[-1]):
        
        var.speed = (20. * np.pi) * sum(trial.speedDist) / 360
        trial.speedDist[int(str(round(Timing.times['session_time'], 
                                      1))[-1])] = 0
        Timing.times['act_sec'] = int(str(
                round(Timing.times['session_time'], 1))[-1])
        GUI.LSpeed.config(text="Speed:\t %.1f cm/s" % var.speed)
        if var.speed >= float(GUI.eRunTrigger.get()) and \
        Timing.times['wait_for_trigger']:
            
            # reached
            trial.accSpeed += 1
            if trial.accSpeed >= 10 and Timing.times['wait_for_trigger'] and \
                behavior.answerWindow == 0 and behavior.rewardWindow == 0:
                    
                GUI.LStartLED.config(bg="#86b300", text="Trial Running")
                server.handler.handle_send('+')
                if var.NI and var.digital_output:
                    TTL.TTLTrigger(0)
                data[1].add(trial_start=Timing.get_time())
                Timing.times['wait_for_trigger'] = False

                # Create new Task for counter (delete data from the old one)
                tracking_device.restart()
                print('Starting Trial No %d' % Trials.trial_no)
                #if GUI.startTrackingdirectly.get():
                #    start_tracking(data, GUI, maze)
                #else:
                Trials.trial_running = True
                Timing.times['tracking_time'] = time.time()

    # test if trial ends in tmaze
    if (time.time() > (Timing.times['TM_end_time'] +
        Timing.times['TM_end_timeak_time'])) and \
        Timing.times['TM_end_time'] != 0:  
            
        pause_button_text = GUI.startTrialsButton['text']
        if "Pausing" in pause_button_text:
            GUI.startTrialsButton_text.set("Resume")
        elif "Resume" in pause_button_text:
            pass
        else:
            GUI.startTrialsButton_text.set("Pause")
            # only if not paused initiate new trial
            Timing.times['TM_end_time'] = 0
            Timing.times['TM_end_timeak_time'] = 0
            #

            Trials.trial_running = False
            if not GUI.TMaze.get():
                data[1].add(Answer_side=None)

            if var.digital_output:
                TTL.TTLTrigger(1)

            print("Timeout")
            trial.new_trial(
                config, tracking_device, data, rules, GUI_Rules, GUI, GUI_Behavior,
                maze, server, TTL, stim, GUI_FT)
# =============================================================================
#    updates
# =============================================================================

    #update wheel
    tracking_device.update(config, data, GUI, GUI_Behavior, maze, server, 
                           trial, TTL, rules, GUI_Rules, stim, GUI_FT, 
                           Trials.trial_running)

    #update GUI
    maze.update_sensors()

    #Update Stim and Reward

    if start_airpuff_update == True:
        airpuffthread.start()
        start_airpuff_update = False
        print("threadstarts")
    else:
        pass


    #stim.airpuff_update()
    stim.reward_update(config, tracking_device, data, GUI, maze, server, TTL, 
                       trial, rules, GUI_Behavior, GUI_Rules, GUI_FT)
    TTL.trigger_update()
    
    #update Licksensor
    if GUI_TopMenu.isOpen(GUI_Behavior):
        if GUI_Behavior.lickDetection.get():
            lickSide = behavior.lick_update(Behavior.target, GUI, data, stim, 
                                            GUI_Behavior)
            if lickSide != None:
                #add to TrialData
                data[0].add_row(
                    time=Timing.get_time(), xpos=var.mouse_x, ypos=var.mouse_x,
                    lick=lickSide)
                GUI_Behavior.update_lick(True,lickSide)                            
            else:
                GUI_Behavior.update_lick(False,lickSide)
        #
        
        if behavior.behavior_update(data):
            pause_button_text = GUI.startTrialsButton['text']
            if "Pausing" in pause_button_text:
                GUI.startTrialsButton_text.set("Resume")
            elif "Resume" in pause_button_text:
                pass
            else:
                GUI.startTrialsButton_text.set("Pause")
                # only if not paused initiate new trial
                data[0].save_data(
                            data, GUI.saveFilesTo.get(), GUI.eDataDir.get(),
                            GUI.eFileBaseName.get(), GUI.timeDisplay,
                            Timing.get_time(), GUI)

                trial.new_trial(config, tracking_device, data, rules,
                                            GUI_Rules, GUI, GUI_Behavior, maze,
                                            server,TTL, stim, GUI_FT)
    #
                
    #update Flashtunnel
    if GUI_TopMenu.isOpen(GUI_FT) and Trials.trial_running:     
        if var.mouse_y != None:
            GUI_FT.flashTunnel_update(var.mouse_y-maze.Wall0_y, server, 
                                      '0', '10')
        else:
            GUI_FT.flashTunnel_update(0, server, '0', '10')
                                
    #update GUI        
    GUI.Canvas.update()
    
    
# =============================================================================
#   Closing functions
# =============================================================================
    def on_closing():
        if mbox.askokcancel("Quit", "Do you want to quit?"):
            GUI.Exit = True
                
    master.protocol("WM_DELETE_WINDOW", on_closing)

    if maze.update():
        GUI.Exit = True
        
    if GUI.Exit:
        if var.NI:
            TTL.close()
            
            stim.close()
            tracking_device.__del__()
                
            behavior.close()
            print("Tasks closed")

        #GUI_maze.window.destroy()
        maze.window.destroy()    
        GUI.Canvas.destroy()
        if hasattr(GUI, 'masterReplay'):
            if GUI.isOpen(GUI.windowReplay):
                GUI.windowReplay.destroy()

        if stim.isOpen():
            stim.masterSequ.destroy()
        GUI_TopMenu.closeAll(
            [GUI_FT, GUI_Conf, GUI_MazeConf, GUI_Behavior, GUI_Rules, 
             GUI_Settings, GUIScripts])
        
        master.destroy()
        
if server.running:
    server.stopServer(data, GUI, trial)
print("Quit")
