##############################################################################
#
# Maze Builder for VR Maze
#
# Copyright 2015, Alexander Bexter, Alexander.Bexter@rwth-aachen.de
#
#
import tkinter as tk
from tkinter import messagebox as mbox
import tkinter.filedialog
import configparser
import os
import numpy as np
import sys
from PIL import Image, ImageTk
import shutil
import ast

sys.path.append('../modules')
sys.path.append('modules')

from MM_maze import Maze

import var


###--->maybe class with init: canvas = GUI.Canvas
###--->then also all variables defined

def checkered(canvas, line_distance):
    # vertical lines at an interval of "line_distance" pixel
    for x in range(line_distance, window_width, line_distance):
        canvas.create_line(
            var.margin+x, var.margin, var.margin+x, var.margin+window_height, 
            fill="#476042")
    # horizontal lines at an interval of "line_distance" pixel
    for y in range(line_distance,window_height,line_distance):
        canvas.create_line(
            var.margin, var.margin+y, var.margin+window_width, var.margin+y, 
            fill="#476042")

def draw_dots(canvas, radius):
    for i in range(int(window_width/var.resolution)+1): #number in width
        for p in range(int(window_height/var.resolution)+1): #number in height
            dot.append(canvas.create_oval( ###---> what is dot and where it is used?
                var.margin + (i*var.resolution) - radius,
                var.margin + (p*var.resolution) - radius,
                var.margin + (i*var.resolution) + radius,
                var.margin + (p*var.resolution) + radius, 
                fill='#000000', activefill='#00CD00'))
            
def on_dot_click(event, canvas):  
    if modus_Sensor_draw_Pos ==False and modus_Sensor_Pos ==False:
    
        selected_dot = canvas.find_withtag("current")
        if var.modus_select == True: 
            #add maze wall        
            TempCoords = canvas.coords(selected_dot)
            TempCoords[0] = TempCoords[0]+radius
            TempCoords[1] = TempCoords[1]+radius
            MazeWall.append(canvas.create_line(
                var.dot_coords[0], var.dot_coords[1], 
                TempCoords[0], TempCoords[1], 
                width=2, fill='#7D26CD', activefill='#E32636'))
            #Test for right mousebutton on Wall (DELETE WALL)
            for i in MazeWall:
                canvas.tag_bind(
                    i, '<ButtonPress-3>',
                    lambda event: delete_wall(event, canvas))
            #write wall to file

            TempString = [ 
                var.dot_coords[0] - var.margin, var.dot_coords[1] - var.margin, 
                TempCoords[0] - var.margin, TempCoords[1] - var.margin]
            TempMazeData.append(TempString)
       
        var.modus_select = True
        var.dot_coords = canvas.coords(selected_dot)
        var.dot_coords[0] = var.dot_coords[0] + radius
        var.dot_coords[1] = var.dot_coords[1] + radius

def save(maze, canvas): 
    global RewPos
    global eMazeName, EndlessCorridor, FalseWall_Pos, StartPosMarker
    if eMazeName.get() !='':
        _tempdict = {} 
        saveDict  = {}
        #if open_mode == False:
        save = True
        if os.path.isfile(eMazeName.get()) == True or \
                os.path.isfile(eMazeName.get()+'.maze') == True: #file already exists
            if mbox.askyesno(
                    "Overwrite", "File already exists, overwrite?",
                    icon='warning', master=canvas) ==False:
                save = False
        if save == True:   

            #Enable different Gratings for a linear track
            _tempdict['gratings'] = EnableGratings.get()
                
            #Enable Endless corridor        
            _tempdict['endless'] = EndlessCorridor.get()
            
            #Set Tmaze
            if NumRewards<2 and TMaze.get():
                mbox.showerror("Not enough reward areas", "Place at least one reward zone in each arm of the TMaze")
                return
            else:    
                _tempdict['tmaze'] = TMaze.get()
            
            if EndlessCorridor.get():
                #Endless corridor factor             
                _tempdict['endless_factor'] = EEndlessfact.get()
                
                #Endless corridor length   
                _tempdict['endless_length'] = ENoPics.get()
            else:
                _tempdict['endless_length'] = 0
                _tempdict['endless_factor'] = 0
                
                
            _tempdict['reward_visible'] = RewardVisible.get()    
             
            saveDict['settings'] = _tempdict
            _tempdict = {}
             
            #check for emty maze
            if TempMazeData == []:
                mbox.showerror('Exception','Maze is empty')
                return
            
            for i, wall in enumerate(TempMazeData):  
                _tempdict[str(i)] = wall
            saveDict['Walls'] = _tempdict
            _tempdict = {}
         
            #rewards          
            for i, rewards in enumerate(RewardZone):
                RewPos = canvas.coords(rewards)
                _tempdict[str(i)] = [RewPos[0]+5 - var.margin, RewPos[1]+5 - var.margin]
            saveDict['Rewards'] = _tempdict
            _tempdict = {}  
         
            #Sensors
            for i,sensors in enumerate(Sensor_Pos):
                _tempdict[str(i)] = sensors
            saveDict['Sensors'] = _tempdict
            _tempdict = {}   
           
            #False Walls   
            for i, entry in enumerate(FalseWall_Pos):
                _tempdict[str(i)] = entry
            saveDict['False Walls'] = _tempdict
            _tempdict = {}    
         
            #Starting position
            StrtPos = canvas.coords(StartPosMarker)
            #file.write("%"+str(StrtPos[0]+5-var.margin)+'#'+str(StrtPos[1]+5-var.margin)+"#\n")
            _tempdict['Start'] = [
                StrtPos[0]+5 - var.margin, StrtPos[1]+5 - var.margin]
            #Teleport position
            TelePos = canvas.coords(TeleportMarker)
            #file.write("*"+str(TelePos[0]+5-var.margin)+'#'+str(TelePos[1]+5-var.margin)+"#\n")
            _tempdict['Teleport'] = [
                TelePos[0]+5 - var.margin, TelePos[1]+5 - var.margin]
            saveDict['Positions'] = _tempdict
         
         
            for name, dict_ in saveDict.items():             
                maze.write(mazeFolder + eMazeName.get() + '.maze', name, dict_)
        
            saveTextures()
            print ("Data saved!")
            
    else:
        mbox.showerror("Name missing", "Maze has no name, not saved!")

