#############################################################################
# Author     : Anantharaman Chandar                                         #
# CWID       : A20403439                                                    #
# Course     : ITMD 513 Open Source Programming Final Project               #
# Instructor : James Papademas                                              #
# Description: This script compares two players regarding their             #
#              Overall vs Potential Growth                                  #
#                                                                           #                      
#                                                                           #
#                                                                           #
#############################################################################

# Import the necessary Libraries 
import sys,time,io,os,tkinter.messagebox
import matplotlib.pyplot as plt
import numpy as np

#Import specific modules from the Libraries
from tkinter import *

#Import other files
import DB_Objects as DB
import Extract_Records as ER


#Declare Necessary variables
Distinct_Club=[]
Distinct_Club_Final=[]
Players_Data=[]
Player1_Values=[]
Player2_Values=[]
global teamName2,teamName1
Team_1=[]
Team_2=[]
FetchDataSQL = "SELECT OVERALL, POTENTIAL FROM AC_FIFA18_READ_DATA WHERE NAME = "


#GUI Formation Function   
def buildFrame () :
    try:
            
        Val_1="Opening Players_Compare Menu"
        DB.InsertLogs(Val_1)
        
        global select,root, Player1_Var, Player2_Var, Team1,Team2,AddTeam1Button,AddTeam2Button
        print("Start")
        #Build Frame
        root=Tk()
        root.title("Country Stats")
        root.resizable(width=FALSE, height=FALSE)
        root.geometry('1000x650')
        

        GUIFrame = Frame(root)
        GUIFrame.grid(row=20,column=20)




        #Player1
        #Player1Label = Label(GUIFrame, text = "Team_1 Selected").grid(row=12, column=3)
        Player1_Var = StringVar(GUIFrame)
        Team1 = Entry(GUIFrame, textvariable=Player1_Var).grid(row=12, column=4, sticky=E)

        #Player2
        #Player2Label = Label(GUIFrame, text = "Team_2 Selected").grid(row=13, column=3)
        Player2_Var = StringVar(GUIFrame)
        Team2 = Entry(GUIFrame, textvariable=Player2_Var).grid(row=13, column=4, sticky=E)
        



        DisplayPlayerLabel = Label(GUIFrame, text="Below are the available Teams").grid(row=11,column=0)
        scroll = Scrollbar(GUIFrame, orient=VERTICAL)
        select = Listbox(GUIFrame, yscrollcommand=scroll.set, height=25)
        scroll.config (command=select.yview)
        select.grid(row=12,column=0)
        
        #Header
        Heading = Label(GUIFrame, text = "Welcome To FIFA 18 Player Stats Club Stats").grid(row=1, column=3)  
        AddTeam1Button = Button(GUIFrame, text="Add Player_1",command=LoadPlayer1).grid(row=12, column=2)
        AddTeam2Button = Button(GUIFrame, text="Add Player_2",command=LoadPlayer2).grid(row=13, column=2)
        
        RemoveTeam1Button = Button(GUIFrame, text="Clear Player_1").grid(row=12, column=6,padx=30)
        RemoveTeam2Button = Button(GUIFrame, text="Clear Player_2").grid(row=13, column=6,padx=10)


        GenerateButton = Button(GUIFrame, text="Generate",command=lambda: PopulateData(Player1_Var.get(),Player2_Var.get())).grid(row=26, column=4,pady=30)


        
        setList()
        root.mainloop()
        return GUIFrame
    except Exception as e:
        DB.InsertExceptionStmtTable(e,"Players_Compare - buildFrame")
    

#Generate Players Name from the Database
def setList ():
    try:
        Val_1="Populating Players Name from DB"
        DB.InsertLogs(Val_1)            
        print("Generate")
        conn = DB.OpenConnection()
        c= conn.cursor()
        c.execute("SELECT NAME FROM AC_FIFA18_READ_DATA;")
        select.delete(0,END)
        for name in c.fetchall():
            select.insert (END, name)
    except Exception as e:
        DB.InsertExceptionStmtTable(e,"Players_Compare - setList")
        

