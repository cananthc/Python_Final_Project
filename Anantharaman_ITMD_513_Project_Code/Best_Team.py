#############################################################################
# Author     : Anantharaman Chandar                                         #
# CWID       : A20403439                                                    #
# Course     : ITMD 513 Open Source Programming Final Project               #
# Instructor : James Papademas                                              #
# Description: This script gives you a best team report based on the        #
#              selected formation                                           #                      
#                                                                           #
#                                                                           #
#############################################################################

##Import Libraries needed
import sys,time,io,os,tkinter.messagebox
import numpy as np

#Import specifc modules from the libraries 
from tkinter import *


#Import other python files
import DB_Objects as DB

##Declare necessary variables
squad=list()
Def =""
Mid = ""
Att = ""
Defender    = list()
Midfielders = list()
Attackers   = list()
GoalKeeper = list()
DefSql_LB=""
DefSql_LB=""

#tkinter Screen
def buildFrame () :
    Val_1="Opening Best Team Menu"
    DB.InsertLogs(Val_1)
    global FormationVar,Condvar,root,select, GUIFrame
    root = Tk()
    root.title("FIFA 18 Team Selection")
    root.resizable(width=FALSE, height=FALSE)
    root.geometry('1000x650')

    global FormationVar,Condvar
    # Add a grid
    GUIFrame = Frame(root)
    GUIFrame.grid(column=0,row=0, sticky=(N,W,E,S) )

    Condvar  = StringVar(GUIFrame)
    
     #Headingx
    Heading = Label(GUIFrame, text = "Welcome To FIFA 18 Best Team").grid(row=1, column=5)  
    Heading1 = Label(GUIFrame, text = "Stats").grid(row=2, column=5)

   
    DisplayCountryLabel = Label(GUIFrame, text="Below are the available Formations").grid(row=3,column=5)
    scroll = Scrollbar(GUIFrame, orient=VERTICAL)
    select = Listbox(GUIFrame, yscrollcommand=scroll.set, height=5)
    scroll.config (command=select.yview)
    select.grid(row=4,column=5)

    FormationLabel = Label(GUIFrame, text = "Formation Selected").grid(row=3, column=9)
    FormationVar = StringVar(GUIFrame)
    FormationVar.set('')
    FormationDisplay = Entry(GUIFrame, textvariable=FormationVar).grid(row=4, column=10,sticky=W)
    
    AddButton = Button(GUIFrame, text="Add",command=AddFormation).grid(row=4, column=6)
    GenerateButton =  Button(GUIFrame, text="Generate",command=createSquad).grid(row=4, column=11, padx=20)
    ClearButton =  Button(GUIFrame, text="Clear",command=clearButton).grid(row=4, column=12, padx=20)
    setList()
    return GUIFrame


# Fetch and Insert Formation from the database
def setList ():
    try:
        ##Log Statement
        Val_1="Started Fetching Formation from DB"
        DB.InsertLogs(Val_1)
        
        print("Generate")
        #print(Condition)
        conn = DB.OpenConnection()
        c = conn.cursor()
        c.execute('SELECT FORMATION FROM AC_FIFA18_FORMATIONS')
        select.delete(0,END)
        for i in c.fetchall():
            select.insert (END, i)
            
        ##Log Statement
        Val_1="Completed Inserting Formation "
        DB.InsertLogs(Val_1)
        
    except Exception as e:
        DB.InsertExceptionStmtTable(e,"Best Team - setList")
        

# Add the user selected formation
def AddFormation():
    try:
        ##Log Statement
        Val_1="Formation Selection"
        DB.InsertLogs(Val_1)
        
        a = select.curselection()
        print("Pass")
        if select.curselection() == ():
            tkinter.messagebox.showinfo("Error", "Select a formation")
            DB.InsertExceptionStmtTable(e,"Best Team - AddFormation - No formation selected")
        else:
            FormationVar.set(select.get(ACTIVE))
            
    except Exception as e:
        print("Error",e)
        DB.InsertExceptionStmtTable(e,"Best Team- AddFormation")