def clear_maze(canvas):
    global NumRewards,RewardZone
    global Sensor_Pos,SensorWall
    global TempMazeData,MazeWall
   
   
    NumRewards = 0
    for entry in RewardZone:
        canvas.delete(entry)

    for Wall in MazeWall:
        canvas.delete(Wall)


    for Sensor in SensorWall:
        canvas.delete(Sensor)

    RewardZone =[]
    MazeWall=[]
    Sensor_Pos=[]
    SensorWall =[]
    TempMazeData=[]
   
def open_maze(canvas): 
    global open_mode
    global file_path
    global TempMazeData, WallPositions
    global NumRewards
    global Sensor_Pos,SensorWall
    global EnableGratings
    global LRewards
   
    TempMazeData = []
    file_path = tkinter.filedialog.askopenfilename()
    if file_path != '':
        clear_maze(canvas)
        data = configparser.ConfigParser()
        data.read(file_path)
        
        #open_mode = True
        #Tempfile = open(file_path, "r")
      
        #TempfileLines = Tempfile.readlines()
        #insert name into textbox
        eMazeName.delete(0, 'end')
        eMazeName.insert(0, os.path.splitext(os.path.basename(file_path))[0])

        #insert Maze
        for wallNo in data['Walls']:  
            # build Walls
            coord = ast.literal_eval(data.get('Walls', wallNo))
        

            #build Walls
            MazeWall.append(canvas.create_line(
                coord[0] + var.margin, coord[1] + var.margin,
                coord[2] + var.margin, coord[3] + var.margin, 
                width=2, fill='#7D26CD', activefill='#E32636'))
            #Test for right mousebutton on Wall (DELETE WALL)
            for i in MazeWall:
                canvas.tag_bind(
                    i, '<ButtonPress-3>', 
                    lambda event: delete_wall(event, canvas))
            #write wall to file
            TempString = [ 
                coord[0], coord[1],
                coord[2], coord[3]]
            TempMazeData.append(TempString)
                
            #TempMazeData.append(MazeWall[-1])
            WallPositions.append(MazeWall[-1])#coord[0], coord[1], coord[2], coord[3])

        for rewNo in data['Rewards']:
            _rewards = ast.literal_eval(data.get('Rewards',rewNo))

            RewardZone.append(canvas.create_oval(
                _rewards[0]-5 + var.margin, _rewards[1]-5 + var.margin,
                _rewards[0]+5 + var.margin, _rewards[1]+5 + var.margin, 
                fill='#1C86EE', activefill='#FF00FF'))       
            for i in RewardZone:
                canvas.tag_bind(
                    i, '<ButtonPress-1>', 
                    lambda event: on_reward_click(event, canvas))



        _entry = ast.literal_eval(data.get('Positions','start'))    
            
        canvas.coords(
            StartPosMarker,
            _entry[0]-5 + var.margin, _entry[1]-5 + var.margin,
            _entry[0]+5 + var.margin, _entry[1]+5 + var.margin)
            
##            elif line[0] == '*': #Teleport position
##                #get coords
##                coord = ['' for i in range(3)]
##                i = 0
##
##                #Read out digits
##                for ch in line:
##                    if ch != '*':
##                        if ch != '#':
##                            coord[i] += ch                    
##                        else: 
##                            coord[i] = int(float(coord[i]))            
##                            i += 1
##
##                canvas.coords(
##                    TeleportMarker,
##                    coord[0]-5 + var.margin, coord[1]-5 + var.margin,
##                    coord[0]+5 + var.margin, coord[1]+5 + var.margin)   
##                
##            elif line[0] == '!': #Sensor
##                SenCoords=['' for i in range(5)]
##                i=0
##                for ch in line:
##                   if ch!='!':
##                      if ch!='#':
##                         SenCoords[i]=SenCoords[i]+ch
##                      else:                     
##                         SenCoords[i]=int(float(SenCoords[i]))
##                         i=i+1
##                         
##                SensorWall.append(canvas.create_line(
##                    SenCoords[0] + var.margin, SenCoords[1] + var.margin,
##                    SenCoords[2] + var.margin, SenCoords[3] + var.margin, 
##                    width=2, tags='currentSensor', fill="#FF4500", dash=3))
##                
##                #really strange stuff happening here...
##                Sensor_Pos.append([
##                    SenCoords[0] - var.margin, SenCoords[1] - var.margin,
##                    SenCoords[2] - var.margin, SenCoords[3] - var.margin])
##
##                canvas.tag_bind(
##                    SensorWall[-1], '<ButtonPress-3>', 
##                    lambda event: delete_sensor(event, canvas))
##            
##            elif line[0] == '&': #False Wall
##                SenCoords = ['' for i in range(5)]
##                i = 0
##                for ch in line:
##                    if ch != '&':
##                        if ch != '#':
##                            SenCoords[i] += ch
##                        else:                     
##                            SenCoords[i] = int(float(SenCoords[i]))
##                            i += 1
##                         
##                SensorWall.append(canvas.create_line(
##                    SenCoords[0] + var.margin, SenCoords[1] + var.margin,
##                    SenCoords[2] + var.margin, SenCoords[3] + var.margin, 
##                    width=2, tags='currentSensor', fill="#668014", dash=3))
##                
##                #really strange stuff happening here...
##                FalseWall_Pos.append([
##                    SenCoords[0], SenCoords[1], SenCoords[2], SenCoords[3]])
##
##                canvas.tag_bind(
##                    SensorWall[-1], '<ButtonPress-3>', 
##                    lambda event: delete_sensor(event, canvas))
##               
##            elif line[0] == '?': #enable different gratings for a linear track
##                if line[1] == '0': #False
##                    EnableGratings.set(False)
##                elif line[1] == '1': #True
##                    EnableGratings.set(True)
##                   
##            elif line[0] == '+': #enable Endless Corridor
##                if line[1] == '0': #False
##                    EndlessCorridor.set(False)
##                elif line[1] == '1': #True
##                    EndlessCorridor.set(True)      
##            
##        Tempfile.close()

