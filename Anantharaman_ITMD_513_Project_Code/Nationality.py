#############################################################################
# Author     : Anantharaman Chandar                                         #
# CWID       : A20403439                                                    #
# Course     : ITMD 513 Open Source Programming Final Project               #
# Instructor : James Papademas                                              #
# Description: This script generates Scatter Plot for the selected          #
#              nationalities                                                #
#                                                                           #                      
#                                                                           #
#                                                                           #
#############################################################################

#Import Necessary Libraries
import sys,time,io,os,tkinter.messagebox
import matplotlib.pyplot as plt
import numpy as np

#Import Necessary modules from the Libraries
from tkinter import *

#Import other files
import DB_Objects as DB
import Nationality_Display as ND
import Extract_Records as ER
import DB_Objects as DB

#Declare necessary Variables 
countries=[]
Tosend={}


#GUI Formation Function   
def buildFrame () :
    try:
            
        Val_1="Opening Nationality Menu"
        DB.InsertLogs(Val_1)
        global select,root, nameVar, mobVar
        print("Start")
        #Build Frame
        root=Tk()
        root.title("Country Stats")
        root.resizable(width=FALSE, height=FALSE)
        root.geometry('1000x650')
        

        GUIFrame = Frame(root)
        GUIFrame.grid(row=20,column=20)

        #Header
        Heading = Label(GUIFrame, text = "Welcome To FIFA 18 Player Stats Country Stats").grid(row=1, column=3)  

        #Add Button
        AddButton = Button(GUIFrame, text="Add",command= lambda: loadFunction(1)).grid(row=12, column=2)
        AddAllButton = Button(GUIFrame, text="Add All",command=lambda: loadFunction(2)).grid(row=12, column=3)

        #Remove Button
        RemoveButton = Button(GUIFrame, text="Remove",command=lambda: removeFunction(1)).grid(row=12, column=5)
        RemoveAllButton = Button(GUIFrame, text="Remove All",command=lambda: removeFunction(2)).grid(row=12, column=6)
        GenerateButton = Button(GUIFrame, text="Generate",command=GenerateScatterPlotDict).grid(row=20, column=3)
        
        #Listbox for Nationalities 
        DisplayCountryLabel = Label(GUIFrame, text="Below are the available Countries").grid(row=11,column=0)
        scroll = Scrollbar(GUIFrame, orient=VERTICAL)
        select = Listbox(GUIFrame, yscrollcommand=scroll.set, height=15)
        scroll.config (command=select.yview)
        select.grid(row=12,column=0)

        #Listbox for selected Nationalities 
        global scroll_Add
        global select1
        DisplayCountrySelectedLabel = Label(GUIFrame, text="Below are the selected Countries").grid(row=11,column=4)
        scroll_Add = Scrollbar(GUIFrame, orient=VERTICAL)
        select1 = Listbox(GUIFrame,yscrollcommand=scroll_Add.set, height=15)
        scroll_Add.config (command=select1.yview)
        select1.grid(row=12,column=4)

        setList()
        #ER.extractRecords()
        root.mainloop()
        return GUIFrame
    except Exception as e:
        DB.InsertExceptionStmtTable(e,"Nationality - GenerateClubs")

#Inserts Countries fetched from Database
def setList ():
    try:
        Val_1="Extracting Nationality "
        DB.InsertLogs(Val_1)   
        conn = DB.OpenConnection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM AC_FIFA18_COUNTRIES ORDER BY 1 ')
        select.delete(0,END)
        for name in cur.fetchall():
            #temp=[name,count]
            #countries.append(temp)
            select.insert (END, name)
        #print(countries)
        Val_1="Extracting Nationality Completed"
        DB.InsertLogs(Val_1)
        
    except Exception as e:
        DB.InsertExceptionStmtTable(e,"Nationality - setList")

