#############################################################################
# Author     : Anantharaman Chandar                                         #
# CWID       : A20403439                                                    #
# Course     : ITMD 513 Open Source Programming Final Project               #
# Instructor : James Papademas                                              #
# Description: This script gives you the options to select which            #
#              chart do you want to visualize                               #
#                                                                           #                      
#                                                                           #
#                                                                           #
#############################################################################

#Import libraries
import sys,time,io,os,tkinter.messagebox

## Import specific modules from Libraries
from tkinter import *


##Import other files
import BasedOnAge as Age
import Nationality as Nat
import PersonalDetails as PD
import Compare_Two_Teams as CTT
import Generate_Report as GR
import Best_Team as BT
import Players_Compare as PC
import DB_Objects as DB
import WC as WordCloudD


#GUI Formation Function   
def buildFrame () :
    Val_1="Opening Menu Options"
    DB.InsertLogs(Val_1)
    global select,root, nameVar, mobVar
    #Build Frame
    root=Tk()
    root.title("Player Stats")
    root.resizable(width=FALSE, height=FALSE)
    root.geometry('1000x650')

    GUIFrame = Frame(root)
    GUIFrame.grid(row=20,column=20)
    

    #Header
    Heading = Label(GUIFrame, text = "Welcome To FIFA 18 Player Stats").grid(row=1, column=3)  
    Heading1 = Label(GUIFrame, text = "Stats").grid(row=2, column=3)
   
    #Add Button
    AgeLabel = Label(GUIFrame, text="Get Players Based on Age").grid(row=4,column=0,sticky=W)
    AgeButton = Button(GUIFrame, text = "Get ", width=6,command=Age.PlayersBasedOnAge).grid(row=4,column=1)

    #Country Button
    CountryLabel = Label(GUIFrame, text="Get Count of Nationality").grid(row=7,column=0,sticky=W)
    CountryButton = Button(GUIFrame, text = "Get ", width=6,command=Nat.buildFrame).grid(row=7,column=1)

    #Personal Button
    PersonalLabel = Label(GUIFrame, text="Get To Know About a Player").grid(row=8,column=0,sticky=W)
    PersonalButton = Button(GUIFrame, text = "Get ", width=6,command=PD.buildFrame).grid(row=8,column=1)

    #Compare Team Button
    CompareLabel = Label(GUIFrame, text="Compare Two Teams").grid(row=9,column=0,sticky=W)
    CompareButton = Button(GUIFrame, text = "Get ", width=6,command=CTT.buildFrame).grid(row=9,column=1)
    
    #Generate Report
    ReportLabel = Label(GUIFrame, text="Generate Report").grid(row=10,column=0,sticky=W)
    ReportButton = Button(GUIFrame, text = "Get ", width=6,command=GR.buildFrame).grid(row=10,column=1)

    #Pick Team Report
    TeamLabel = Label(GUIFrame, text="Generate Best Team Report").grid(row=11,column=0,sticky=W)
    TeamButton = Button(GUIFrame, text = "Get ", width=6,command=BT.buildFrame).grid(row=11,column=1)

    #Compare Players Report
    PlayerLabel = Label(GUIFrame, text="Compare Players Potential").grid(row=12,column=0,sticky=W)
    PlayerButton = Button(GUIFrame, text = "Get ", width=6,command=PC.buildFrame).grid(row=12,column=1)
    
    #Generate Word Cloud 
    PlayerLabel = Label(GUIFrame, text="Generate Word Cloud").grid(row=13,column=0,sticky=W)
    PlayerButton = Button(GUIFrame, text = "Get ", width=6,command=WordCloudD.GenerateExceptionFile).grid(row=13,column=1)
    
    #root.mainloop()
    return GUIFrame

#buildFrame()
#root.mainloop()