def quit_maze(): ###--->master, os?
    master.destroy()
    os._exit(1)
    
def draw_maze_line(event, canvas):
    global Sensor_Pos_Temp
    if var.modus_select == True:  #draw Maze Wall to mouse 
        #Line shift
        #x-axis
        xshift = event.x - var.dot_coords[0]
        #y-axis
        yshift = event.y - var.dot_coords[1]

        totalshift = abs(xshift) + abs(yshift)
        if totalshift > 0:
            xshift = xshift/totalshift
            yshift = yshift/totalshift
       
        #Line update (Temp Wall)
        canvas.coords(
            TempWall, 
            var.dot_coords[0], var.dot_coords[1],
            event.x - (xshift*4), event.y - (yshift*4))


    if modus_Start_Pos == True: #Start position positioning
        canvas.coords(
            StartPosMarker, event.x - 5, event.y - 5, event.x + 5, event.y + 5)
    if modus_teleport_Pos == True:
        canvas.coords(
            TeleportMarker, event.x - 5, event.y-5,event.x+5,event.y+5)
    if var.modus_select_reward == True: #Reward positioning
        canvas.coords(
            selected_Reward, event.x - 5, event.y - 5, event.x + 5, event.y + 5)
    if modus_Sensor_draw_Pos ==True: #light sensor drawing
        canvas.coords(
            SensorWallTemp, Sensor_Pos_Temp[0], Sensor_Pos_Temp[1], event.x, event.y)    
       
def abort(event, canvas):
    global modus_Start_Pos,modus_teleport_Pos
    global modus_Sensor_Pos,modus_Sensor_draw_Pos
    if var.modus_select ==True: #abort new maze wall positioning
        var.modus_select=False
        canvas.coords(TempWall, 0, 0, 0, 0)
       
    if modus_Start_Pos == True:  #Start positioning abort
        modus_Start_Pos = False
        canvas.coords(
            StartPosMarker, StartPos[0], StartPos[1], 
            StartPos[0] + 10, StartPos[1] + 10)
       
    if modus_teleport_Pos == True:
        modus_teleport_Pos = False   
        canvas.coords(
            TeleportMarker, TeleportPos[0], TeleportPos[1],
            TeleportPos[0] + 10, TeleportPos[1] + 10)
 
    if modus_Sensor_draw_Pos == True or modus_Sensor_Pos == True:
        modus_Sensor_draw_Pos =False
        modus_Sensor_Pos =False
        canvas.coords(SensorWallTemp, 0, 0, 0, 0)
      
def delete_wall(event, canvas):
    global dWall
    dWall = canvas.find_withtag("current")
     
    #remove from list
    dWallCoords = canvas.coords(dWall)
    SearchString = [ 
                dWallCoords[0] - var.margin, dWallCoords[1] - var.margin, 
                dWallCoords[2] - var.margin, dWallCoords[3] - var.margin]
                
    TempMazeData.remove(SearchString)
    #remove from screen
    MazeWall.remove(dWall[0])
    canvas.delete(dWall)

def delete_sensor(event, canvas): 
    global FalseWall_Pos

    dSensor = canvas.find_withtag("current")
    print(dSensor)
    print(Sensor_Pos)
    print(canvas.coords(dSensor))
    try:
        Sensor_Pos.remove(canvas.coords(dSensor))
    except:
        FalseWall_Pos.remove(canvas.coords(dSensor))
           
    canvas.delete(dSensor)
   
def place_start():
    global modus_Start_Pos
    modus_Start_Pos= True

def place(event, canvas):
    global modus_Start_Pos,modus_teleport_Pos
    global modus_Sensor_Pos
    global modus_Sensor_draw_Pos
    global first_click
    global Sensor_Pos_Temp
    global Sensor_Pos
    global FalseWall_Pos, FalseWall

    if modus_Sensor_draw_Pos == True:
        modus_Sensor_draw_Pos = False
        Sensor_Pos_Temp[2] = event.x
        Sensor_Pos_Temp[3] = event.y
        if FalseWall.get() == False:
            SensorWall.append(canvas.create_line(
                Sensor_Pos_Temp[0], Sensor_Pos_Temp[1], 
                Sensor_Pos_Temp[2], Sensor_Pos_Temp[3], 
                width=2, tags='currentSensor', fill="#FF4500", dash=3))
        else:
            SensorWall.append(canvas.create_line(
                Sensor_Pos_Temp[0], Sensor_Pos_Temp[1],
                Sensor_Pos_Temp[2], Sensor_Pos_Temp[3], 
                width=2, tags='currentSensor',fill="#668014",dash=3))

        canvas.coords(SensorWallTemp, 0, 0, 0, 0)
        #really strange stuff happening here...
        gg = [
            Sensor_Pos_Temp[0] - var.margin, Sensor_Pos_Temp[1] - var.margin,
            Sensor_Pos_Temp[2] - var.margin, Sensor_Pos_Temp[3] - var.margin]
        if FalseWall.get() == False:
            Sensor_Pos.append(gg)#Sensor_Pos_Temp)
        else:
            FalseWall_Pos.append(gg)    
          

        canvas.tag_bind(
            SensorWall[-1], '<ButtonPress-3>', 
            lambda event: delete_sensor(event, canvas))
      
      
    if modus_Sensor_Pos == True:    #positioning "light sensor" point for cues
        modus_Sensor_draw_Pos = True
        Sensor_Pos_Temp[0] = event.x
        Sensor_Pos_Temp[1] = event.y
        modus_Sensor_Pos = False
      
    if modus_Start_Pos == True:    #positioning Starting point
        modus_Start_Pos = False
        canvas.coords(
            StartPosMarker, event.x - 5, event.y - 5, event.x + 5, event.y + 5)
      
    if modus_teleport_Pos==True:
        modus_teleport_Pos = False
        canvas.coords(
            TeleportMarker, event.x - 5, event.y - 5, event.x + 5, event.y + 5)
          
      
    if var.modus_select_reward ==True:    #positioning Reward point
        if first_click == False:
            first_click = True
        else:
            var.modus_select_reward = False
            canvas.coords(
                selected_Reward, event.x - 5, event.y - 5, event.x + 5, event.y + 5)

