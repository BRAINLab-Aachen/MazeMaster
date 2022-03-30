import tkinter
import random
from copy import deepcopy
'''
file_open also in drop_down
Sensor_var_false_wall same as is dropdown?
rule_active, also a variable in rules: do we need both?
'''

class GUIRules():
    def __init__(self):
        self.stndDict = {"sensor_var1": -1,
                     "sensor_var2": -1,
                     "sensor_var_false_wall": -1,
                     "shuffle": False,
                     "teleport": False,
                     "cuesVar1": -1,
                     "cuesVar2": -1,
                     "rule_cue_direction": "right",
                     }

    def isOpen(self):
        try:
            if 'normal' == self.window.state():
                return True
            else:
                return False
        except:
            return False
        
    def add_rule_row(self, rules):
        """Add an additional row to the list of rules and initialize 
        with the default rules"""
        self.rows += 1
        #sensor
        self.sensor_var1.append(tkinter.IntVar(self.window))
        self.sensor_var2.append(tkinter.IntVar(self.window)) 
        self.sensor_var1[-1].set(-1) # default value
        self.sensor_var2[-1].set(-1) # default value
        

        self.sensor_var_false_wall.append(tkinter.IntVar(self.window))
        self.sensor_var_false_wall[-1].set(-1) # default value

        tkinter.OptionMenu(
            self.window,
            self.sensor_var1[-1],
            *self.opt_sensors
            ).grid(row=self.rows,column=0)
        tkinter.OptionMenu(
            self.window, 
            self.sensor_var2[-1], 
            *self.opt_sensors
            ).grid(row=self.rows,column=1)

        tkinter.OptionMenu(
            self.window, 
            self.sensor_var_false_wall[-1],
            *self.false_walls
            ).grid(row=self.rows,column=6)

        #Shuffle
        self.shuffle.append(tkinter.BooleanVar(self.window)) 
        self.shuffle[-1].set(False)

        tkinter.Checkbutton(
            self.window, 
            text="Shuffle Cues ", 
            variable=self.shuffle[-1]
            ).grid(row=self.rows,column=7)

        #Teleport
        self.teleport.append(tkinter.BooleanVar(self.window)) 
        self.teleport[-1].set(False)

        tkinter.Checkbutton(
            self.window, 
            text="Use Teleport ", 
            variable=self.teleport[-1]
            ).grid(row=self.rows,column=8)

        #rule: Cue
        self.cuesVar1.append(tkinter.IntVar(self.window))
        self.cuesVar1[-1].set(-1)

        tkinter.OptionMenu(
            self.window, 
            self.cuesVar1[-1],
            *self.OptCues
            ).grid(row=self.rows,column=3)

        self.cuesVar2.append(tkinter.IntVar(self.window))
        self.cuesVar2[-1].set(-1)

        tkinter.OptionMenu(
            self.window, 
            self.cuesVar2[-1],
            *self.OptCues2
            ).grid(row=self.rows,column=5)

        self.rule_cue_direction.append(tkinter.StringVar(self.window))
        self.rule_cue_direction[-1].set('right')

        tkinter.OptionMenu(
            self.window, 
            self.rule_cue_direction[-1],
            "left","right","both"
            ).grid(row=self.rows,column=4)

        self.add_button.grid(row=self.rows+1, column = 0)

        rules.add_rule(deepcopy(self.stndDict))

    def openWindow(self, _maze, rules):
        self.rows = 0
        
        #check for correct parameter type and transform if necessary
        if isinstance(_maze, tuple):
            maze = _maze[0]
        else:
            maze = _maze
            
        Sensors = len(maze.sensorWall)
        FWalls = len(maze.falseWall)

        self.sensor_var1 = []
        self.sensor_var2 = []
        self.sensor_var_false_wall = []
        self.shuffle = []
        self.teleport = []
        self.cuesVar1 = []
        self.cuesVar2 = []
        self.rule_cue_direction = []
        #self.opt_sensors = []
        
        def file_open():
            f = tkinter.filedialog.askopenfilename(defaultextension=".txt")
             # asksaveasfile return `None` if dialog closed with "cancel".
            if f is '':
                return
            file = open(f)
            n=-1
            i=0
            self.Rules = []
            self.rule_active = []
            entry=['' for i in range(9)]
            for line in file:
                for ch in line:
                
                    if ch!='#':
                        entry[i]=entry[i]+ch                    
                    else:                 
                        i=i+1
                n=n+1
                self.sensor_var1[n].set(int(entry[0]))
                self.sensor_var2[n].set(int(entry[1]))
                self.cuesVar1[n].set(int(entry[2]))
                self.rule_cue_direction[n].set(entry[3])
                self.cuesVar2[n].set(int(entry[4]))
                self.shuffle[n].set(bool(int(entry[5])))
                self.sensor_var_false_wall[n].set(int(entry[6]))
                self.teleport[n].set(bool(int(entry[7])))
                
                self.rules.append(
                    [self.sensor_var1[n].get(), 
                    self.Sensor_var2[n].get(),
                    self.CuesVar1[n].get(),
                    self.rule_cue_direction[n].get(),
                    self.cuesVar2[n].get(),
                    self.sensor_var_false_wall[n].get()])
                self.rule_active.append(False)
                i=0
                entry=['' for i in range(9)]
            file.close()

        def file_save():
            f = tkinter.filedialog.asksaveasfile(
                mode='w', defaultextension=".txt")
            # asksaveasfile return `None` if dialog closed with "cancel".
            if f is None: 
                return
            self.rules = []
            self.rule_active = []
            for i in range(self.rows):
                text2save = str(
                    self.sensor_var1[i].get()) + "#"\
                    + str(self.Sensor_var2[i].get()) + "#"\
                    + str(self.CuesVar1[i].get()) + "#"\
                    + self.rule_cue_direction[i].get() + "#"\
                    + str(self.cuesVar2[i].get()) + "#" \
                    + str(int(Shuffle[i].get())) + "#" \
                    + str(self.sensor_var_false_wall[i].get()) + "#" \
                    + str(int(self.teleport[i].get())) + "#\n"
                f.write(text2save)
                self.rules.append(
                    [self.sensor_var1[i].get(),
                    self.sensor_var2[i].get(),
                    self.cues_var1[i].get(),
                    self.rule_cue_direction[i].get(),
                    self.cuesVar2[i].get(),
                    self.sensor_var_false_wall[i].get()])
                self.rule_active.append(False)
                
            f.close() 
            

        self.window = tkinter.Tk()
        self.window.title("Rules")

        tkinter.Button(
            self.window, 
            text="Save Rules",
            command=file_save
            ).grid(row=0,column=7)
        tkinter.Button(
            self.window, 
            text="Load Rules",
            command=file_open
            ).grid(row=0,column=8)


        self.opt_sensors = []
        self.opt_sensors.append(-1)

        self.false_walls = []
        self.false_walls.append(-1)

        for i in range(Sensors):
            self.opt_sensors.append(i)

        for i in range(FWalls):
            self.false_walls.append(i)    


        self.OptCues = []
        self.OptCues.append(-1)

        self.OptCues2 = []
        self.OptCues2.append(-1)

        for i in range(5):
            self.OptCues.append(i)
            self.OptCues2.append(i)

        tkinter.Label(
            self.window,
            text="Choose Sensor: ").grid(row=0,column=0)
        tkinter.Label(
            self.window,
            text="additional Sensor: ").grid(row=0,column=1)
        tkinter.Label(
            self.window,
            text=" | Rules: ",font = "Verdana 10 bold").grid(row=0,column=2)
        tkinter.Label(
            self.window,
            text="Show Cue No: ").grid(row=0,column=3)
        tkinter.Label(
            self.window,
            text="Direction: ").grid(row=0,column=4)
        tkinter.Label(
            self.window,
            text="2nd Cue No(left side): ").grid(row=0,column=5)
        tkinter.Label(
            self.window,
             text="Activate false Wall: ").grid(row=0,column=6)


        self.add_button = tkinter.Button(
            self.window, 
            text=" Add Rule ", 
            command=lambda:self.add_rule_row(rules)
            )
        self.add_button.grid(row=1, column=0, columnspan=9, sticky='WE')

        self.add_rule_row(rules)
            
    def getSensors(self, no):
        return (self.sensor_var1[no].get(), self.sensor_var2[no].get())
    
    def getCues(self, no):
        """Return numbers of the left and right cues for rule no"""
        _cueL = None
        _cueR = None
        
        if self.rule_cue_direction[no].get() == 'right':                   
            _cueL = None
            _cueR = self.cuesVar1[no].get()
        elif self.rule_cue_direction[no].get() == 'left':
            _cueL = self.cuesVar1[no].get()
            _cueR = None
        elif  self.rule_cue_direction[no].get() == 'both':
            _cueL = self.cuesVar2[no].get()
            _cueR = self.cuesVar1[no].get()

        if self.shuffle[no].get(): #shuffle
            if random.getrandbits(1) == 1: #switch stimuli with 50% chance
                _cueL,_cueR = _cueR,_cueL

        return (_cueL, _cueR)
    
    def getCueDirection(self, no): ###--->not used
        return self.rule_cue_direction[no].get()

    def getFalseWallNo(self, no):
        return self.sensor_var_false_wall[no].get()

    def get_setrule_active(self, no, change=None):
        """set and get value for active first sensor of rule no"""
        if change != None:
            self.rule_active[no] = change
        return self.rule_active[no]

    def getTeleport(self, no):
        return self.teleport[no].get()

    def getShuffle(self, no): ###--->not used
        return self.shuffle[no].get()

    def updateRules(self, rules):
        """Updates the GUI elements with the rules"""
        
        for row in range(self.rows):
            self.sensor_var1[row].set(rules[row]["sensor_var1"])
            self.sensor_var2[row].set(rules[row]["sensor_var2"])
            self.cuesVar1[row].set(rules[row]["cuesVar1"])
            self.cuesVar2[row].set(rules[row]["cuesVar2"])
            self.teleport[row].set(rules[row]["teleport"])
            self.rule_cue_direction[row].set(rules[row]["rule_cue_direction"])
            self.sensor_var_false_wall[row].set(rules[row]["sensor_var_false_wall"])
        
    def resetRules():
        """deletes all rules"""

        
