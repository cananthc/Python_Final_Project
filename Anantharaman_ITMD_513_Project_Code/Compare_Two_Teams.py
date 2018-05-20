#############################################################################
# Author     : Anantharaman Chandar                                         #
# CWID       : A20403439                                                    #
# Course     : ITMD 513 Open Source Programming Final Project               #
# Instructor : James Papademas                                              #
# Description: This script compares two selected teams and creats a         #
#              box plot                                                     #
#                                                                           #                      
#                                                                           #
#                                                                           #
#############################################################################

#Import necessary Libraries
import sys,time,io,os,tkinter.messagebox
import matplotlib.pyplot as plt
import numpy as np

#Import specific modules from the libraries
from tkinter import *

#Import other Python files
import DB_Objects as DB
import Extract_Records as ER


#Declare necessary variables
Distinct_Club=[]
Distinct_Club_Final=[]
Players_Data=[]
Gen_Values=[]
Gen_Values_1=[]
global teamName2,teamName1
Team_1=[]
Team_2=[]
    


#GUI Formation Function   
def buildFrame () :
    Val_1="Opening Compare Two Teams Menu"
    DB.InsertLogs(Val_1)
    
    global select,root, Teamname1Var, Teamname2Var, Team1,Team2,AddTeam1Button,AddTeam2Button
    print("Start")
    #Build Frame
    root=Tk()
    root.title("Country Stats")
    root.resizable(width=FALSE, height=FALSE)
    root.geometry('1000x650')
    

    GUIFrame = Frame(root)
    GUIFrame.grid(row=20,column=20)

      #Team1
    Team1Label = Label(GUIFrame, text = "Team_1 Selected").grid(row=12, column=3)
    Teamname1Var = StringVar(GUIFrame)
    Team1 = Entry(GUIFrame, textvariable=Teamname1Var).grid(row=12, column=4, sticky=E)

    #Team2
    Team1Label = Label(GUIFrame, text = "Team_2 Selected").grid(row=13, column=3)
    Teamname2Var = StringVar(GUIFrame)
    Team2 = Entry(GUIFrame, textvariable=Teamname2Var).grid(row=13, column=4, sticky=E)
    



    DisplayCountryLabel = Label(GUIFrame, text="Below are the available Teams").grid(row=11,column=0)
    scroll = Scrollbar(GUIFrame, orient=VERTICAL)
    select = Listbox(GUIFrame, yscrollcommand=scroll.set, height=25)
    scroll.config (command=select.yview)
    select.grid(row=12,column=0)
    
    #Header
    Heading = Label(GUIFrame, text = "Welcome To FIFA 18 Player Stats Club Stats").grid(row=1, column=3)  
    AddTeam1Button = Button(GUIFrame, text="Add Team_1",command=LoadTeam1).grid(row=12, column=2)
    AddTeam2Button = Button(GUIFrame, text="Add Team_2",command=LoadTeam2).grid(row=13, column=2)
    
    RemoveTeam1Button = Button(GUIFrame, text="Clear Team_1",command=lambda: clearTeam(1)).grid(row=12, column=6,padx=30)
    RemoveTeam2Button = Button(GUIFrame, text="Clear Team_2",command=lambda: clearTeam(2)).grid(row=13, column=6,padx=10)


    GenerateButton = Button(GUIFrame, text="Generate",command=lambda: PopulateData(Teamname1Var.get(),Teamname2Var.get())).grid(row=26, column=4,pady=30)


    Distinct_Club_Final = GenerateClubs()
    setList(Distinct_Club_Final)
    
    
    root.mainloop()
    return GUIFrame


#Generate Clubs from the list 
def GenerateClubs():
    try:
            
        Val_1="Fetching Records from the list"
        DB.InsertLogs(Val_1)
        
        Players_Data=ER.extractRecords()
        for i in range(0,len(Players_Data)):
            Distinct_Club.append(Players_Data[i][8])

        
        Val_1="Fetching Records from the list completed"
        DB.InsertLogs(Val_1)

        #Delete Duplicates
        Distinct_Club_Final=set(Distinct_Club)
        print(len(Distinct_Club_Final))
        Distinct_Club_Final=list(sorted(Distinct_Club_Final))

        #Remove Null Value
        del Distinct_Club_Final[0]
        
        Val_1="Returning Distinct Club Values"
        DB.InsertLogs(Val_1)

        return Distinct_Club_Final
    except Exception as e:
        DB.InsertExceptionStmtTable(e,"Compare Two Teams - GenerateClubs")
       
    
    
#Inset Distinct Clubs into listbox    
def setList (Distinct_Club_Final):
    try:
        Val_1="Insert Club Names into Listbox"
        DB.InsertLogs(Val_1)
        
        print("Generate")
        select.delete(0,END)
        for i in Distinct_Club_Final:
            select.insert (END, i)

        print("setList  Size",len(Distinct_Club_Final))
        return Distinct_Club_Final
    except Exception as e:
        DB.InsertExceptionStmtTable(e,"Compare Two Teams - GenerateClubs")
        
    