def add_reward(canvas):
    global NumRewards,LRewards, RewardZone
    NumRewards += 1
    LRewards.config(text="Rewards: "+str(NumRewards))
    n = len(RewardZone)
    RewardZone.append(canvas.create_oval(
        var.margin+170 + (n*30), var.margin + window_height+60, 
        var.margin+170 + (n*30)+10, var.margin + window_height + 60+10, 
        fill='#1C86EE', activefill='#FF00FF'))
    for i in RewardZone:
        canvas.tag_bind(
            i, '<ButtonPress-1>', lambda event: on_reward_click(event, canvas))
   
def remove_reward(canvas):
    global NumRewards,LRewards
    if NumRewards > 0:
        NumRewards -= 1
        LRewards.config(text="Rewards: "+str(NumRewards))
        canvas.delete(RewardZone.pop())
      
def on_reward_click(event, canvas):
    global first_click
    global selected_Reward
    if var.modus_select_reward == False and modus_Start_Pos == False \
            and modus_teleport_Pos == False:
        var.modus_select_reward = True
        selected_Reward = canvas.find_withtag("current")
        first_click = False
        #

def add_sensor():
    global modus_Sensor_Pos
    modus_Sensor_Pos =True
   
def set_teleporter_point(): 
    global modus_teleport_Pos
    modus_teleport_Pos = True   
 
def show_help():
    HelpFile = open('documentation.txt','r')
    mbox.showinfo("Documentation", HelpFile.read())

def create_maze_by_numbers(canvas): 
    global EMazeX, EMazeY, ESensorPos,MazeWall,TempMazeData
    clear_maze(canvas)
    add_reward(canvas)
    #build Walls
    posx0 = 10 * var.resolution
    #y1
    MazeWall.append(canvas.create_line(
        posx0 + var.margin, var.margin, 
        posx0 + var.margin, int(EMazeY.get()) + var.margin, 
        width=2, fill='#7D26CD', activefill='#E32636'))
    #x1
    MazeWall.append(canvas.create_line(
        posx0 + var.margin, int(EMazeY.get()) + var.margin, 
        posx0 + int(EMazeX.get()) + var.margin, int(EMazeY.get()) + var.margin, 
        width=2, fill='#7D26CD', activefill='#E32636'))
    #y2
    MazeWall.append(canvas.create_line(
        posx0 + int(EMazeX.get()) + var.margin, var.margin, 
        posx0 + int(EMazeX.get()) + var.margin, int(EMazeY.get()) + var.margin, 
        width=2, fill='#7D26CD', activefill='#E32636'))
    #x2
    MazeWall.append(canvas.create_line(
        posx0 + var.margin, var.margin, 
        posx0 + int(EMazeX.get()) + var.margin, var.margin, 
        width=2, fill='#7D26CD', activefill='#E32636'))
    #Test for right mousebutton on Wall (DELETE WALL)
    for i in MazeWall:
        canvas.tag_bind(
            i, '<ButtonPress-3>', lambda event: delete_wall(event, canvas))
    #write wall to file
    TempMazeData.append([
        posx0, 0, posx0, EMazeY.get()])
    TempMazeData.append([
        posx0, EMazeY.get(), 
        posx0 + int(EMazeX.get()), int(EMazeY.get())])
    TempMazeData.append([
        posx0 + int(EMazeX.get()), 0, 
        posx0 + int(EMazeX.get()), int(EMazeY.get())])
    TempMazeData.append([
        posx0, 0, 
        posx0 + int(EMazeX.get()), 0])
    
    #start position marker
    canvas.coords(
        StartPosMarker, 
        posx0+(int(EMazeX.get())/2) - 5 + var.margin,
        StartPosition-5 + var.margin, 
        posx0 + (int(EMazeX.get())/2)+5 + var.margin, 
        StartPosition+5 + var.margin)
    
    #sensor walls
    if ESensorPos.get() != "":
        SensorWall.append(canvas.create_line(
            posx0 + var.margin, int(ESensorPos.get()) + var.margin,
            posx0 + int(EMazeX.get()) + var.margin, int(ESensorPos.get()) 
            + var.margin, 
            width=2, tags='currentSensor', fill="#FF4500", dash=3))
        Sensor_Pos.append([
            posx0, int(ESensorPos.get()), 
            posx0 + int(EMazeX.get()), int(ESensorPos.get())])

