import tkinter
import rawinputreader as rr
from tkinter import messagebox as mbox

'''
there are self.mmconfig in GUI, GUI_maz_config and here
SetMouse1Button, SetMouse2Button also in GUI

still as GUI-variables used...in:

'''

class Configure():
    def __init__(self, config, GUI):
        self.mmconfig = config
        self.wheel_conf = False
        self.GUI = GUI
        
    def GetSensorID(self):
        # set sensor input
        if self.rir is None:
            print("No Module rawinputreader found")
            self.rir = rr.rawinputreader() 
        NoTrial = 0
        SensorID = 0
        p = 0
        self.rir.empty_events()
        print("Search for Sensors ...", end='')
        while NoTrial < 10:
            p = p+1
            Output = self.rir.pollEvents() #mdebug
            print(Output)
            #print(Output)
            if Output != []:
                if SensorID == Output[-1][0]:
                    NoTrial = NoTrial+1
                else:
                    SensorID = Output[-1][0]
                    #NoTrial = 0
            if p % 1000 == 0:
                print(".", end='')
            if p > 500000:
                print(".")
                break
        print("getSensorID")
        if int(SensorID) != 0:
            print("Found Sensor with ID: ", SensorID)
        else:
            print("No Sensor found")
        #self.rir.stop()
        return int(SensorID)
        
    def set_ball_pos_sensor_color(self, sensor_ID):
        if sensor_ID == 0: 
            return "#dd867c"
        else:
            return "#f5f5f5"
            
    def set_ball_pos_sensor(self, sensorEntry):
        sensorEntry.config(state='normal')
        sensor_ID = self.GetSensorID()
        sensorEntry.delete(0, tkinter.END)
        sensorEntry.insert(0, str(sensor_ID))
        sensorEntry.config(text=str(sensor_ID), state='readonly')
        sensorEntry.config(
            readonlybackground=self.set_ball_pos_sensor_color(sensor_ID))
        print("set_ball_pos_sensor") #mdebug
        return sensor_ID
        
    def update_window(self):
        '''
        make widgets to configure the wheel encoder visible or disappear
        '''
        if self.tracking_device.get() == 'Wheel' and self.wheel_conf == False:
            self.wheel_conf = True
           
            self.lEncoder_Type.grid(row=1,column=0)
            self.rEncoderType_360.grid(row=1,column=1)
            self.lEncoderPos.grid(row=2,column=0)
            self.rEncoderPos_left.grid(row=2,column=1)
            self.rEncoderPos_right.grid(row=2,column=2)
            self.rEncoderType_1024.grid(row=1,column=2)
            
            self.eSensor1.grid_remove()
            self.SetMouse1Button.grid_remove()
            self.eSensor2.grid_remove()
            self.SetMouse2Button.grid_remove()
           
            
            print("update_window_wheel") #mdebug
            self.loadConfig()
        elif self.tracking_device.get() != 'Wheel' and self.wheel_conf == True:
            print(self.tracking_device.get()) #mdebug

            self.wheel_conf = False
            print("update_window no wheel") #mdebug
            self.lEncoder_Type.grid_remove()
            self.rEncoderType_360.grid_remove()
            self.lEncoderPos.grid_remove()
            self.rEncoderPos_left.grid_remove()
            self.rEncoderPos_right.grid_remove()
            self.rEncoderType_1024.grid_remove()
            self.eSensor1.grid(row=4,column=0) 
            self.SetMouse1Button.grid(row=4,column=1)
            self.eSensor2.grid(row=5,column=0)
            self.SetMouse2Button.grid(row=5,column=1)
            self.loadConfig()

        else:
            print("update window else") #mdebug
            pass


    def openWindow(self):  
        """Create and open the window"""
        self.window = tkinter.Tk()
        self.window.title("Configure")

        #Number of ticks per round of wheel
        self.encoderType = tkinter.StringVar(self.window)
        self.encoderType.set('360')

        self.tracking_device = tkinter.StringVar(self.window)
        
        tkinter.OptionMenu(
            self.window, 
            self.tracking_device, 
            *['Wheel','Ball'], 
            command=lambda x:self.update_window()
            ).grid(row=0, column=0, padx=(10, 0), pady=(10, 0))
      
        self.lEncoder_Type = tkinter.Label(
            self.window,
            text="Wheel Encoder Type (Ticks/Round)")
        self.rEncoderType_360 = tkinter.Radiobutton(
            self.window, 
            text="360", variable=self.encoderType, value='360')  
        
        self.rEncoderType_1024 = tkinter.Radiobutton(
            self.window, 
            text="1024", variable=self.encoderType, value='1024')  

        #Position of wheel encoder
        self.encoderPos = tkinter.StringVar(self.window)
        self.encoderPos.set('left')
        
        self.lEncoderPos = tkinter.Label(
            self.window,
            text="Position of Encoder)")
        self.rEncoderPos_left = tkinter.Radiobutton(
            self.window, 
            text="left", variable=self.encoderPos, value='left')  
        
        self.rEncoderPos_right = tkinter.Radiobutton(
            self.window, 
            text="right", variable=self.encoderPos, value='right')  
        

        #Set ball position sensors
        self.rir = rr.rawinputreader()
        print("open_wiiindow_configure") #mdebug
        self.eSensor1 = tkinter.Entry(
            self.window, 
            insertofftime=0, relief=tkinter.FLAT, width=10) 
        self.SetMouse1Button = tkinter.Button(
            self.window, 
            text="set",command=lambda:self.set_ball_pos_sensor(self.eSensor1))

        self.eSensor2 = tkinter.Entry(
            self.window, 
            insertofftime=0, relief=tkinter.FLAT, width=10)
        self.SetMouse2Button = tkinter.Button(
            self.window, text="set",
            command=lambda:self.set_ball_pos_sensor(self.eSensor2))

        #Save button
        SaveButton = tkinter.Button(
            self.window, 
            text = "Save", command = self.saveConfig)
        SaveButton.grid(row=11,column=5, padx=(0, 10), pady=(0,10))
        
        if self.mmconfig.get('conf', 'useWheel') == 'True' or \
        self.mmconfig.get('conf', 'useWheel'):
            self.tracking_device.set('Wheel')
            self.update_window()
        elif self.mmconfig.get('conf', 'useBall') == 'True' or \
        self.mmconfig.get('conf', 'useBall'):  
            self.tracking_device.set('Ball')
            self.update_window()
        else:
            self.tracking_device.set('use tracking device...')

        if self.mmconfig.get('conf', 'useWheel') == 'True':
            self.tracking_device.set('Wheel')
            print("usewheelconf")
        elif self.mmconfig.get('conf', 'useBall') == 'True':
            self.tracking_device.set('Ball')
            print("useballconf")
            
            
        self.update_window()
                
    def saveConfig(self):
        print("saves")
        """Saves the values in the config file and closes the window"""
        self.mmconfig.set_value('conf', 'EncoderType', self.encoderType.get())
        self.mmconfig.set_value('conf', 'EncoderPos', self.encoderPos.get())
        self.mmconfig.set_value('conf', 'mouseid1', self.eSensor1.get())
        self.mmconfig.set_value('conf', 'mouseid2', self.eSensor2.get())

        exit = False
        if (self.mmconfig.get('conf', 'useBall') == 'True' and self.tracking_device.get() == 'Wheel') or \
            (self.mmconfig.get('conf', 'useWheel') == 'True' and self.tracking_device.get() == 'Ball'):
            if mbox.askokcancel("Quit", "Input Device has been changed, Maze Master need to restart. Do you want to quit now?"):
                exit=True

        self.mmconfig.set_value(
            'conf', 'useWheel', 
            str(self.tracking_device.get() == 'Wheel'))
        self.mmconfig.set_value(
            'conf', 'useBall', 
            str(self.tracking_device.get() == 'Ball'))
        self.window.destroy()
        
        if exit:
            self.GUI.Exit = True
    def loadConfig(self):
        print("loads")
        """Loads the values from the config file and fill them in"""
        
        self.encoderType.set(self.mmconfig.get('conf', 'EncoderType'))
        self.encoderPos.set(self.mmconfig.get('conf', 'EncoderPos'))
        self.eSensor1.insert(0, self.mmconfig.get('conf', 'mouseid1'))
        self.eSensor1.config(
                state='readonly', 
                readonlybackground = self.set_ball_pos_sensor_color(
                    int(self.mmconfig.get('conf', 'mouseid1'))))
        self.eSensor2.insert(0, self.mmconfig.get('conf', 'mouseid2'))
        self.eSensor2.config(
                state='readonly', 
                readonlybackground = self.set_ball_pos_sensor_color(
                    int(self.mmconfig.get('conf', 'mouseid2'))))

        """
        if self.mmconfig.get('conf', 'useWheel') == 'True':
            self.tracking_device.set('Wheel')
            print("usewheelconf")
        elif self.mmconfig.get('conf', 'useBall') == 'True':
            self.tracking_device.set('Ball')
            print("useballconf")
        """
