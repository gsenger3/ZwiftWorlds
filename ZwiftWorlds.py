# ZwiftWorlds.py
# George Senger
# Simple app (OS X only for now) that allows you to select any world in Zwift and make it
# your home world. Will launch Zwift with the selected world as HOME WORLD
#
# TODO integrate with Zwift API to query active guest worlds and gray out the selection buttons
#  based on active guest worlds.
# TODO Make windows compatible if anyone has interest

import os
import shutil
import xml.etree.ElementTree as ET
import zhw_scraper
import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox

APP_NAME = "ZwiftWorlds"
VERSION = "0.5"
COPYRIGHT = u"\u00A9" + "2022 Primo Studios"

home = os.getenv("HOME")
prefs = home + "/Documents/Zwift/prefs.xml"
prefs_bak = home + "/Documents/Zwift/prefs.xml.bak"
ZWIFT = "/Applications/Zwift.app"
WORLDS = []

class ZwiftWorlds:
    def __init__(self, root):
        # setting title
        root.title("Zwift Worlds")

        # setting window size and properties
        width = 865
        height = 775
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root["bg"] = "white"
        root.resizable(width=False, height=False)

        # basic menubar to just quit the app and show version
        menubar = tk.Menu(root)
        # Mac application menu
        app_menu = tk.Menu(menubar, name='apple', tearoff=0)
        app_menu.add_command(label='About ZwiftWorlds', command=self.show_about_dialog)
        menubar.add_cascade(menu=app_menu)
        # file menu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Restore Prefs.xml", command=self.restore_prefs)
        filemenu.entryconfig("Restore Prefs.xml")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        root.config(menu=menubar)

        # Zwift Worlds banner
        zw_label = tk.Label(root, font=("Arial", 53))
        zw_label["justify"] = "center"
        zw_label["text"] = "Zwift Worlds"
        zw_label.place(x=20, y=20, width=865, height=48)

        # Footer
        self.status_label = tk.Label(root, font=("Arial", 12))
        self.status_label["text"] = ""
        self.status_label.place(x=15, y=750, width=200, height=12)

        foot_label = tk.Label(root, font=("Arial", 12))
        foot_label["justify"] = "center"
        #copyright = u"\u00A9"
        foot_label["text"] = COPYRIGHT
        foot_label.place(x=375, y=750, width=150, height=12)

        v_label = tk.Label(root, font=("Arial", 12))
        #v_label["font"] = foot_font
        v_label["text"] = VERSION
        v_label.place(x=810, y=750, width=30, height=12)

        # build the button interface
        self.france_gif = tk.PhotoImage(file='img/france.gif')
        france_button = tk.Button(root, image=self.france_gif)
        france_button.place(x=20, y=100, width=163, height=200)
        #france_button["command"] = self.france_button_command
        if self.is_active_world("France") == False:
            france_button["command"] = self.france_button_command
        else:
            france_button["state"] = "disabled"

        self.inns_gif = tk.PhotoImage(file='img/innsbruck.gif')
        inns_button = tk.Button(root, image=self.inns_gif)
        inns_button.place(x=240, y=100, width=163, height=200)
        #inns_button["command"] = self.inns_button_command
        if self.is_active_world("Innsbruck") == False:
            inns_button["command"] = self.inns_button_command
        else:
            inns_button["state"] = "disabled"

        self.london_gif = tk.PhotoImage(file='img/london.gif')
        london_button = tk.Button(root, image=self.london_gif)
        london_button.place(x=460, y=100, width=163, height=200)
        #london_button["command"] = self.london_button_command
        if self.is_active_world("London") == False:
            london_button["command"] = self.london_button_command
        else:
            london_button["state"] = "disabled"

        self.makuri_gif = tk.PhotoImage(file='img/makuri.gif')
        makuri_button = tk.Button(root, image=self.makuri_gif)
        makuri_button.place(x=680, y=100, width=163, height=200)
        #makuri_button["command"] = self.makuri_button_command
        if self.is_active_world("Makuri Islands") == False:
            makuri_button["command"] = self.makuri_button_command
        else:
            makuri_button["state"] = "disabled"

        self.ny_gif = tk.PhotoImage(file='img/ny.gif')
        ny_button = tk.Button(root, image=self.ny_gif)
        ny_button.place(x=120, y=320, width=163, height=200)
        #ny_button["command"] = self.ny_button_command
        if self.is_active_world("New York") == False:
            ny_button["command"] = self.ny_button_command
        else:
            ny_button["state"] = "disabled"

        self.paris_gif = tk.PhotoImage(file='img/paris.gif')
        paris_button=tk.Button(root, image=self.paris_gif)
        paris_button.place(x=360,y=320,width=163,height=200)
        #paris_button["command"] = self.paris_button_command
        if self.is_active_world("Paris") == False:
            paris_button["command"] = self.paris_button_command
        else:
            paris_button["state"] = "disabled"

        self.richmond_gif = tk.PhotoImage(file='img/richmond.gif')
        richmond_button=tk.Button(root, image=self.richmond_gif)
        richmond_button.place(x=590,y=320,width=163,height=200)
        if self.is_active_world("Richmond") == False:
            richmond_button["command"] = self.richmond_button_command
        else:
            richmond_button["state"] = "disabled"

        self.watopia_gif = tk.PhotoImage(file='img/watopia.gif')
        watopia_button=tk.Button(root, image=self.watopia_gif)
        watopia_button.place(x=240,y=540,width=163,height=200)
        watopia_button["command"] = self.watopia_button_command

        self.york_gif = tk.PhotoImage(file='img/yorkshire.gif')
        york_button=tk.Button(root, image=self.york_gif)
        york_button.place(x=490,y=540,width=163,height=200)
        #york_button["command"] = self.york_button_command
        if self.is_active_world("Yorkshire") == False:
            york_button["command"] = self.york_button_command
        else:
            york_button["state"] = "disabled"

    # button command handlers (on click)
    def show_about_dialog(self):
        tk_version = root.tk.call('info', 'patchlevel')
        tk.messagebox.showinfo(title="About ZwiftWorlds", message=APP_NAME + "\n" + "Version: " + VERSION + "\n\n" +
                                    "Tk Version: " + tk_version + "\n\n" +
                                    COPYRIGHT)
    
    def france_button_command(self):
        print("SELECTION: france")
        self.set_world_in_prefs(10)
        self.launchZwift()

    def inns_button_command(self):
        print("SELECTION: innsbruck")
        self.set_world_in_prefs(5)
        self.launchZwift()

    def london_button_command(self):
        print("SELECTION: london")
        self.set_world_in_prefs(3)
        self.launchZwift()

    def makuri_button_command(self):
        print("SELECTION: makuri islands")
        self.set_world_in_prefs(9)
        self.launchZwift()

    def ny_button_command(self):
        print("SELECTION: new york")
        self.set_world_in_prefs(4)
        self.launchZwift()

    def paris_button_command(self):
        print("SELECTION: paris")
        self.set_world_in_prefs(11)
        self.launchZwift()

    def richmond_button_command(self):
        print("SELECTION: richmond")
        self.set_world_in_prefs(2)
        self.launchZwift()

    def watopia_button_command(self):
        print("SELECTION: watopia")
        self.set_world_in_prefs(1)
        self.launchZwift()

    def york_button_command(self):
        print("SELECTION: yorkshire")
        self.set_world_in_prefs(7)
        self.launchZwift()

    # update WORLD in prefs.xml with selected world
    def set_world_in_prefs(self, world):
        tree = ET.parse(prefs)
        root = tree.getroot()

        # clean worlds
        worlds = root.findall("WORLD")
        for w in worlds:
            root.remove(w)

        # insert selected world and write out prefs.xml
        ET.SubElement(root, 'WORLD').text = str(world)
        tree.write(prefs)

    # backup the prefs.xml file before continuing
    def backup_prefs(self):
        if os.path.exists(prefs_bak) == False: # check to see if the prefs.xml is already backed up
            try:
                # not backed up, so let's back it up
                shutil.copy(prefs, prefs_bak)
                print("prefs.xml successfully backed up.")
                self.status_label["text"] = "prefs.xml successfully backed up."
            except:
                print("Error occurred while copying file.")
                e = sys.exc_info()[0]
                print(e)
                self.status_label["text"] = "Error occurred while copying file."
        else:
            # prefs.xml already backed up so we don't need to do anything since we only keeping 1 original backup
            print("We're good... prefs.xml already backed up!")
            self.status_label["text"] = "prefs.xml successfully backed up."

    # restore the saved backup prefs.xml
    def restore_prefs(self):
        if os.path.exists(prefs_bak) == True: # check to see if we have a backup of prefs.xml
            try:
                # we have one so lets try to restore it
                shutil.copy(prefs_bak, prefs)
                print("prefs.xml successfully restored.")
                tk.messagebox.showinfo(title="Status",
                                       message="prefs.xml successfully restored.")
            except:
                print("Error occurred while copying file.")
                tk.messagebox.showinfo(title="Status",
                                       message="Error occured while restoring prefs.xml")
        else:
            # sorry, backup doesn't exist, can't restore it
            print("Backup prefs.xml doesn't exist!")
            tk.messagebox.showinfo(title="Status",
                                   message="Backup prefs.xml doesn't exist!")

    # world_exists
    def is_active_world(self, w):
        try:
            return WORLDS.__contains__(w)
        except:
            return False

    # launch Zwift
    def launchZwift(self):
        exit_code = os.system("open " + ZWIFT) # launch Zwift

        if os.WEXITSTATUS(exit_code) == 0: # good launch, we can quit this app
            root.quit()
        else: # oops, alert user that we had issues launching Zwift
            print("Error occurred while launching Zwift!\nError Code: " + str(exit_code))
            tk.messagebox.showinfo(title="Error",
                                   message="Error occurred while launching Zwift!\n\nError Code: " + str(exit_code))


if __name__ == "__main__":
    WORLDS = zhw_scraper.get_worlds()
    root = tk.Tk()
    app = ZwiftWorlds(root)
    app.backup_prefs() #backup the prefs.xml
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    root.mainloop()