def create_maze(canvas, endless=False): 
    global EndlessCorridor, eMazeName, Flash
    global pic,pic_phot
    
    if endless:
        EndlessCorridor.set(True)    
    noPics = int(ENoPics.get())
    
    var.endless_width = 20
    if endless:
        var.endless_heigth = noPics * var.endless_width * int(EEndlessfact.get())
    else:    
        var.endless_heigth = noPics * var.endless_width +int(ENoPicsADDB.get()) * var.endless_width+ int(ENoPicsADD.get())*var.endless_width
    var.viewoffset = 5.2
    addB = int(ENoPicsADDB.get()) * var.endless_width
    #addE = int(eAddEnd.get()) * var.endless_width
    #addB = 0
    addE = 0
    
    clear_maze(canvas)
    add_reward(canvas)

    #build Walls
    posx0 = 10*var.resolution
    #y1
    MazeWall.append(canvas.create_line(
        posx0 + var.margin, var.margin, 
        posx0 + var.margin, int(var.endless_heigth) + var.margin, 
        width=2, fill='#7D26CD', activefill='#E32636'))
    #x1
    MazeWall.append(canvas.create_line(
        posx0 + var.margin, int(var.endless_heigth) + var.margin,
        posx0 + int(var.endless_width) + var.margin, 
        int(var.endless_heigth) + var.margin, 
        width=2, fill='#7D26CD', activefill='#E32636'))
    #y2
    MazeWall.append(canvas.create_line(
        posx0 + int(var.endless_width) + var.margin, var.margin,
        posx0 + int(var.endless_width) + var.margin, 
        int(var.endless_heigth) + var.margin, 
        width=2, fill='#7D26CD', activefill='#E32636'))
    #x2
    MazeWall.append(canvas.create_line(
        posx0 + var.margin, var.margin,
        posx0 + int(var.endless_width) + var.margin, var.margin, 
        width=2, fill='#7D26CD', activefill='#E32636'))

    #Test for right mousebutton on Wall (DELETE WALL)
    for i in MazeWall:
        canvas.tag_bind(
            i, '<ButtonPress-3>', lambda event: delete_wall(event, canvas))
    #write wall to file        
    TempMazeData.append([
        str(posx0), str(0), str(posx0), str(var.endless_heigth)])
    TempMazeData.append([
        str(posx0), str(var.endless_heigth), 
        str(posx0+int(var.endless_width)), str(var.endless_heigth)])
    TempMazeData.append([
        str(posx0+int(var.endless_width)), str(0), 
        str(posx0+int(var.endless_width)), str(var.endless_heigth)])
    TempMazeData.append([
        str(posx0), str(0), 
        str(posx0+int(var.endless_width)), str(0)])
    
    #start position marker
    canvas.coords(
        StartPosMarker,
        posx0 + (int(var.endless_width)/2)-5 + var.margin, 
        StartPosition-5 + var.margin,
        posx0 + (int(var.endless_width)/2)+5 + var.margin,
        StartPosition+5 + var.margin)
    #TeleportMarker
    canvas.coords(
        TeleportMarker,
        posx0 + (int(var.endless_width)/2)-5 + var.margin,
        StartPosition-5 + var.margin,
        posx0 + (int(var.endless_width)/2)+5 + var.margin,
        StartPosition+5 + var.margin)
    
    
    #sensor walls
    if endless:
        SensorWall.append(canvas.create_line(
            posx0 + var.margin,
            (noPics) * var.endless_width + var.margin + StartPosition + var.viewoffset + addB + addE,
            posx0 + int(var.endless_width) + var.margin,
            (noPics) * var.endless_width + var.margin + StartPosition + var.viewoffset + addB + addE, 
            width=2, tags='currentSensor', fill="#FF4500", dash=3))
        Sensor_Pos.append([
            posx0, 
            (noPics) * var.endless_width + StartPosition + var.viewoffset + addB + addE,
            posx0 + int(var.endless_width), 
            (noPics) * var.endless_width + StartPosition + var.viewoffset + addB + addE])    
    
    #Flash Images
    for i in range(0,noPics):
        _y_pos = i * var.endless_width + StartPosition + var.viewoffset + addB
        #sensor walls
        SensorWall.append(canvas.create_line(
            posx0 + var.margin, _y_pos + var.margin, 
            posx0 + int(var.endless_width) + var.margin, _y_pos + var.margin, 
            width=2, tags='currentSensor', fill="#FF4500", dash=3))
        Sensor_Pos.append([posx0,_y_pos,posx0+int(var.endless_width),_y_pos])  
               
def load_pics(canvas):
    global pic,pic_phot
    filename = tk.filedialog.askopenfilename(
        multiple=True, title='Please select pictures')
    #insert blanks in between pictures
    Image_array=np.insert(
        filename[1:], np.arange(len(filename[1:])), filename[0])
    print(Image_array)
    imgs = [ Image.open(i) for i in Image_array ]
    
    for n,img in enumerate(imgs):
        img.thumbnail((32,32))
        pic_phot.append(ImageTk.PhotoImage(img))
        pic.append(tk.Label(canvas, image=pic_phot[-1]))
        pic[-1].place(x=n*40 + window_width + (var.margin+10), y=var.margin + 300)
        
def add_picture(canvas):
    global pic,pic_phot,currPic,WallImages
    filename = tk.filedialog.askopenfilename(
        multiple=False,title='Please select picture')
    print(filename)
    img = Image.open(filename)
    WallImages.append(filename)
    img.thumbnail((32,32))
    pic_phot.append(ImageTk.PhotoImage(img))
    pic.append(tk.Label(canvas, image=pic_phot[-1]))
    pic[-1].place(x=currPic*40 + window_width + var.margin+10, y=var.margin+560)
    currPic += 1
    


