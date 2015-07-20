#!/usr/bin/env python
# -*- coding: utf8 -*-

from Tkinter import *
#from Tkinter import Tk,Frame,Label,Entry,Radiobutton,Button,StringVar,ANCHOR

class TkinterGameSetupParams:

    def __init__(self):
        self.root = Tk()
        self.root.title("Welcome to Python Chess!")
        self.frame = Frame(self.root)
        self.frame.pack()

        self.instructionMessage = StringVar()
        Label(self.frame, textvariable=self.instructionMessage).grid(row=0)
        self.instructionMessage.set("Please enter game options.")

        Label(self.frame, text="Name").grid(row=1,column=1)
        Label(self.frame, text="Type").grid(row=1,column=2)

        Label(self.frame, text="Player 1 (White)").grid(row=2,column=0)
        self.entry_player1Name = Entry(self.frame)
        self.entry_player1Name.grid(row=2,column=1)
        self.entry_player1Name.insert(ANCHOR,"Human")

        self.tk_player1Type = StringVar()
        Radiobutton(self.frame, text="Human",variable=self.tk_player1Type,value="human").grid(row=2,column=2)
        Radiobutton(self.frame, text="AI",variable=self.tk_player1Type,value="AI").grid(row=2,column=3)
        self.tk_player1Type.set("human")


        Label(self.frame, text="Player 2 (Black)").grid(row=3,column=0)
        self.entry_player2Name = Entry(self.frame)
        self.entry_player2Name.grid(row=3,column=1)
        self.entry_player2Name.insert(ANCHOR,"AI")

        self.tk_player2Type = StringVar()
        Radiobutton(self.frame, text="Human",variable=self.tk_player2Type,value="human").grid(row=3,column=2)
        Radiobutton(self.frame, text="AI",variable=self.tk_player2Type,value="AI").grid(row=3,column=3)
        self.tk_player2Type.set("AI")


        b = Button(self.frame, text="Start the Game!", command=self.ok)
        b.grid(row=4,column=1)

    def ok(self):
        self.player1Name = self.entry_player1Name.get()
        #hardcoded so that player 1 is always white
        self.player1Color = "w"
        self.player1Type = self.tk_player1Type.get()
        self.player2Name = self.entry_player2Name.get()
        self.player2Color = "b"
        self.player2Type = self.tk_player2Type.get()

        if self.player1Name != "" and self.player2Name != "":
            self.frame.destroy()
        else:
            #self.instructionMessage.set("Please input a name for both players!")
            if self.player1Name == "":
                self.entry_player1Name.insert(ANCHOR,"Kasparov")
            if self.player2Name == "":
                self.entry_player2Name.insert(ANCHOR,"Light Blue")

    def GetGameSetupParams(self):
        self.root.wait_window(self.frame) #waits for frame to be destroyed
        self.root.destroy() #noticed that with "text" gui mode, the tk window stayed...this gets rid of it.
        return (self.player1Name, self.player1Color, self.player1Type,
                self.player2Name, self.player2Color, self.player2Type)



if __name__ == "__main__":		

    d = TkinterGameSetupParams()
    x = d.GetGameSetupParams()
    print x