#Insert a Team of User selection
def LoadTeam1():
    try:
        Val_1="inserting Team_1"
        DB.InsertLogs(Val_1)
        
        Distinct_Club_Final=GenerateClubs()
        print("Team1",len(Distinct_Club_Final))
        print(select.curselection())
        a=select.curselection()
        a = str(a).replace(',','').replace(')','').replace('(','')
        print(a)
        print(Distinct_Club_Final[int(a)])
        teamName1=str(Distinct_Club_Final[int(a)])
        Teamname1Var.set(teamName1)

        Val_1="insertion completed Team_1"
        DB.InsertLogs(Val_1)
        
    except Exception as e:
        tkinter.messagebox.showinfo("Error","Select a Team !!")
        DB.InsertExceptionStmtTable(e,"Compare Two Teams - LoadTeam1")
        

def LoadTeam2():
    try:
        Val_1="inserting Team_2"
        DB.InsertLogs(Val_1)
        
        Distinct_Club_Final=GenerateClubs()
        print("Team2",len(Distinct_Club_Final))
        print(select.curselection())
        a=select.curselection()
        a = str(a).replace(',','').replace(')','').replace('(','')
        print(a)
        teamName2=str(Distinct_Club_Final[int(a)])
        Teamname2Var.set(teamName2)

        Val_1="insertion Completed Team_2"
        DB.InsertLogs(Val_1)
    except Exception as e:
        tkinter.messagebox.showinfo("Error","Select a Team !!")
        DB.InsertExceptionStmtTable(e,"Compare Two Teams - LoadTeam2")

##Remove Team if User wants to change team
def clearTeam(x):
    try:
            
        if x==1:
            if Teamname1Var.get() =="":
                tkinter.messagebox.showinfo("Error","Nothing To Remove!")
                DB.InsertExceptionStmtTable("Nothing To Remove!","Comapare Two  Teams - clearTeam1")
            else:
                Teamname1Var.set("")
            
        else:
            if Teamname2Var.get() == "":
                tkinter.messagebox.showinfo("Error","Nothing To Remove!")
                DB.InsertExceptionStmtTable("Nothing To Remove!","Comapare Two  Teams - clearTeam2")
            else:
                Teamname2Var.set("")
    except Exception as e:
        print("Error",e)
        DB.InsertExceptionStmtTable(ae,"Comapare Two  Teams - clearTeam")
        

#Populate Data based on the team selected
def PopulateData(Team1, Team2):
    try:
        Val_1="Populating Data for Teams"
        DB.InsertLogs(Val_1)
        
        print(Team1)
        print(Team2)
        Gen_Values=[]
        Gen_Values_1=[]
        Team_1=[]
        Team_2=[]

        #Validate the Teams and Null values
        if Team1 =="":
            tkinter.messagebox.showinfo("Error","Team_1 Cannot be Empty")
            DB.InsertExceptionStmtTable("Team_1 Cannot be Empty","Comapare Two  Teams - clearTeam")
        elif Team2 == "":
            tkinter.messagebox.showinfo("Error","Team_2 Cannot be Empty")
            DB.InsertExceptionStmtTable("Team_2 Cannot be Empty","Comapare Two  Teams - clearTeam")
            
        elif Team1 == Team2:
            tkinter.messagebox.showinfo("Error","Team_1 and Team_2 are Same")
            DB.InsertExceptionStmtTable("Team_1 and Team_2 are Same","Comapare Two  Teams - clearTeam")
        else:

            Val_1="Populating Data for Team_1"
            DB.InsertLogs(Val_1)
            #Extract Player overall stats from the file for Team1
            Players_Data=ER.extractRecords()
            for i in range(0,len(Players_Data)):
                if Players_Data[i][8]==str(Team1):
                    Gen_Values.append(int(Players_Data[i][6]))

            Val_1="Populating Data for Team_2"
            DB.InsertLogs(Val_1)
            #Extract Player overall stats from the file for Team2
            for i in range(0,len(Players_Data)):
                if Players_Data[i][8]==str(Team2):
                    Gen_Values_1.append(int(Players_Data[i][6]))

            print(len(Gen_Values))
            print(len(Gen_Values_1))
            
            Val_1="Sorting Data for Teams"
            DB.InsertLogs(Val_1)
            ##Sort values of each Team
            Team_1=sorted(Gen_Values)
            Team_2=sorted(Gen_Values_1)
            print(Team_1)
            print(Team_2)

            ##pass each Team values as a list for box Plot
            Val_1="Generate box Plot"
            DB.InsertLogs(Val_1)
            
            data=[Team_1,Team_2]
            plt.boxplot(data)

            fig, ax = plt.subplots(facecolor='#d2f53c')
            ax.boxplot(data,widths = 0.3,patch_artist=True)
            plt.xlabel("Teams")
            ax.set_xticklabels([Team1,Team2])

            ax.set_facecolor("white")
            ax.yaxis.grid(linestyle='--')
            ax.xaxis.grid()

            plt.ylabel("Range of Players")
            plt.title("Team Comparison")
            plt.ylim(40,100)
            fig.show()
            Val_1="Box Plot completed"
            DB.InsertLogs(Val_1)
            
    except Exception as e:
        print("Error", e)
        DB.InsertExceptionStmtTable(e,"Comapre Two Teams - PopulateData")


#buildFrame()