#Load Player 1 Name
def LoadPlayer1():
    try:
        Val_1="Load player 1 data and Validate"
        DB.InsertLogs(Val_1)          
        a=select.curselection()
        if a == ():
            tkinter.messagebox.showinfo("Error","Choose a Player")
            DB.InsertExceptionStmtTable("Player_1 Empty","Players_Compare - LoadPlayer1")
        else:
            Player1_Var.set(select.get(ACTIVE))
    except Exception as e:
        tkinter.messagebox.showinfo("Error",e)
        DB.InsertExceptionStmtTable(e,"Players_Compare - LoadPlayer1")

#Load Player 1 Name
def LoadPlayer2():
    try:
        Val_1="Load player 2 data and Validate"
        DB.InsertLogs(Val_1)        
        a=select.curselection()
        if a == ():
            tkinter.messagebox.showinfo("Error","Choose a Player")
            DB.InsertExceptionStmtTable("Player_2 Empty","Players_Compare - LoadPlayer2")
        else:
            Player2_Var.set(select.get(ACTIVE))
    except Exception as e:
        tkinter.messagebox.showinfo("Error",e)
        DB.InsertExceptionStmtTable(e,"Players_Compare - LoadPlayer2")

def clearTeam(x):
    if x==1:
        Player1_Var.set("")
    else:
        Player2_Var.set("")


#Populate the Players Overall and Potential
def PopulateData(Player1_Name, Player2_Name):
    #print(Player1_Name)
    #print(Player2_Name)

    try:
        Val_1="Load Players data and Validate"
        DB.InsertLogs(Val_1)
        
        Player2_Values=[]
        Player1_Values=[]
        
        Player1_Name = str(Player1_Name).replace(",",'')
        Player2_Name = str(Player2_Name).replace(",",'') 
        if Player1_Name=="":
            tkinter.messagebox.showinfo("Error","Player1 Name is Empty")
            DB.InsertExceptionStmtTable("Player1 Name is Empty","Players_Compare - PopulateData")
        elif Player2_Name=="":
            tkinter.messagebox.showinfo("Error","Player2 Name is Empty")
            DB.InsertExceptionStmtTable("Player2 Name is Empty","Players_Compare - PopulateData")
            
        elif Player1_Name == Player2_Name:
            tkinter.messagebox.showinfo("Error","Same Player Choosen")
            DB.InsertExceptionStmtTable("Same Player Choosen","Players_Compare - PopulateData")
        else:
                
            print("STR", Player1_Name)
            #print(FetchDataSQL+Player1_Name)

            Val_1="Open DB and Fect the Player 1 Overall and Potential"
            DB.InsertLogs(Val_1)
            conn = DB.OpenConnection()
            c=conn.cursor()
            c.execute(FetchDataSQL+Player1_Name)
            for overall,potenetial in c.fetchall():
                #print(overall)
                #print(potenetial)
                Player1_Values.append(overall)
                Player1_Values.append(potenetial)

            Val_1="Open DB and Fect the Player 2 Overall and Potential"
            DB.InsertLogs(Val_1)
            c=conn.cursor()
            c.execute(FetchDataSQL+Player2_Name)
            for overall,potenetial in c.fetchall():
                Player2_Values.append(overall)
                Player2_Values.append(potenetial)
                
            print(Player1_Values)
            print(Player2_Values)


            Val_1="Plot Barplots for Player 1 and Player 2 and Format"
            DB.InsertLogs(Val_1)
            y = np.arange(2)
            plt.autoscale(tight=True)
            Player1_color = ['red','green']
            Player2_color=['blue','green']
            
            a = plt.bar(y+1,Player1_Values ,width=0.7,alpha=1,color=Player1_color,edgecolor='black')
            b = plt.bar(y+5,Player2_Values ,width=0.7,alpha=1,color=Player2_color,edgecolor='black')
           
            plt.xlim(0,7)

            ##i is location, v is value for Legend
        
            for i,v in enumerate(Player1_Values):
                plt.text(i+1,v+1,str(v),fontweight='bold')

            for i,v in enumerate(Player2_Values):
                plt.text(i+5,v+1,str(v),fontweight='bold')


            
            plt.legend([a,b],[Player1_Name+' Overall',Player2_Name+' Overall'],loc=10)
            plt.ylim(0,100)

            #plt.grid(True)
            #plt.spines['left'].set_linewidth(1)
            plt.xlabel('Players')
            plt.ylabel('Potential')
            plt.title('Overall vs Potential')
            plt.show()
    except Exception as e:
        DB.InsertExceptionStmtTable(e,"Players_Compare - PopulateData")
#buildFrame()

