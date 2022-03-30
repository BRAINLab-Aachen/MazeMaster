import ast
import configparser
import numpy as np
import shutil
import time
import os
import tkinter as tk
from win32api import GetSystemMetrics
from tkinter import messagebox

class GUIMaze():
    """Class containing the window showing the maze and all objects regarding 
    the maze structure"""
    
    def __init__(self, config, GUIRules):
        """Creates the window for displaying the maze and initialzes the maze 
        structure objects"""
        
        self.data = configparser.ConfigParser()
        self.data.read("InputMaze.maze")
        self.winConfig = configparser.ConfigParser()
        self.winConfig.read('windowconf.ini')
        self.maze_wall = []
        self.falseWall = []
        self.Wall0_y = 0
        self.tmaze = False

        # def class variables
        
        #scaling factor for different resolution
        self.scale_x = GetSystemMetrics(0) / 1920 *3
        self.scale_y = GetSystemMetrics(1) / 1080 *3 
        self.grid_res = int(self.winConfig.get('maze_grid', 'grid_res'))
        self.grid_no_width = int(self.winConfig.get('maze_grid', 'grid_no_x'))
        self.grid_no_height = int(self.winConfig.get('maze_grid', 'grid_no_y'))
        self.ratio = self.grid_no_height / self.grid_no_width
        self.space_height = int(
                float(self.winConfig.get('maze_grid', 'ypos')) * self.scale_y)
        self.grid_xpos = int(
                float(self.winConfig.get('maze_grid', 'xpos')) * self.scale_x)
        self.grid_ypos = int(
                float(self.winConfig.get('maze_grid', 'ypos')) * self.scale_y)
        self.width = int(
                float(self.winConfig.get('maze_grid', 'width')) * self.scale_x)
        self.grid_size = self.width / (self.grid_no_width-1)
        self.height = int(self.width * self.ratio)

        self.margin = 2 #no of extra tiles at the borders
        self.Exit = False

        self.sensorWallInactive = []
        self.waypoint = [] #stay here?

        #generate window
        self.window = tk.Tk()
        self.window.title("Maze")
        self.window.minsize(self.width, self.height)# + self.space_height)

        #load window position
        self.window.geometry(
                "+"+str(self.winConfig.get(
                        'Last Window Positions', 'maze_x')) + "+" + \
                str(self.winConfig.get('Last Window Positions', 'maze_y')))

        self.canvas = tk.Canvas(
            self.window, 
            width=self.width + self.grid_xpos, 
            height=self.height + self.grid_ypos,
            bg="#EDEDED")
        self.canvas.pack()
        self.canvas.update()

        # set title in window
        self.Lm_title = tk.Label(
            self.window, 
            text="Maze: " + config.get('Files', 'MazeFile'), 
            font=('Verdana', int(4.9*self.scale_x)))
        self.Lm_title.place(
            x=self.grid_xpos, 
            y=self.grid_ypos/4)

        # draw boundaries and grid
        self.canvas.create_rectangle(
            self.grid_xpos, self.grid_ypos, 
            self.width + self.grid_xpos, self.height + self.grid_ypos, 
            width=2, fill='#E5E5E5')
        self.create_grid()
        
        # create cue
        self.cueMarker = self.canvas.create_rectangle(
            -100, -90, 0, 0, width=1, fill='#EE2C2C')
            

    def resetVariables(self, coords):
        """Resets all variables for changing the window size"""
        
        self.grid_no_width = (coords[2]-coords[0])/self.grid_res
        self.grid_no_height = (coords[3]-coords[1])/self.grid_res

        self.ratio = self.grid_no_height / self.grid_no_width
        self.grid_size = self.width / (self.grid_no_width)
        self.grid_start_x = coords[0]
        self.grid_start_y = coords[1]
        
    def getArea(self):
        """defines the area of the drawing board to show"""
        
        x_min = []
        y_min = []
        x_max = []
        y_max = []
        
        #search for the smallest and biggest numbers
        for wall_no in self.data['Walls']:  
            _wall = ast.literal_eval(self.data.get('Walls', wall_no))
            x_min.append(min(float(_wall[0]),float(_wall[2])))
            y_min.append(min(float(_wall[1]),float(_wall[3])))
            x_max.append(max(float(_wall[0]),float(_wall[2])))
            y_max.append(max(float(_wall[1]),float(_wall[3])))

        #check for endless maze --> take sensor as end of area
        if self.data.get('settings', 'endless') == 'True':
            sensor_tele = ast.literal_eval(self.data.get('Sensors','0'))
            y_max = [float(sensor_tele[3])]
            
        offset = self.margin * self.grid_res
        
        #return start and end point of maze grid
        return ( min(x_min) - offset, min(y_min) - offset, max(x_max) + offset,
                max(y_max) + offset ) 

    def transform(self,val_input):
        return val_input/self.grid_res*self.grid_size
    
    def get(self, window_name, field_name):
        return self.data.get(window_name, field_name)
    
    def update(self):
        """Update function for adjusting to window size and closing of the 
        window has to be run in the main script in the mainloop"""
        
        def configure(event):
            if self.width != min(int((self.window.winfo_height() - \
                                      self.grid_ypos - 4) / self.ratio),
                    int(self.window.winfo_width() - self.grid_xpos - 4)):
            
                self.canvas.delete("all")
                self.width = int(
                        self.window.winfo_width() - self.grid_xpos - 4)
                self.height = min(
                    int(self.ratio * self.width), 
                    int(self.window.winfo_height() - self.grid_ypos - 4))
                self.grid_size = self.height / (self.grid_no_height)
                self.width = int(self.height / self.ratio)
                self.canvas.config(
                    width=self.width + 4, 
                    height=self.height + self.grid_ypos)
                self.canvas.create_rectangle(
                    self.grid_xpos, self.grid_ypos, 
                    self.width + self.grid_xpos, self.height + self.grid_ypos, 
                    width=3, fill='#E5E5E5')

                self.resetVariables(self.getArea())
                self.create_grid()
                self.build_maze()
                
                
        def on_closing():
            """Closes the window after asking to quit"""
            
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.Exit = True
                
        self.canvas.bind("<Configure>", configure)
        self.window.protocol("WM_DELETE_WINDOW", on_closing)
        return self.Exit
    
    def create_grid(self):
        """Draw the grid"""
        
        # vertical lines at an interval of "line_distance" pixel
        for x in np.linspace(0, self.width, int(self.grid_no_width)+1):
            self.canvas.create_line(
                self.grid_xpos + x, 
                self.grid_ypos, 
                self.grid_xpos + x, 
                self.grid_ypos + self.height,
                fill="#476042")
        # horizontal lines at an interval of "line_distance" pixel
        for y in np.linspace(0, self.height, int(self.grid_no_height)+1):
            self.canvas.create_line(
                self.grid_xpos, 
                self.grid_ypos + y,
                self.grid_xpos + self.width, 
                self.grid_ypos + y, 
                fill="#476042")

    def pos_mouse(self, xPos, yPos):
        """Position mouse marker in the maze"""
        
        self.canvas.coords(
          self.mouseMarker,
          self.transform(float(xPos) - self.grid_start_x) + self.grid_xpos - \
              0.2*self.grid_size,
          self.transform(float(yPos) - self.grid_start_y) + self.grid_ypos - \
              0.2*self.grid_size,
          self.transform(float(xPos) - self.grid_start_x) + self.grid_xpos + \
              0.2*self.grid_size,
          self.transform(float(yPos) - self.grid_start_y) + self.grid_ypos + \
              0.2*self.grid_size)           


    def update_sensors(self):
        """Update the sensor times and the color in the maze"""
        
        for n, i in enumerate(self.sensorWallInactive):
            if i > 0:
                if time.time() >= i:
                    self.sensorWallInactive[n] = 0
                    self.canvas.itemconfig(self.sensorWall[n], fill="#FF4500")
                                      
                        
    def position_cue(self, canvas, xPos, yPos):
        """place the marker for cues at the cue position (x,y)"""
        
        canvas.coords(
            self.cueMarker,
            self.transform(float(xPos) - self.grid_start_x) + \
                self.grid_xpos - 0.1*self.grid_size,
            self.transform(float(yPos) - self.grid_start_y) + \
                self.grid_ypos - 0.1*self.grid_size,
            self.transform(float(xPos) - self.grid_start_x) + \
                self.grid_xpos + 0.1*self.grid_size,
            self.transform(float(yPos) - self.grid_start_y) + \
                self.grid_ypos + 0.1*self.grid_size) 

        
    def initialization(self):
        """builds the maze and sets up all values. 
        Is executed once in the main script"""
        
        print('Building Maze...')
        self.resetVariables(self.getArea())

        self.width = int(self.window.winfo_width() - self.grid_xpos - 4)
        self.height = min(
            int(self.ratio * self.width), 
            int(self.window.winfo_height() - self.grid_ypos - 4))
        self.grid_size = self.height / (self.grid_no_height)
        self.width = int(self.height / self.ratio)
        self.canvas.config(
            width=self.width + 4, 
            height=self.height + self.grid_ypos)
        self.canvas.create_rectangle(
            self.grid_xpos, self.grid_ypos, 
            self.width + self.grid_xpos, self.height + self.grid_ypos, 
            width=3,
            fill='#E5E5E5')
        
        self.resetVariables(self.getArea())
        self.create_grid()
        self.build_maze()
        print("done")

    def clearMaze(self):  
        """Deletes all objects from the maze window"""
        
        self.sensorWallNoL = []
        self.falseWallNoL = []
        self.rewardZone = []
        self.mazeWall = []
        self.sensor_Pos = []
        self.sensorWall = []
        self.falseWall = []
        self.canvas.delete("all")

    def load_maze(self, GUI, GUIRules, config):
        """Loads a new maze file and recreates the maze in the maze window.
        Copies all maze textures into the _temp folder for textures"""
        
        LoadMazeFile = tk.filedialog.askopenfilename(initialdir = "Mazes/")
        if LoadMazeFile != '':
            self.clearMaze()
            

            shutil.copyfile(LoadMazeFile, "InputMaze.maze")
            self.data = configparser.ConfigParser()
            self.data.read("InputMaze.maze")
            # maze title
            mazeName = str(os.path.basename(LoadMazeFile)) 
            
            self.Lm_title.config(
                text=("Maze: " + mazeName[:mazeName.find('.maze')]))
            
            config.set_value(
                'Files', 'MazeFile',
                mazeName[:mazeName.find('.maze')])

            #create the new maze
            self.resetVariables(self.getArea())
            self.create_grid()
            self.build_maze()  
            
            #copy textures into the _temp folder for blender
            shutil.copyfile("Data/wall_textures/maze_textures/" + 
                        mazeName[:mazeName.find('.maze')] + "/ceiling.png",
                        "Data/wall_textures/maze_textures/_temp/ceiling.png")
            
            shutil.copyfile("Data/wall_textures/maze_textures/" + 
                        mazeName[:mazeName.find('.maze')] + "/floor.png",
                        "Data/wall_textures/maze_textures/_temp/floor.png")
            
            shutil.copyfile("Data/wall_textures/maze_textures/" + 
                        mazeName[:mazeName.find('.maze')] + "/wall.png",
                        "Data/wall_textures/maze_textures/_temp/wall.png")
            
 
            
            self.canvas.delete("all")
            self.width = int(
                    self.window.winfo_width() - self.grid_xpos - 4)
            self.height = min(
                int(self.ratio * self.width), 
                int(self.window.winfo_height() - self.grid_ypos - 4))
            self.grid_size = self.height / (self.grid_no_height)
            self.width = int(self.height / self.ratio)
            self.canvas.config(
                width=self.width + 4, 
                height=self.height + self.grid_ypos)
            self.canvas.create_rectangle(
                self.grid_xpos, self.grid_ypos, 
                self.width + self.grid_xpos, self.height + self.grid_ypos, 
                width=3, fill='#E5E5E5')

            self.resetVariables(self.getArea())
            self.create_grid()
            self.build_maze()
 
            #change maze title in GUI
            GUI.LmTitle.config(text="Maze: " + 
                               mazeName[:mazeName.find('.maze')], 
                               font='Verdana 12')
    
            #change mazeinfo in GUI
            
            GUI.LEndlessCorridor.config(text="Endless Corridor:  "
                                    + self.get('settings', 'endless'))
            
            GUI.lLengthEndl.config(text="Length of Endless Corridor:  "
                                        + self.get('settings', 
                                                   'endless_length'))
            
            GUI.lEndlFact.config(text="Endless Corridor Factor:  "
                                    + self.get('settings', 
                                               'endless_factor'))
            
            GUI.lNoOfSens.config(text="Number of Sensors:  "
                                    + str(len(self.data['Sensors'])))
    
    def build_maze(self):
        """loads settings from maze input file 
        and creates all canvas objects"""
        
        self.rewardZone = []
        self.sensorWall = []
        self.sensorWall_noL = []
        try:
            if self.data.get('settings', 'tmaze') == 'True':
                self.tmaze = True
            else:
                self.tmaze = False
        except:
            self.tmaze = False

        for wall_no in self.data['Walls']:  
            # build Walls
            _wall = ast.literal_eval(self.data.get('Walls', wall_no))
            if self.data.get('settings', 'endless') == 'True' and \
                    ( int(wall_no)==0 or int(wall_no)==2 ):
                sensor_tele = ast.literal_eval(self.data.get('Sensors','0'))
                self.maze_wall.append(self.canvas.create_line(
                    self.transform(float(_wall[0]) - self.grid_start_x) + \
                        self.grid_xpos,
                    self.transform(float(_wall[1]) - self.grid_start_y) + \
                        self.grid_ypos,
                    self.transform(float(_wall[2]) - self.grid_start_x) + \
                        self.grid_xpos,
                    self.transform(float(sensor_tele[3]) - \
                        self.grid_start_y) + self.grid_ypos,
                    width=2, fill='#7D26CD'))
            else:
                self.maze_wall.append(self.canvas.create_line(
                    self.transform(float(_wall[0]) - self.grid_start_x) + \
                        self.grid_xpos,
                    self.transform(float(_wall[1]) - self.grid_start_y) + \
                        self.grid_ypos,
                    self.transform(float(_wall[2]) - self.grid_start_x) + \
                        self.grid_xpos,
                    self.transform(float(_wall[3]) - self.grid_start_y) + \
                        self.grid_ypos,
                    width=2, fill='#7D26CD'))
        
        for rewNo in sorted(self.data['Rewards']):
            _entry = ast.literal_eval(self.data.get('Rewards',rewNo))
            self.rewardZone.append(self.canvas.create_oval(
                self.transform(float(_entry[0]) - self.grid_start_x) + \
                    self.grid_xpos - 0.2*self.grid_size,
                self.transform(float(_entry[1]) - self.grid_start_y) + \
                    self.grid_ypos - 0.2*self.grid_size,
                self.transform(float(_entry[0]) - self.grid_start_x) + \
                    self.grid_xpos + 0.2*self.grid_size,
                self.transform(float(_entry[1]) - self.grid_start_y) + \
                    self.grid_ypos + 0.2*self.grid_size,
                fill='#1C86EE'))

        _entry = ast.literal_eval(self.data.get('Positions','start'))
        self.startPosMarker = self.canvas.create_oval(
            self.transform(float(_entry[0]) - self.grid_start_x) + \
                self.grid_xpos - 0.2*self.grid_size,
            self.transform(float(_entry[1]) - self.grid_start_y) + \
                self.grid_ypos - 0.2*self.grid_size,
            self.transform(float(_entry[0]) - self.grid_start_x) + \
                self.grid_xpos + 0.2*self.grid_size,
            self.transform(float(_entry[1]) - self.grid_start_y) + \
                self.grid_ypos + 0.2*self.grid_size,
            fill='#49E20E')
        
        # create mouse marker
        self.mouseMarker = self.canvas.create_oval(
            self.transform(float(_entry[0]) - self.grid_start_x) + \
                self.grid_xpos - 0.2*self.grid_size,
            self.transform(float(_entry[1]) - self.grid_start_y) + \
                self.grid_ypos - 0.2*self.grid_size,
            self.transform(float(_entry[0]) - self.grid_start_x) + \
                self.grid_xpos + 0.2*self.grid_size,
            self.transform(float(_entry[1]) - self.grid_start_y) + \
                self.grid_ypos + 0.2*self.grid_size,
            fill='#37FDFC')
        
        
        #teleport position
        _entry = ast.literal_eval(self.data.get('Positions','teleport'))
        if float(_entry[1]) < 700:
            self.teleportMarker = self.canvas.create_oval(
                self.transform(float(_entry[0]) - self.grid_start_x) + \
                    self.grid_xpos - 0.2*self.grid_size,
                self.transform(float(_entry[1]) - self.grid_start_y) + \
                    self.grid_ypos - 0.2*self.grid_size,
                self.transform(float(_entry[0]) - self.grid_start_x) + \
                    self.grid_xpos + 0.2*self.grid_size,
                self.transform(float(_entry[1]) - self.grid_start_y) + \
                    self.grid_ypos + 0.2*self.grid_size,
                fill='#FF6600')
        else:
            self.teleportMarker = self.canvas.create_oval(
            0 * self.grid_size + self.grid_xpos + 0.1*self.grid_size, 
            0 * self.grid_size + self.grid_ypos + 0.1*self.grid_size,
            1 * self.grid_size + self.grid_xpos - 0.1*self.grid_size,
            1 * self.grid_size + self.grid_ypos - 0.1*self.grid_size,
             fill='#FF6600')
            
        if self.data.has_section('Sensors'):    
            for sensorNo in self.data['Sensors']:
                _wall = ast.literal_eval(self.data.get('Sensors',sensorNo))
                self.sensorWall.append(self.canvas.create_line(
                    self.transform(float(_wall[0]) - self.grid_start_x) + \
                        self.grid_xpos,
                    self.transform(float(_wall[1]) - self.grid_start_y) + \
                        self.grid_ypos,
                    self.transform(float(_wall[2]) - self.grid_start_x) + \
                        self.grid_xpos,
                    self.transform(float(_wall[3]) - self.grid_start_y) + \
                        self.grid_ypos,
                    width=2, tags='currentSensor', fill="#FF4500", dash=3))
                self.sensorWallInactive.append(0)

                self.sensorWall_noL.append(self.canvas.create_text(
                    self.transform(float(_wall[0]) - self.grid_start_x) + \
                        self.grid_xpos-5,
                    self.transform(float(_wall[1]) - self.grid_start_y) + \
                        self.grid_ypos,
                    text=str(sensorNo)))

        if self.data.has_section('False Walls'):         
            for falwall_no in self.data['False Walls']:
                _wall = ast.literal_eval(self.data.get('False Walls',
                                                       falwall_no))
                self.falseWall.append(self.canvas.create_line(
                    self.transform(float(_wall[0]) - self.grid_start_x) + \
                        self.grid_xpos,
                    self.transform(float(_wall[1]) - self.grid_start_y) + \
                        self.grid_ypos,
                    self.transform(float(_wall[2]) - self.grid_start_x) + \
                        self.grid_xpos,
                    self.transform(float(_wall[3]) - self.grid_start_y) + \
                        self.grid_ypos,
                    width=2, tags='currentSensor', fill="#668014", dash=3))

                self.falseWall_noL.append(self.canvas.create_text(
                    self.transform(float(_wall[0]) - self.grid_start_x) + \
                        self.grid_xpos-5,
                    self.transform(float(_wall[1]) - self.grid_start_y) + \
                        self.grid_ypos,
                    text=str(falwall_no)))

