import tkinter 

class GUITopMenu():
    def __init__(self, root, data, GUI, GUIFlash, GUIconf, GUIBehavior, 
                 GUIRules, GUIMazeConfig, GUISettings, GUIScripts ,Maze, rules):

        def openWindow(windowObj, *param):
            if not self.isOpen(windowObj):
                if param != ():
                    windowObj.openWindow(*param)
                else:
                    windowObj.openWindow()
        def showHelp():
            import webbrowser
            webbrowser.open('doc.pdf')
                       
        menubar = tkinter.Menu(root)

        # create pulldown menus, and add them to the menu bar

        #file
        filemenu = tkinter.Menu(menubar, tearoff=0)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=lambda: GUI.quitMM(data))
        menubar.add_cascade(label="File", menu=filemenu)

        #view
        viewmenu = tkinter.Menu(menubar, tearoff=0)
        viewmenu.add_command(label="Reset Window Positions", 
                        command=lambda: GUI.resetWindows( (root,Maze.window)))
        viewmenu.add_command(label="Save Window Positions", 
                        command=lambda: GUI.saveWindows( (root,Maze.window)))
        menubar.add_cascade(label="View", menu=viewmenu)

        #windows
        windowsmenu = tkinter.Menu(menubar, tearoff=0)
        windowsmenu.add_command(label="Tunnel Flashes", 
                                command = lambda: openWindow(GUIFlash, Maze))
        windowsmenu.add_command(label="Behavior", 
                                command = lambda: openWindow(GUIBehavior))
        windowsmenu.add_command(label="Input Devices", 
                                command = lambda: openWindow(GUIconf))
        windowsmenu.add_command(label="Maze Settings", 
                                command = lambda: openWindow(GUIMazeConfig))
        windowsmenu.add_command(label="Rules", 
                                command = lambda: openWindow(GUIRules, Maze, 
                                                             rules))
        windowsmenu.add_command(label="Scripts", 
                                command = lambda: openWindow(GUIScripts))
        
        windowsmenu.add_command(label="Settings", 
                                command = lambda: openWindow(GUISettings))
        menubar.add_cascade(label="Windows", menu=windowsmenu)

        #help
        helpmenu = tkinter.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=showHelp)
        menubar.add_cascade(label="Help", menu=helpmenu)

        # display the menu
        root.config(menu=menubar)
        
    def isOpen(self, window):
        try:
            if 'normal' == window.window.state():
                return True
            else:
                return False
        except:
            return False

    def closeAll(self, windows):        
        for window in windows:
            if self.isOpen(window):
                window.window.destroy()