def saveTextures():
    name = eMazeName.get()
    
    if os.path.isdir("Data/wall_textures/maze_textures/_temp/"):
        savepathFrom = "Data/wall_textures/maze_textures/_temp/"
        savepathTo =  "Data/wall_textures/maze_textures/"   
             
    elif os.path.isdir("../Data/wall_textures/maze_textures/_temp/"):
        savepathFrom =  "../Data/wall_textures/maze_textures/_temp/"
        savepathTo =  "../Data/wall_textures/maze_textures/"       
        
    os.makedirs(savepathTo+name)    
    shutil.copyfile(savepathFrom+"ceiling.png", savepathTo+name+"/ceiling.png")
    shutil.copyfile(savepathFrom+"floor.png", savepathTo+name+"/floor.png")
    shutil.copyfile(savepathFrom+"wall.png", savepathTo+name+"/wall.png")

def setCeiling():
    global ceilingPicMiniThump,ceilingPicMini
    CueTex = tk.filedialog.askopenfilename()
    if CueTex != '':
        if os.path.isdir("Data/wall_textures/maze_textures/_temp/"):
            savepath =  "Data/wall_textures/maze_textures/_temp/"   
             
        elif os.path.isdir("../Data/wall_textures/maze_textures/_temp/"):
            savepath =  "../Data/wall_textures/maze_textures/_temp/"
             
        shutil.copyfile(CueTex, savepath+"ceiling.png")
        with open(savepath+"ceiling.png", 'rb') as image_file:
            with Image.open(image_file) as _image:
                _image.thumbnail((200, 37), Image.ANTIALIAS)
                ceilingPicMiniThump = ImageTk.PhotoImage(_image)
                ceilingPicMini = tk.Label(canvas, image=ceilingPicMiniThump)
                ceilingPicMini.place(x=x+100,y=y+yPos[1])  

def setFloor():
    global floorPicMiniThump,floorPicMini
    CueTex = tk.filedialog.askopenfilename()
    if CueTex != '':
        if os.path.isdir("Data/wall_textures/maze_textures/_temp/"):
            savepath =  "Data/wall_textures/maze_textures/_temp/"   
             
        elif os.path.isdir("../Data/wall_textures/maze_textures/_temp/"):
            savepath =  "../Data/wall_textures/maze_textures/_temp/"  
             
        shutil.copyfile(CueTex, savepath+"floor.png")
        with open(savepath+"floor.png", 'rb') as image_file:
            with Image.open(image_file) as _image:
                _image.thumbnail((200, 37), Image.ANTIALIAS)
                floorPicMiniThump = ImageTk.PhotoImage(_image)
                floorPicMini = tk.Label(canvas, image=floorPicMiniThump)
                floorPicMini.place(x=x+100,y=y+yPos[2])   


def setWalltex():
    global wallPicMiniThump,wallPicMini
    CueTex = tk.filedialog.askopenfilename()
    if CueTex != '':
        if os.path.isdir("Data/wall_textures/maze_textures/_temp/"):
            savepath =  "Data/wall_textures/maze_textures/_temp/"   
             
        elif os.path.isdir("../Data/wall_textures/maze_textures/_temp/"):
            savepath =  "../Data/wall_textures/maze_textures/_temp/"  
             
        shutil.copyfile(CueTex, savepath+"wall.png")
        with open(savepath+"wall.png", 'rb') as image_file:
            with Image.open(image_file) as _image: 
                _image.thumbnail((200, 37), Image.ANTIALIAS)
                wallPicMiniThump = ImageTk.PhotoImage(_image)
                wallPicMini = tk.Label(canvas, image=wallPicMiniThump)
                wallPicMini.place(x=x+100,y=y+yPos[0])


master = tk.Tk()
master.title("Maze Builder 1.1")
master.protocol("WM_DELETE_WINDOW", quit_maze)  # This properly closes the window if not done by the quit button
dot = []
open_mode = False
modus_Start_Pos = False
modus_teleport_Pos = False
var.modus_select_reward = False
modus_Sensor_Pos = False
modus_Sensor_draw_Pos = False
first_click = False
EnableGratings = tk.BooleanVar()
EnableGratings.set(False)
EndlessCorridor = tk.BooleanVar()
EndlessCorridor.set(False)
TMaze = tk.BooleanVar()
TMaze.set(False)
RewardVisible = tk.BooleanVar()
RewardVisible.set(False)
Flash = tk.BooleanVar()
Flash.set(False)
WallPositions = []
pic = []
pic_phot = []
StartPosition = 8.35
currPic = 0
WallImages = []

current_folder_path, current_folder_name = os.path.split(os.getcwd())
if current_folder_name == 'MazeBuilder' or current_folder_name == 'MazeBuilderV2_ex':
    mazeFolder = '../Mazes/'
else:
    mazeFolder = 'Mazes/'

maze = Maze(15, 60)

#Create TempData
TempMazeData = []

#Starting Point
StartingPos = [0,0]

#Reward Zone Positions
RewardPositions = []

#global MazeWall
MazeWall=[]

#width of border
var.margin = 100

#radius of dots
radius = 3

#space between grid/points
var.resolution = 20 
# var.resolution = maze_GUI.width / maze_GUI.grid_no_width

#dimensions of the maze
window_width = var.resolution*40
window_height = var.resolution*30

canvas = tk.Canvas(
    master, 
    width=window_width + (2*var.margin) + 170, 
    height=window_height + (2*var.margin))


#Draw boundaries
canvas.create_rectangle(
    var.margin, var.margin, var.margin + window_width, var.margin + window_height, 
    width=3, fill='#E5E5E5')

#Draw Grid
checkered(canvas,var.resolution)

