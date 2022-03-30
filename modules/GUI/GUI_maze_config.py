import tkinter as tk

class GUIMazeConfig():

    def __init__(self, config):
        self.mmconfig = config
        self.eSensorDelay = tk.Entry()
        
    def openWindow(self):
        """Creates and opens the window"""
        self.window = tk.Tk()
        self.window.title("Maze Config")

        tk.Label(self.window, text="Resize factor Blender (length & width): \
                 ").grid(row=0,column=0,sticky=tk.W)
        self.eResizer = tk.Entry(
            self.window, insertofftime=0, relief=tk.GROOVE, bg="white", 
            width=5)
        self.eResizer.grid(row=0,column=1)
        
        
        tk.Label(self.window, text="heigth of walls (factor of width): \
                 ").grid(row=1,column=0,sticky=tk.W)
        self.eResizerHeigth = tk.Entry(
            self.window, insertofftime=0, relief=tk.GROOVE, bg="white", 
            width=5)
        self.eResizerHeigth.grid(row=1,column=1)

        #Multiple Trial end Zones
        self.newTrialReward = tk.BooleanVar(self.window)
        self.newTrialReward.set(False)
        _cFlash = tk.Checkbutton(
            self.window, text="New Trial after Reward", 
            variable=self.newTrialReward)
        _cFlash.grid(row=2,column=0, sticky=tk.W)

        #New Trial after Teleport
        self.newTrialTeleport = tk.BooleanVar(self.window)
        self.newTrialTeleport.set(False)
        _cFlash = tk.Checkbutton(
                self.window, text="New Trial after Teleport", 
                variable=self.newTrialTeleport)
        _cFlash.grid(row=3,column=0, sticky=tk.W)

        # ### sensors frame ###################################################

        tk.Label(self.window, text="-------------Sensor Barriers-------------"\
                 ).grid(row=5,column=0,columnspan=2)
        
        self.sensorReUse = tk.BooleanVar(self.window)
        self.sensorReUse.set(True)
        _cUseSensor = tk.Checkbutton(
            self.window, text="sensors reusable", variable=self.sensorReUse)
        _cUseSensor.grid(row=6,column=0, sticky=tk.W)

        tk.Label(self.window, text="Sensor Delay by ").grid(row=7,column=0)
        self.eSensorDelay = tk.Entry(
            self.window, insertofftime=0, relief=tk.GROOVE, bg="white", 
            width=5)
        self.eSensorDelay.grid(row=7,column=0, sticky=tk.E)

        tk.Label(self.window, text="sec").grid(row=7,column=1, sticky=tk.W)

        #Save button
        SaveButton = tk.Button(self.window, text = "Save", 
                               command = self.saveConfig)
        SaveButton.grid(row=10,column=1)
        
        self.loadConfig()
        
    def saveConfig(self):
        """Save all values to the config file and closes the window"""
        
        self.mmconfig.set_value(
            'conf', 'sizefactorBlender',
            str(float(self.mmconfig.get('conf','sizefactorPython')) * float(
                    self.eResizer.get())/5))
        
        self.mmconfig.set_value(
            'conf', 'wallHeigth', str(self.eResizerHeigth.get()))

        self.mmconfig.set_value('conf', 'newTrialReward',
                                str(int(self.newTrialReward.get())))
        self.mmconfig.set_value('conf', 'newTrialTeleport',
                                str(int(self.newTrialTeleport.get())))
        self.mmconfig.set_value('conf', 'sensorReUse',
                                str(int(self.sensorReUse.get())))
        self.mmconfig.set_value('conf', 'sensorDelay',
                                str(self.eSensorDelay.get()))

        self.window.destroy()
        
    def loadConfig(self):
        """Load the values from the config file and insert 
        into the entry fields"""

        self.eResizer.insert(0, float(self.mmconfig.get(
                'conf','sizefactorBlender'))/float(
                        self.mmconfig.get('conf','sizefactorPython'))*5)
            
        self.eResizerHeigth.insert(0, self.mmconfig.get('conf','wallHeigth'))
        self.newTrialReward.set(self.mmconfig.get('conf','newTrialReward'))
        self.newTrialTeleport.set(self.mmconfig.get('conf','newTrialTeleport'))
        self.sensorReUse.set(self.mmconfig.get('conf','sensorReUse'))
        self.eSensorDelay.insert(0, self.mmconfig.get('conf','sensorDelay'))