##Fetch necessary details from the Databse for the formation 
def createSquad():
    try:

        ##Log Statement
        Val_1="Formation Selection-2"
        DB.InsertLogs(Val_1)
        
        if FormationVar.get()=="":
            tkinter.messagebox.showinfo("Error", "Select a formation to generate Your Squad")
            DB.InsertExceptionStmtTable(e,"Best Team - AddFormation - No formation selected-2")
        else:
            try:

                ##Log Statement
                Val_1="Opening Connection for formation details"
                DB.InsertLogs(Val_1)
                
                conn = DB.OpenConnection()
                c = conn.cursor()
                b = FormationVar.get()
                b = ((b.replace(',','')).replace('(','')).replace(')','')
                print(b)
                sql = 'SELECT Defenders,Midfielders,Attackers FROM AC_FIFA18_FORMATIONS Where Formation = '+str(b)
                c.execute(sql)

                
                squad =[] # Insert how many defenders/Midfielders/Attackers necessary for the foramation
                for i in c.fetchone():
                    squad.append(i)

                #Log Statement
                Val_1="Squad details fetched"
                DB.InsertLogs(Val_1)
                
                print(len(squad))
                print("squad is ",squad)
                Def = squad[0] #Defenders
                Mid = squad[1] #Midfielders
                Att = squad[2] #Attackers

                #Pass on the above details to generate Players Llist
                Val_1="Generate Squad"
                DB.InsertLogs(Val_1)
                
                generateSquad(Def,Mid,Att)
                
            except Exception as e:
                print(e)
                DB.InsertExceptionStmtTable(e,"Best Team - CreateSquad")
    except Exception as ae:
        print(ae)
        DB.InsertExceptionStmtTable(ae,"Best Team- CreateSquad Outer Exception")