#entry(name of maze) window
tk.Label(canvas, text="Name of Maze:").place(x=var.margin, y=20)
eMazeName = tk.Entry(canvas, bg='#D3D3D3', relief=tk.GROOVE, insertofftime=0)
eMazeName.place(x=var.margin+100, y=20, width=260, height=20)
#number of reward zones
NumRewards = 1
LRewards = tk.Label(canvas, text="Rewards: "+str(NumRewards))
LRewards.place(x=(var.margin) + 170, y=var.margin + window_height+30)

cRewardVisible = tk.Checkbutton(
    master, text="rewards visible ", variable=RewardVisible)
cRewardVisible.place(x=(var.margin) + 170, y=var.margin + window_height+75)


#Buttons
#top
OpenButton = tk.Button(
    canvas, 
    text="Open", fg="black",
    command=lambda: open_maze(canvas),
    bg='#D3D3D3').place(
        x=window_width + var.margin-400, y=20, width=100, height=20)
SaveButton = tk.Button(
    canvas,
    text="Save", fg="black",
    command= lambda: save(maze, canvas),
    bg='#D3D3D3').place(
        x=window_width + var.margin-280, y=20, width=100, height=20)
QuitButton = tk.Button(
    canvas, 
    text="Quit", fg="black",
    command=quit_maze, bg='#D3D3D3').place(
        x=window_width + var.margin-100, y=20, width=100, height=20)
#bottom
StartPosButton = tk.Button(
    canvas, 
    text="Place Start", fg="black",
    command=place_start,
    bg='#D3D3D3').place(
        x=var.margin+20, y=var.margin + window_height+30, width=100, height=20)
#add reward -button
AddRewardButton = tk.Button(canvas,
    text="+", fg="black",
    command=lambda: add_reward(canvas),
    bg='#D3D3D3').place(
        x=var.margin+280, y=var.margin + window_height+30, width=20, height=20)
#light sensor
AddSensorButton = tk.Button(
    canvas, text="Add Sensor", fg="black",
    command=add_sensor,
    bg='#D3D3D3').place(
        x=var.margin+460, y=var.margin + window_height+30, width=100, height=20)
#remove reward -button
remove_rewardButton = tk.Button(
    canvas, 
    text="-", fg="black",
    command=lambda: remove_reward(canvas),
    bg='#D3D3D3').place(
        x=var.margin+250, y=var.margin + window_height+30, width=20, height=20)

#panels right side
# =============================================================================
# Create Maze by Values
# =============================================================================

y_gap=90

tk.LabelFrame(
    canvas, 
    text="Create Maze by Values", font="Verdana 8 bold", fg='black', 
    bd=6, width=220, height=260, labelanchor='n',
    relief = tk.RIDGE).place(x=window_width + var.margin+20, y=var.margin-y_gap)

tk.Label(
    canvas, 
    text="Lenght of a tile: " + str(var.resolution)).place(
        x=window_width + (1.5*var.margin), y=var.margin+30-y_gap)

tk.Label(
    canvas, 
    text="Tunnel Walls:").place(
        x=window_width + 1.5*var.margin, y=var.margin+60-y_gap)
tk.Label(
    canvas, 
    text="width").place(
        x=window_width + 1.5*var.margin, y=var.margin+80-y_gap)
EMazeX = tk.Entry(
    canvas, bg='#D3D3D3', relief=tk.GROOVE, insertofftime=0, width=10)
EMazeX.place(x=window_width + (1.5*var.margin), y=var.margin+100-y_gap)
EMazeX.insert(0, 20)

tk.Label(canvas, text="lenght").place(
    x = window_width+(1.5*var.margin)+100, y = var.margin+80-y_gap)
EMazeY = tk.Entry(
    canvas, bg='#D3D3D3', relief=tk.GROOVE, insertofftime=0, width=10)
EMazeY.place(x=window_width + (1.5*var.margin)+100, y=var.margin+100-y_gap)
EMazeY.insert(0, 0)

tk.Label(
    canvas, text="Sensor Position:").place(
        x=window_width + (1.5*var.margin), y=var.margin+130-y_gap)
ESensorPos = tk.Entry(
    canvas, bg='#D3D3D3', relief=tk.GROOVE, insertofftime=0, width=10)
ESensorPos.place(x=window_width + (1.5*var.margin), y=var.margin+150-y_gap)
ESensorPos.insert(0,"")

CreateMazeButton = tk.Button(
    canvas, text="Create Maze", fg="black",
    command=lambda: create_maze_by_numbers(canvas),bg='#D3D3D3').place(
        x=window_width + (1.5*var.margin), y=var.margin+180-y_gap)


# =============================================================================
# Create Maze by Pictures
# ============================================================================= 
tk.LabelFrame(
    canvas, text="Create Maze by Pictures", font="Verdana 8 bold", fg='black', 
    bd=6, width=220, height=200, labelanchor='n', relief=tk.RIDGE).place(
        x=window_width + var.margin+20, y=var.margin+270-y_gap)


tk.Label(
    canvas, text="Number of \n pictures:").place(
        x=window_width + (1.5*var.margin), y=var.margin+300-y_gap-10)
ENoPics = tk.Entry(
    canvas, bg='#D3D3D3', relief=tk.GROOVE, insertofftime=0, width=5)
ENoPics.place(x=window_width + (1.5*var.margin), y=var.margin+330-y_gap)
ENoPics.insert(0, 6)

tk.Label(
    canvas, text="Additional \n Squares:").place(
        x=window_width + (1.5*var.margin)+90, y=var.margin+300-y_gap-15)

tk.Label(
    canvas, text="end:").place(
        x=window_width + (1.5*var.margin)+90, y=var.margin+300-y_gap+15)
ENoPicsADD = tk.Entry(
    canvas, bg='#D3D3D3', relief=tk.GROOVE, insertofftime=0, width=5)
ENoPicsADD.place(x=window_width + (1.5*var.margin)+90, y=var.margin+330-y_gap+10)
ENoPicsADD.insert(0, 1)

