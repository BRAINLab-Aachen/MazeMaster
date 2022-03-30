import tkinter as tk
import time

from MM_trial import Trials
from MM_behavior import Behavior

class GUIBehavior():

    '''
    still as GUI-variables used...in:
    AnswerLED_L...communication
    AnswerLED_R...communication

    StimLED_L...trial
    StimLED_R...trial

    lickDetection...MazeMaster
    '''
    def __init__(self):
        self.lickLEDdelay = [0,0] #left,right

    def openWindow(self):

        self.window = tk.Tk()
        self.window.title("Behavior")
        #Current Reward side/ Answer
        tk.Label(self.window, text="Reward Side").grid(row=0,column=0,sticky=tk.W)
        self.StimLED_R = tk.Label(self.window, text="Right Side", font="Verdana 10",
                                                 borderwidth=3, relief="groove", width=10)
        self.StimLED_R.grid(row=0,column=2,sticky=tk.W)

        self.StimLED_L = tk.Label(self.window, text="Left Side", font="Verdana 10",
                                                 borderwidth=3, relief="groove", width=10)
        self.StimLED_L.grid(row=0,column=1,sticky=tk.W)


        tk.Label(self.window, text="Answer Side").grid(row=1,column=0,sticky=tk.W)
        self.AnswerLED_R = tk.Label(self.window, text="Right Side", font="Verdana 10",
                                                 borderwidth=3, relief="groove", width=10)
        self.AnswerLED_R.grid(row=1,column=2,sticky=tk.W)

        self.AnswerLED_L = tk.Label(self.window, text="Left Side", font="Verdana 10",
                                                 borderwidth=3, relief="groove", width=10)
        self.AnswerLED_L.grid(row=1,column=1,sticky=tk.W)

        #Answer behavior summary
        tk.Label(self.window, text="--------------------------").grid(row=2,column=0,columnspan=2)
        tk.Label(self.window, text="Correct Answers").grid(row=4,column=0,sticky=tk.W)
        tk.Label(self.window, text="Wrong Answers").grid(row=5,column=0,sticky=tk.W)
        
        tk.Label(self.window, text="Left",font="Verdana 7").grid(row=3,column=1)
        tk.Label(self.window, text="Right",font="Verdana 7").grid(row=3,column=2)

        self.Behav_Correct_L = tk.Label(self.window, text="0", font="Verdana 10",bg="#d6f5d6",
                                                 borderwidth=3, relief="groove", width=8)
        self.Behav_Correct_L.grid(row=4,column=1)

        self.Behav_Wrong_L = tk.Label(self.window, text="0", font="Verdana 10",bg="#ff8080",
                                                 borderwidth=3, relief="groove", width=8)
        self.Behav_Wrong_L.grid(row=5,column=1)

        self.Behav_Correct_R = tk.Label(self.window, text="0", font="Verdana 10",bg="#d6f5d6",
                                                 borderwidth=3, relief="groove", width=8)
        self.Behav_Correct_R.grid(row=4,column=2)

        self.Behav_Wrong_R = tk.Label(self.window, text="0", font="Verdana 10",bg="#ff8080",
                                                 borderwidth=3, relief="groove", width=8)
        self.Behav_Wrong_R.grid(row=5,column=2)

        tk.Label(self.window, text="--------------------------").grid(row=6,column=0,columnspan=2)

        self.LAnswer_history = tk.Label(self.window, text="Answer History")
        self.LAnswer_history.grid(row=7,column=0)

        self.lickLEDL = tk.Label(self.window, text="Lick L", font="Verdana 10",bg="#f5f5f5",
                                                 borderwidth=3, relief="groove", width=7,height=2)
        self.lickLEDL.grid(row=11,column=0)
        
        self.lickLEDR = tk.Label(self.window, text="Lick R", font="Verdana 10",bg="#f5f5f5",
                                                 borderwidth=3, relief="groove", width=7,height=2)
        self.lickLEDR.grid(row=11,column=1)
        
        
        self.lickDetection = tk.BooleanVar(self.window)
        self.lickDetection.set(True)
        _cLickDetection = tk.Checkbutton(
                self.window, text="Lick Detection", variable=self.lickDetection)
        _cLickDetection.grid(row=10,column=1)
        
        self.taskEnabled = tk.BooleanVar(self.window)
        self.taskEnabled.set(True)
        c2AFCTask = tk.Checkbutton(
                self.window, text="2AFC Task enabled", variable=self.taskEnabled)
        c2AFCTask.grid(row=10,column=2)
        
        tk.Label(self.window,text="Answer time window [sec]").grid(row=12,column=0)
        self.eAnswerWindow = tk.Entry(self.window,width=10)
        self.eAnswerWindow.grid(row=12,column=1)
        self.eAnswerWindow.insert(0,'2')
        
        tk.Label(self.window,text="Reward time window [sec]").grid(row=13,column=0)
        self.eRewardWindow = tk.Entry(self.window,width=10)
        self.eRewardWindow.grid(row=13,column=1)
        self.eRewardWindow.insert(0,'2')
        

    def update_lick(self, switch, lickSide):
        if switch == True:
            if lickSide=='right':
                self.lickLEDR.config(bg="#86b300")
                self.lickLEDdelay[1] = time.time() + 0.5
            else:
                self.lickLEDL.config(bg="#86b300")      
                self.lickLEDdelay[0] = time.time() + 0.5
                                 
        else:
            if time.time() > self.lickLEDdelay[0]:
                self.lickLEDL.config(bg="#f5f5f5")
            if time.time() > self.lickLEDdelay[1]:                   
                self.lickLEDR.config(bg="#f5f5f5")

    def update_answers(self, target, answer):
        if self.isOpen():
            if target == 'right':
                self.StimLED_R.config(bg="#86b300")
                self.StimLED_L.config(bg="#f5f5f5")                      
            elif target == 'left':
                self.StimLED_L.config(bg="#86b300")
                self.StimLED_R.config(bg="#f5f5f5") 
            else:
                self.StimLED_L.config(bg="#f5f5f5")
                self.StimLED_R.config(bg="#f5f5f5")           
                                      
            if answer == 'right':
                self.AnswerLED_R.config(bg="#86b300")
                self.AnswerLED_L.config(bg="#f5f5f5")                      
            elif answer == 'left':
                self.AnswerLED_L.config(bg="#86b300")
                self.AnswerLED_R.config(bg="#f5f5f5") 
            else:
                self.AnswerLED_L.config(bg="#f5f5f5")
                self.AnswerLED_R.config(bg="#f5f5f5")  



    def update_behavior(self):
        if len(Behavior.answers) > 0:
            answers_in = Behavior.answers
            data = Behavior.calc_behavior(answers_in)
            self.Behav_Correct_L.config(text=str(data[0]))
            self.Behav_Wrong_L.config(text=str(data[2]))
            self.Behav_Correct_R.config(text=str(data[1]))
            self.Behav_Wrong_R.config(text=str(data[3]))
            self.LAnswer_history.config(text=answers_in[-3:])    
            
            
    def isOpen(self):
        """Check if window is open and return state as bool"""
        try:
            if 'normal' == self.window.state():
                return True
            else:
                return False
        except:
            return False               