#Extract Players Information from the parameters
def generateSquad(Def, Mid, Att):
    try:

        Val_1="Fetching Players based on the values"
        DB.InsertLogs(Val_1)
        
        Defender    = list()
        Midfielders = list()
        Attackers   = list()
        GoalKeeper = list()

        Val_1="Opening Connection for Squad Creation"
        DB.InsertLogs(Val_1)
        
        conn = DB.OpenConnection()
        c = conn.cursor()

        Val_1="Fetching Defenders"
        DB.InsertLogs(Val_1)
        ##Fetch Defenders
        if Def ==5:
            DefSql_CB = "SELECT NAME FROM AC_FIFA18_READ_DATA where PreferredPositions like '%CB%' order by Overall desc LIMIT 3; "
            DefSql_RB = "SELECT NAME FROM AC_FIFA18_READ_DATA where PreferredPositions like '%RB%' order by Overall desc LIMIT 1; "
            DefSql_LB = "SELECT NAME FROM AC_FIFA18_READ_DATA where PreferredPositions like '%LB%' order by Overall desc LIMIT 1; "
            rows = c.execute(DefSql_CB)
            
            for row in rows:
                Defender.append(row)
            
            rows = c.execute(DefSql_LB)
            for row in rows:
                Defender.append(row)

            rows = c.execute(DefSql_RB)
            for row in rows:
                Defender.append(row)
                
            print(Defender)
            
                
        elif Def == 4:
            DefSql_CB = "SELECT NAME FROM AC_FIFA18_READ_DATA where PreferredPositions like '%CB%' order by Overall desc LIMIT 2;"
            DefSql_RB = "SELECT NAME FROM AC_FIFA18_READ_DATA where PreferredPositions like '%RB%' order by Overall desc LIMIT 1; "
            DefSql_LB = "SELECT NAME FROM AC_FIFA18_READ_DATA where PreferredPositions like '%LB%' order by Overall desc LIMIT 1; "
            rows = c.execute(DefSql_CB)
            
            for row in rows:
                Defender.append(row)
            
            rows = c.execute(DefSql_LB)
            
            for row in rows:
                Defender.append(row)

            rows = c.execute(DefSql_RB)
            
            for row in rows:
                Defender.append(row)

        elif Def == 3:
            
            DefSql_CB = "SELECT NAME FROM AC_FIFA18_READ_DATA where PreferredPositions like '%CB%' order by Overall desc LIMIT " + str(Def) + ";"
            rows = c.execute(DefSql_CB)
            
            for row in rows:
                Defender.append(row)
            
        else:
            pass


        Val_1="Fetching Midfielders"
        DB.InsertLogs(Val_1)
        ##Fetch Midfielders
        MidSql = "SELECT NAME FROM AC_FIFA18_READ_DATA WHERE PreferredPositions like '%CM%' order by Overall desc LIMIT " +str(Mid) +";"
        rows = c.execute(MidSql)
            
        for row in rows:
            Midfielders.append(row)
            
        Val_1="Fetching Attackers"
        DB.InsertLogs(Val_1)
        ##Fetch Attackers
        AttSql = "SELECT NAME FROM AC_FIFA18_READ_DATA where PreferredPositions like '%ST%' OR PreferredPositions like '%RW%'\
                  order by Overall desc LIMIT " + str(Att) +";"
        rows = c.execute(AttSql)
            
        for row in rows:
            Attackers.append(row)

        Val_1="Fetching Goal Keeper"
        DB.InsertLogs(Val_1)
        ##Fetch Goal keepers
        GKSql = "SELECT NAME FROM AC_FIFA18_READ_DATA where PreferredPositions like '%GK%' order by Overall desc LIMIT 1;"
        rows = c.execute(GKSql)
            
        for row in rows:
            GoalKeeper.append(row)

        print("Defenders are ", Defender)
        print("Mid are ", Midfielders)
        print("Att are ", Attackers)
        print("GK are ", GoalKeeper)


        ## Listbox Formatting
        TeamLabel = Label(GUIFrame, text="Below is Your Team").grid(row=5,column=1,pady = 10)
        scroll = Scrollbar(GUIFrame, orient=VERTICAL)
        BestTeam = Listbox(GUIFrame, yscrollcommand=scroll.set, height=30)
        scroll.config (command=select.yview)
        BestTeam.grid(row=6,column=1)


        ##Insert each players in the Listbox
        Val_1="Insert Players"
        DB.InsertLogs(Val_1)
        
        #Fetch Goal Keeper
        BestTeam.insert(END, "Goal Keeper: ")
        for i in GoalKeeper:
            BestTeam.insert(END,i)

        BestTeam.insert(END, "  ")
        BestTeam.insert(END, "  ")
        BestTeam.insert(END, "  ")
        BestTeam.insert(END, "Defenders: ")

        #Fetch Defenders
        for i in Defender:
            BestTeam.insert(END,i)

        BestTeam.insert(END, "  ")
        BestTeam.insert(END, "  ")
        BestTeam.insert(END, "  ")

        #Fetch Midfielders
        BestTeam.insert(END, "Midfielders: ")
        for i in Midfielders:    
            BestTeam.insert(END,i)   

        BestTeam.insert(END, "  ")
        BestTeam.insert(END, "  ")
        BestTeam.insert(END, "  ")

        #Fetch Attackers
        BestTeam.insert(END, "Attackers: ")
        for i in Attackers:            
            BestTeam.insert(END,i)
            
    except Exception as a:
        print(a)
        DB.InsertExceptionStmtTable(a,"Best Team - generateSquad")


##Clear Selection
def clearButton():
    if FormationVar.get()=="":
        tkinter.messagebox.showinfo("Error", "Nothing to remove")
    else:
        root.destroy()
        buildFrame()
    
    
    

    
    
#buildFrame()
#setList("Attack")
#root.mainloop()
