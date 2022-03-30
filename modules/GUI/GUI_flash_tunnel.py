import tkinter
import random
import ast
import numpy as np
#------------------------------------------------------------------------------
#assisting functions
#------------------------------------------------------------------------------

def flashTunnelCue(direction, ServerObj, cue, time):
    ServerObj.handler.handle_send(
        "$" + direction + "#" + cue +
        "*" + time)
        

class GUIFlashTunnel():
    def __init__(self, config):
        self.stimulusSpaceR = []
        self.stimulusSpaceL = []
        self.distOrder = None
        self.targetOrder = None
        self.targetSide = None
        self.mmconfig = config
        self.modalities = []
        
    def checkTarget(self, maze, *args):
        lenMaze=int(self.ReadLengfhtofMaze(maze)/20)
        if lenMaze==len(self.targetOrder.get()):
            self.LMatchTarget.config(text="Length is matching")
        else:
            self.LMatchTarget.config(text="Length is NOT matching")

    def openWindow(self, maze):    
        self.window = tkinter.Tk()
        self.window.title("Flash Tunnel")

        self.shuffle = tkinter.BooleanVar(self.window)
        self.shuffle.set(True)
        self.CuesVisible = tkinter.BooleanVar(self.window)
        self.CuesVisible.set(False)
        
        tkinter.Label(self.window,text="Random Sequence").grid(row=0,column=0)
        self.cflashTunnel = tkinter.Checkbutton(self.window, text="Shuffle Cues ", variable=self.shuffle)
        self.cflashTunnel.grid(row=1,column=0)

        tkinter.Label(self.window,text="Flash Cues").grid(row=0,column=1)
        self.cflashTunnel = tkinter.Checkbutton(self.window, text="Cues Always Visible", variable=self.CuesVisible)
        self.cflashTunnel.grid(row=1,column=1)
        
        """
        tkinter.Label(self.window,text="No of cues used in sequence" ).grid(row=0,column=2)
        self.eNoCues = tkinter.Entry(self.window,width=10)
        self.eNoCues.insert(0,'0')
        self.eNoCues.grid(row=1,column=2)
        """
        self.targetOrder = tkinter.StringVar(self.window)
        
        tkinter.Label(self.window,text="Target cue sequence (back to front)" ).grid(row=0,column=2)
        self.eTargetOrder = tkinter.Entry(self.window, textvariable=self.targetOrder, width=50)
        self.eTargetOrder.grid(row=1,column=2)


        self.targetOrder.trace(
            "w", 
            lambda *args: self.checkTarget(maze, *args))

        self.LMatchTarget = tkinter.Label(self.window,text="No of target cues not matching" )

        self.LMatchTarget.grid(row=1,column=3)
        
        #LmatchCuelen = tkinter.Label(self.window,text="Target cue sequence")
        #LmatchCuelen.grid(row=0,column=4)foreground='RED'
        
        """

        tkinter.Label(self.window,text="Stimulus No left").grid(row=2,column=0)
        self.eNoStimL = tkinter.Entry(self.window,width=20)
        self.eNoStimL.grid(row=3,column=0)
        self.eNoStimL.insert(0,'0')

        tkinter.Label(self.window,text="Stimulus No right").grid(row=2,column=1)
        self.eNoStimR = tkinter.Entry(self.window,width=20)
        self.eNoStimR.grid(row=3,column=1)
        self.eNoStimR.insert(0,'0')
        
        tkinter.Label(self.window,text="Extra space at end").grid(row=2,column=2)
        self.eDeadspace = tkinter.Entry(self.window,width=20)
        self.eDeadspace.insert(0,'20')
        self.eDeadspace.grid(row=3,column=2)
        
        """
        

        tkinter.Label(self.window,text="Extra tiles at start").grid(row=2,column=0)
        self.eDeadspaceStart = tkinter.Entry(self.window,width=20)
        self.eDeadspaceStart.grid(row=3,column=0)

        """
        tkinter.Label(self.window,text="Lenght of tunnel: " ).grid(row=5,column=0)
        self.eLenght = tkinter.Entry(self.window,width=20)
        self.eLenght.insert(0,str(self.ReadLengfhtofMaze()))
        self.eLenght.grid(row=5,column=1)
        """
        """
        self.eStimListT = []
        self.eStimListD = []
        tkinter.Label(self.window,text="Stim Target" ).grid(row=6,column=0)
        tkinter.Label(self.window,text="Stim Distractor" ).grid(row=6,column=1)
        for stim in range(10):
            #target
            self.eStimListT.append(tkinter.Entry(self.window,width=20))
            #self.eStimListT[-1].insert(0,'')
            self.eStimListT[-1].grid(row=7+stim,column=0)
            #distractor
            self.eStimListD.append(tkinter.Entry(self.window,width=20))
            #self.eStimListD[-1].insert(0,'')
            self.eStimListD[-1].grid(row=7+stim,column=1)
        """    
            
        """    
        tkinter.Label(self.window,text="Trigger Left" ).grid(row=6,column=2)            
        tkinter.Label(self.window,text="Trigger Right" ).grid(row=6,column=3)     
        
        
        
        self.triggerLeft = tkinter.StringVar(self.window)
        self.triggerLeft .set('never')
        
        triggerList = ("never", "start of experiment", "start of trial", 
                       "end of trial")

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
        
        """
        self.useAirPuffs = tkinter.BooleanVar(self.window)
        self.useAirPuffs.set(False)
        
        self.cAirPuffs = tkinter.Checkbutton(self.window, text="Use Air Puffs",
                                             variable=self.useAirPuffs)
        self.cAirPuffs.grid(row=2,column=1)
        
        tkinter.Label(self.window,text="air puff cue number").grid(row=2,column=2)
        self.eAirpuffcue = tkinter.Entry(self.window,width=20)
        #self.eAirpuffcue.insert(0,'1')
        self.eAirpuffcue.grid(row=3,column=2)
        
        #modality
        tkinter.Label(self.window,text="Modality probability (between 0 and 1)",
                      font='Arial 12 bold').grid(row=4,column=1)
        
        tkinter.Label(self.window,text="visual").grid(row=5,column=0)
        self.visual = tkinter.Entry(self.window,width=20)
        
        self.visual.grid(row=6,column=0)
        
        tkinter.Label(self.window,text="tactile").grid(row=5,column=1)
        self.tactile = tkinter.Entry(self.window,width=20)
        self.tactile.grid(row=6,column=1)
        
        
        tkinter.Label(self.window,text="Modality:").grid(row=5,column=2)
        
        self.lModality = tkinter.Label(self.window,text="None",
                                       font='Arial 14 bold')
        self.lModality.grid(row=6,column=2)
        
        
        self.useModBiasCorr = tkinter.BooleanVar(self.window)
        self.useModBiasCorr.set(False)
        self.cModalityBias = tkinter.Checkbutton(self.window, 
                                                 text="Enable Modality Bias correction",
                                                 variable=self.useModBiasCorr)
        self.cModalityBias.grid(row=8,column=1)
        
        self.saveButton = tkinter.Button(
            self.window, 
            text="set as default", 
            compound="bottom", 
            command=lambda: self.saveConfig(),
            bg=None)
        self.saveButton.grid(row=9,column=4)
        
        self.loadConfig()
    
    def modBiasCorr(self, answers, noTrials=20):
        """calculates a bias for a certain modality and return the modality 
        with the lowest performance with a certian improved probability
        0=visual, 1=tactile, 2=multisensory"""

        perf = [[],[],[]]
        if len(answers) > noTrials:
            for i in range(noTrials):
                if answers[-(i+1)][1] != 'None':
                    perf[self.modalities].append(answers[-(i+1)][1])
            

            arr_perf = np.array(np.sum(perf[0])/len(perf[0]),
                                np.sum(perf[1])/len(perf[1]),
                                np.sum(perf[2])/len(perf[2]))
            
            return np.where(arr_perf == np.amin(arr_perf))[0][0]
        else:            
            return None

    
    def calcModality(self, answers):
        """returns the modality by the chances entered by the user in the 
        entry fields: 0=visual, 1=tactile, 2=multisensory"""
        #use bias correction for modality
        if self.useModBiasCorr.get():
            _mod = self.modBiasCorr(answers)
            
            #not enough trials for bias correction, go back to random
            if _mod == None:
                _rand = random.random()           
                if _rand <= float(self.visual.get()):
                    _mod = 0
                elif _rand <= float(self.visual.get())+float(self.tactile.get()):
                    _mod=1
                else:
                    _mod=2
        #random modality
        else:    
            _rand = random.random()           
            if _rand <= float(self.visual.get()):
                _mod = 0
            elif _rand <= float(self.visual.get())+float(self.tactile.get()):
                _mod=1
            else:
                _mod=2
            
        if _mod == 0:    
            self.useAirPuffs.set(False)
            self.lModality.config(text="Visual")
            self.modalities.append(0)
            return 0
        if _mod == 1:        
            self.useAirPuffs.set(True)
            self.lModality.config(text="Tactile")
            self.modalities.append(1)
            return 1
        elif _mod == 2:
            self.useAirPuffs.set(True)
            self.lModality.config(text="Multisensory")
            self.modalities.append(2)
            return 2
        else:
            print("ERROR: modality could not be calculated")
            return None

    def ReadLengfhtofMaze(self, maze):
           
        return float(ast.literal_eval(maze.data.get('Walls', '0'))[3]) - \
            float(ast.literal_eval(maze.data.get('Walls', '0'))[1])


    def getNoStim(self):
        return self.eNoStimL.get() , self.eNoStimR.get(), self.eDeadspace.get()

    def setLenght(self, lenght):
        self.eLenght.insert(0,str(lenght))
        
    
    def randomSide(self, biasCorr, BiasCorrection):
        if biasCorr:
            return str(BiasCorrection)
        else:
            _randSide = random.getrandbits(1)
            if _randSide == 0:
                return 'right'
            elif _randSide == 1:
                return 'left'

    def resetFlashTunnel(self, maze, BiasCorrection):
        
        jitter = 0 #random 
        stimListNo = []
        for n,i in enumerate(self.eStimListT):
            if i.get() != '':
                stimListNo.append(n)
                
        mazelength = int(self.ReadLengfhtofMaze(maze))
        biasCorr = False
        NoL = 0.0
        NoR = 0.0
        if self.shuffle and stimListNo != []:
            ranNo = random.choice(stimListNo)
            target = self.randomSide(biasCorr, BiasCorrection)
            
            if target == 'right':
                NoR = int(self.eStimListT[ranNo].get())
                NoL = int(self.eStimListD[ranNo].get())
            elif target == 'left':
                NoL = int(self.eStimListT[ranNo].get())
                NoR = int(self.eStimListD[ranNo].get())
            else:
                print("ERROR")
                NoL = int(self.eNoStimL.get())
                NoR = int(self.eNoStimR.get())
        else:
            NoL = int(self.eNoStimL.get())
            NoR = int(self.eNoStimR.get())
            target = self.randomSide(biasCorr, BiasCorrection)

        if NoL > 0:      
            self.stimulusSpaceL = []  
            if NoL >= 2:
                _space = (mazelength-int(self.eDeadspace.get())-int(
                                self.eDeadspaceStart.get()))/(NoL-1)
                for i in range(NoL-1):
                    self.stimulusSpaceL.append(int(
                            self.eDeadspaceStart.get())+_space*(i)+jitter)
                    
                #add second cue at end of maze    
                self.stimulusSpaceL.append(mazelength-int(
                                self.eDeadspace.get()))
            else:
                self.stimulusSpaceL.append(int(self.eDeadspaceStart.get()))
        if NoR > 0:
            self.stimulusSpaceR = []
            if NoR >=2:
                _space = (mazelength-int(self.eDeadspace.get())-int(
                            self.eDeadspaceStart.get()))/(NoR-1)
                for i in range(NoR-1):
                    self.stimulusSpaceR.append(
                            int(self.eDeadspaceStart.get())+_space*(i)+jitter)
                #add second cue at end of maze    
                self.stimulusSpaceR.append(mazelength-int(
                                self.eDeadspace.get()))
            else:
                self.stimulusSpacer.append(int(self.eDeadspaceStart.get()))

        return target


    def flashTunnel_update(self, position, ServerObj, cue, time):
        if self.CuesVisible.get() == False:

            for n,i in enumerate(self.stimulusSpaceR):
                if position >= i:
                    flashTunnelCue('right', ServerObj, cue, time)
                    self.stimulusSpaceR[n] = 9999999
                    
            for n,i in enumerate(self.stimulusSpaceL):
                if position >= i:
                    flashTunnelCue('left', ServerObj, cue, time)
                    self.stimulusSpaceL[n] = 9999999
                    
    
    def setAirPuffs(self, distOrder, targetOrder, targetSide): 
        self.distOrder = distOrder
        self.targetOrder = targetOrder
        self.targetSide = targetSide
        
    def checkAirPuffs(self, sensorNo):
        """
        Checks if the sensor matches the position of the target cue in target 
        or distractor sequence and 
        returns the air puffs trigger as (left, right)
        """
        _dist = False
        _target = False
        for n, i in enumerate(self.distOrder):          
            if str(i) == str(self.eAirpuffcue.get()):
                if n - int(self.eDeadspaceStart.get()) == int(sensorNo): #match
                    _dist = True
        for n, i in enumerate(str(self.targetOrder[::-1])):          
            if str(i) == str(self.eAirpuffcue.get()):
                if n - int(self.eDeadspaceStart.get()) == int(sensorNo): #match
                    _target = True           
                    
        if self.targetSide == 'right': 
            return (_dist, _target)#left right 
        elif self.targetSide == 'left':
            return (_target, _dist)#left right 
        else:
            return (False, False)
        
        
    def saveConfig(self):
        """Saves the values in the config file"""
        self.mmconfig.set_value('conf', 'spaceStart', self.eDeadspaceStart.get())
        self.mmconfig.set_value('conf', 'targetOrder', self.eTargetOrder.get())
        self.mmconfig.set_value('conf', 'useAirPuffs', str(self.useAirPuffs.get()))
        self.mmconfig.set_value('conf', 'airpuffcue', self.eAirpuffcue.get())
        self.mmconfig.set_value('conf', 'visual', self.visual.get())
        self.mmconfig.set_value('conf', 'tactile', self.tactile.get())
        self.mmconfig.set_value('conf', 'useModBiasCorr', str(self.useModBiasCorr.get()))

        
    def loadConfig(self):
        """Loads the values from the config file and fill them in"""
        
        self.eDeadspaceStart.insert(0, self.mmconfig.get('conf', 'spaceStart'))
        self.eTargetOrder.insert(0, self.mmconfig.get('conf', 'targetOrder'))
        self.eAirpuffcue.insert(0, self.mmconfig.get('conf', 'airpuffcue'))
        self.useAirPuffs.set(self.mmconfig.get('conf', 'useAirPuffs'))
        self.visual.insert(0, self.mmconfig.get('conf', 'visual'))
        self.tactile.insert(0, self.mmconfig.get('conf', 'tactile'))
        try:
            self.useModBiasCorr.set(self.mmconfig.get('conf', 'useModBiasCorr'))
        except:
            pass
        #

    def isOpen(self):
        """Check if window is open and return state as bool"""
        try:
            if 'normal' == self.window.state():
                return True
            else:
                return False
        except:
            return False                     