#Loads selected country from the listbox based on the parameter
#Parameters == 1--> Any one country 2 --> All Countries
def loadFunction(x):
    try:
        Val_1="Loading Selected Country based on the parameter"
        DB.InsertLogs(Val_1)   
        #a = select.curselection()
        #print("Value is ",a)
        c =select.curselection()
        print(c)
        print("Pass")
        print("C Value ", c)
        print("Select Value",select1.get(0,END))
        if c ==():
            if x==2:
                conn = DB.OpenConnection()
                cur = conn.cursor()
                cur.execute('SELECT * FROM AC_FIFA18_COUNTRIES ORDER BY 1 ')
                for name in cur.fetchall():
                    select1.insert (END, name)
            else:
                tkinter.messagebox.showinfo("Error","You haven't Selected Any!")
                DB.InsertExceptionStmtTable("You haven't Selected Any team!","Nationality - loadFunction")
        else:
            c =select.get(ACTIVE)
            print(c)
            if c in select1.get(0,END):
                tkinter.messagebox.showinfo("Error","Duplicate Value Cannot be inserted")
                DB.InsertExceptionStmtTable("Duplicate Value Cannot be inserted","Nationality - loadFunction")
            else:
                if x == 1:
                    print("Can Add")
                    print(select.curselection())
                    a=select.get(ACTIVE)
                    select1.insert(END, a)
                else:
                    print("Error")

    except Exception as e:
        tkinter.messagebox.showinfo("Error",e)
        DB.InsertExceptionStmtTable(e,"Nationality - loadFunction")

#Removes Nationalities based on the parameter
#Parameters == 1--> Any one country 2 --> All Countries
def removeFunction(x):
    print("Remove")
    try:
        Val_1="Generating Scatter Plot"
        DB.InsertLogs(Val_1)  
        if select1.size() == 0:
            tkinter.messagebox.showinfo("Error","Nothing to Remove")
            DB.InsertExceptionStmtTable("Nothing to Remove","Nationality - removeFunction")
        else:
            if x ==1:
                #print(select1.curselection())
                a=select1.curselection()
                print("Remove",a)
                print("Replacing")
                #a = str(a).replace(",","")
                print("After", a)
                select1.delete(a,END)
            elif x == 2:
                
                select1.delete(0,END)
            else:
                print("Error")
            
    except Exception as e:
        tkinter.messagebox.showinfo("Error",e)
        DB.InsertExceptionStmtTable(e,"Nationality - removeFunction")

#Generate Scatter Plot from the selected
def GenerateScatterPlotDict():
    try:
        Val_1="Populating Scatter Plot for the countries after validations"
        DB.InsertLogs(Val_1)      
        if select1.size() ==0:
            tkinter.messagebox.showinfo("Error","Add Atleast one or more Countries to view Scatter Plot")
            DB.InsertExceptionStmtTable("Add Atleast one or more Countries to view Scatter Plot","Nationality - removeFunction")
        else:
            Tosend={}
            print("Here1")
            #ND.Nationality_Selection()
            Final_Count = ND.Nationality_Selection()
            #print(Final_Count)
            #print("Generating")
            #print(Final_Count)
            print(select1.size())

            #For each of the countries go in a for loop and update the value
            for i in range(0,select1.size()):
                country = select1.get(i)
                #print("Country Name",country[0])
                #print(Final_Count[country[0]])
                Tosend.update({country[0]:Final_Count[country[0]]})

            #After the for loop send the values to generate Scatter plot
            plotScatterPlot(Tosend)
    except Exception as e:
        DB.InsertExceptionStmtTable(e,"Nationality - GenerateScatterPlotDict")

#Plot the scatter plots and Format the plot    
def plotScatterPlot(Tosend):
    try:
        Val_1="Populating Scatter Plot for the countries after values are fetched"
        DB.InsertLogs(Val_1)  
        x = Tosend.keys()
        y = Tosend.values()
        
        fig, ax = plt.subplots()
        ax.set_facecolor("#fffac8")
        ax.scatter(y,x,color='#800000',s=10,edgecolors='black',linewidths=10)
        
        plt.xlabel("Count")
        #plt.ylabel("")
        plt.xlim(0,2000)
        ax.grid(True)
        #ax.set_ylim(width=10, len=200)
        plt.title("Players Distribution based on Nationality")
        fig.show()
    except Exception as e:
       DB.InsertExceptionStmtTable(e,"Nationality - plotScatterPlot")
       
    



    
#buildFrame()
#setList()

