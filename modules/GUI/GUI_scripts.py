# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 11:28:06 2019

@author: bexter
"""

import tkinter as tk
from tkinter import filedialog
from os import path, getcwd
import importlib.util


def pre_import_module(function_path, function_name='run'):
    spec = importlib.util.spec_from_file_location(function_name, function_path)
    function_handle = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(function_handle)
    print('Imported')

    return function_handle
#


class DeleteButton:
    def __init__(self, parent, window):
        self.parent = parent
        self.object = tk.Button(window, text='-', command=self.delete)
        self.object.grid(row=len(GUIScripts.scripts), column=2, sticky=tk.W)

    def delete(self):
        # This should never actually do anything, but just to make sure
        for i in range(len(self.parent.scripts)):
            GUIScripts.scripts[i]['label'].grid_configure({'row': i + 1})
            GUIScripts.scripts[i]['optMenu'].grid_configure({'row': i + 1})
            GUIScripts.scripts[i]['delete_button'].object.grid_configure({'row': i + 1})
        #

        # I'm not happy with getting the list_ids from the grid, but I couldn't come up with something better for now
        list_id = self.object.grid_info()['row'] - 1

        related_objects = GUIScripts.scripts[list_id]
        related_objects['label'].destroy()
        related_objects['optMenu'].destroy()
        related_objects['delete_button'].object.destroy()
        self.parent.window.update()

        # now remove from list
        GUIScripts.scripts.pop(list_id)

        # update grid
        for i in range(len(GUIScripts.scripts)):
            GUIScripts.scripts[i]['label'].grid_configure({'row': i + 1})
            GUIScripts.scripts[i]['optMenu'].grid_configure({'row': i + 1})
            GUIScripts.scripts[i]['delete_button'].object.grid_configure({'row': i + 1})
        #
    #
#


class GUIScripts:
    """
    Class for the window for handling scripts on triggers
    """

    def __init__(self, config):
        self.mmconfig = config
        self.config_section_name = 'script_settings'
        # I can't cause Alex uses them outside like this:/
        # self.scripts = []  # I'm trying to make this a member of the class
        GUIScripts.scripts = []
        self.window = None
        self.triggerOpt = None
        self.already_initialized = False
    #

    def on_close(self):
        print('Script settings saved')
        self.save_config()
        self.window.quit()
        self.window.destroy()
    #

    def openWindow(self):
        self.window = tk.Tk()
        self.window.title("Scripts")
        # the Menus don't call the function, maybe no active updates? This is my workaround for that
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.triggerOpt = ("None", "Start of Answer Period",
                           "End of Answer Period", "On Reward", "On Error",
                           "On Missed", "Start of Trial")
        
        # Create new scripts
        tk.Button(
            self.window, text="Add Script", compound=tk.RIGHT,
            anchor="w", command=lambda: self.new_script(),
            justify="left").grid(row=0, column=0, sticky=tk.W)
        #

        if self.already_initialized:
            self.rebuild_gui()
        else:
            # I don't want to reimport everything again
            self.load_config()
        #
    #

    def new_script(self, file_name=None, trigger='None', pre_import=True):
        if file_name is None:
            file_name = filedialog.askopenfilename(initialdir=path.join(getcwd(), 'user_functions'),
                                                   multiple=False,
                                                   title="Choose a script file")
        #
        self.window.lift()

        if (file_name is not None) and file_name != [] and file_name != '':
            script = {'path': file_name}

            if pre_import and file_name.endswith('.py'):
                temp_label = tk.Label(self.window, text='Importing function ...')
                temp_label.grid(row=0, column=1, sticky=tk.W, columnspan=2)
                temp_label.update()

                function_handle = pre_import_module(function_path=file_name, function_name='run')
                script['function_handle'] = function_handle

                temp_label.destroy()
            #

            GUIScripts.scripts.append(script)

            # print('New scrip with script length: %d' % (len(self.scripts)))

            GUIScripts.scripts[-1]['trigger'] = tk.StringVar(self.window)
            GUIScripts.scripts[-1]['trigger'].set(trigger)

            GUIScripts.scripts[-1]['label'] = tk.Label(self.window, text=file_name)
            GUIScripts.scripts[-1]['label'].grid(row=len(GUIScripts.scripts), column=0, sticky=tk.W)

            GUIScripts.scripts[-1]['optMenu'] = tk.OptionMenu(
                self.window, self.scripts[-1]['trigger'], *self.triggerOpt)  # , command=self.saveConfig()
            GUIScripts.scripts[-1]['optMenu'].grid(row=len(GUIScripts.scripts), column=1, sticky=tk.W)

            GUIScripts.scripts[-1]['delete_button'] = DeleteButton(parent=self, window=self.window)
        #
    #

    def rebuild_gui(self):
        scripts_to_rebuild = GUIScripts.scripts
        GUIScripts.scripts = []
        for n, script in enumerate(scripts_to_rebuild):
            self.new_script(file_name=script['path'], trigger=script['trigger'].get(), pre_import=False)
        del scripts_to_rebuild
    #

    def executeScript(script):
        print('Execute: %s' % (script['path'],))
        if script['path'].endswith('.py'):
            script['function_handle'].run()
            # with open(script['path'], "r") as file:
            #     exec(file.read())
            # file.close()
        else:
            try:
                import os
                os.startfile(script['path'])
            except Exception as e:
                raise e
                # print("WARNING: could not execute script")
    #

    def save_config(self):
        # It's not efficient and ugly but I want to make sure I don't have Scripts artifacts in here :/
        if self.config_section_name in self.mmconfig.winConfig.sections():
            self.mmconfig.winConfig.remove_section(self.config_section_name)
        #
        self.mmconfig.winConfig.add_section(self.config_section_name)

        n_scripts = len(GUIScripts.scripts)
        self.mmconfig.set_value(self.config_section_name, 'n_scripts', str(n_scripts))
        for script_id in range(n_scripts):
            # print([self.scripts[script_id]['path'], self.scripts[script_id]['trigger'].get()])
            self.mmconfig.set_value(self.config_section_name, 'script_path_'+str(script_id),
                                    GUIScripts.scripts[script_id]['path'])
            self.mmconfig.set_value(self.config_section_name, 'script_trigger_'+str(script_id),
                                    GUIScripts.scripts[script_id]['trigger'].get())
        #
    #

    def load_config(self):
        try:
            if self.config_section_name in self.mmconfig.winConfig.sections():  # Only try to load if the section exists
                n_scripts = int(self.mmconfig.get(self.config_section_name, 'n_scripts'))
                if len(GUIScripts.scripts) > 0:
                    raise Exception('Trying to load scripts over existing ones! This should never occur.')
                else:
                    GUIScripts.scripts = []  # This is redundant, just for testing!!!
                #

                for script_id in range(n_scripts):
                    file_name = self.mmconfig.get(self.config_section_name, 'script_path_' + str(script_id))
                    trigger = self.mmconfig.get(self.config_section_name, 'script_trigger_' + str(script_id))
                    self.new_script(file_name=file_name, trigger=trigger)
                #
            #
        except Exception as e:
            print(e)
            print('Unable to load script settings! Please reenter your scripts.')
            self.mmconfig.winConfig.remove_section(self.config_section_name)
        #
        self.already_initialized = True
    #
#