tk.Label(
    canvas, text="start:").place(
        x=window_width + (1.5*var.margin)+130, y=var.margin+300-y_gap+15)
ENoPicsADDB = tk.Entry( 
    canvas, bg='#D3D3D3', relief=tk.GROOVE, insertofftime=0, width=5)
ENoPicsADDB.place(x=window_width + (1.5*var.margin)+130, y=var.margin+330-y_gap+10)
ENoPicsADDB.insert(0, 1)


tk.Label(
    canvas, text="Endless Maze Factor:").place(
        x=window_width + (1.5*var.margin), y=var.margin+360-y_gap)
EEndlessfact = tk.Entry(
    canvas, bg='#D3D3D3', relief=tk.GROOVE, insertofftime=0, width=10)
EEndlessfact.place(x=window_width + (1.5*var.margin), y=var.margin+390-y_gap)
EEndlessfact.insert(0, 6)

CreateEndlessMazeButton = tk.Button(
    canvas, text="Create Endless Maze", fg="black",
    command=lambda: create_maze(canvas, endless=True), bg='#D3D3D3').place(
        x=window_width + (var.margin*1.5)-20, y=var.margin+430-y_gap)

CreateMazeButton = tk.Button(
    canvas, text="Create Maze", fg="black",
    command=lambda: create_maze(canvas, endless=False), bg='#D3D3D3').place(
        x=window_width + (var.margin*1.5)+110, y=var.margin+430-y_gap)

# =============================================================================
# Load Textures
# =============================================================================
x = window_width + (1.5*var.margin)
y=var.margin+470-y_gap+10
yPos = np.arange(30,1000,60)

tk.LabelFrame(
    canvas, text="Textures", font="Verdana 8 bold", fg='black', 
    bd=6, width=220, height=210, labelanchor='n', relief=tk.RIDGE).place(
        x=x-30, y=y)

tk.Button(
        canvas, text="Background", compound=tk.RIGHT,
        anchor="w", command=lambda: setWalltex(), justify="left").place(
        x=x,y=y+yPos[0],width=80, height=35)


tk.Button(
        canvas, text="Ceiling", compound=tk.RIGHT,
        anchor="w", command=lambda: setCeiling(), justify="left").place(
        x=x,y=y+yPos[1],width=80, height=35)


tk.Button(
    canvas, text="Floor", compound=tk.RIGHT,
    anchor="w", command=lambda: setFloor(), justify="left").place(
    x=x,y=y+yPos[2],width=80, height=35)



#Enable different Gratings (for linear Track)
cEnableGratings = tk.Checkbutton(
    master, text="Enable Wall Pictures ", variable=EnableGratings)
cEnableGratings.place(x=(var.margin)+600, y=var.margin + window_height+30)

#Enable endless corridor
cEndlessCorridor = tk.Checkbutton(
    master, text="Endless Corridor ", variable=EndlessCorridor)
cEndlessCorridor.place(x = (var.margin)+600, y=var.margin + window_height+50)

#Set Tmaze
cTmaze = tk.Checkbutton(
    master, text="T-Maze ", variable=TMaze)
cTmaze.place(x = (var.margin)+600, y=var.margin + window_height+70)

#Set up a teleporter point
SetTeleport = tk.Button(
    canvas, text="Teleporter Point", fg="black",
    command=set_teleporter_point,bg='#D3D3D3').place(
        x=(var.margin)+340, y=var.margin + window_height+30, width=100, height=20)
TeleportPos = [var.margin+340,var.margin+window_height+60]
TeleportMarker = canvas.create_oval(
    TeleportPos[0], TeleportPos[1], TeleportPos[0]+10, TeleportPos[1]+10, 
    fill='#FF6600')

#Place a false wall
FalseWall = tk.BooleanVar()
FalseWall.set(False)
cFalseWall = tk.Checkbutton(master, text="False Wall ", variable=FalseWall)
cFalseWall.place(
    x=(var.margin)+460, y=var.margin+window_height+60, 
    width=100, height=20)

#Draw Dots
draw_dots(canvas, radius)

#Create Temp Wall (line between cursor and selected dot)
TempWall=canvas.create_line(0, 0, 0, 0, width=1, tags='currentline')

#Create Temp Sensor Wall (line between cursor and selected dot)
SensorWallTemp=canvas.create_line(
    0, 0, 0, 0, width=2, tags='currentSensor',fill="#FF4500",dash=3)
SensorWall=[]

#create start position marker
StartPos = [var.margin+20, var.margin + window_height+60]
StartPosMarker = canvas.create_oval(
    StartPos[0], StartPos[1], StartPos[0]+10, StartPos[1]+10, fill='#49E20E')

#Create Reward zone marker
RewardZone=[]

Sensor_Pos_Temp = [0 for i in range(4)]
Sensor_Pos = []
FalseWall_Pos=[]

RewardZone.append(canvas.create_oval(
    var.margin+170, var.margin + window_height+60,
    var.margin+170+10, var.margin + window_height+60+10, 
    fill='#1C86EE', activefill='#FF00FF'))
for i in RewardZone:
   canvas.tag_bind(i, '<ButtonPress-1>', lambda event: on_reward_click(event, canvas))
   
#Test for mouseklick event on circles
for i in dot:
    canvas.tag_bind(i, '<ButtonPress-1>', lambda event: on_dot_click(event, canvas))

canvas.bind("<ButtonPress-3>", lambda event: abort(event, canvas))
canvas.bind("<ButtonPress-1>", lambda event: place(event, canvas))

#Test for mousemovement for Mazewall positioning
canvas.bind("<Motion>", lambda event: draw_maze_line(event, canvas)) 

canvas.pack()
#w.update()
tk.mainloop()
