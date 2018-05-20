#############################################################################
# Author     : Anantharaman Chandar                                         #
# CWID       : A20403439                                                    #
# Course     : ITMD 513 Open Source Programming Final Project               #
# Instructor : James Papademas                                              #
# Description: This script shows details about Players/Clubs/National Teams #
#               in a web browser                                            #
#                                                                           #                      
#                                                                           #
#                                                                           #
#############################################################################

#Import Libraries
import sys,time,io,os,tkinter.messagebox
import urllib
import webbrowser

#import specific modules from the Libraries
from tkinter import *

#Import other files
import Extract_Records as ER
import DB_Objects as DB

#Declare Necessary Variables
Personal_Details=[]
Nationality_Details=[]
Club_Details=[]
url_Link = 'https://www.google.com/search?q='

#GUI Formation Function   
def buildFrame () :
    try:
            
        Val_1="Builiding Personal Details GUI"
        DB.InsertLogs(Val_1)    
        global select,GUIFrame, urlVar, select_1, select_2
        print("Start")
        #Build Frame
        root=Tk()
        root.title("Country Stats")
        root.resizable(width=FALSE, height=FALSE)
        root.geometry('1000x650')
        

        GUIFrame = Frame(root)
        GUIFrame.grid(row=40,column=20)

        #Header
        Heading = Label(GUIFrame, text = "Welcome To FIFA 18 Player Stats Country Stats").grid(row=1, column=3)  
        

        
        #Display Country
        DisplayCountryLabel = Label(GUIFrame, text="Select anyone player").grid(row=11,column=0)
        scroll = Scrollbar(GUIFrame, orient=VERTICAL)
        select = Listbox(GUIFrame, yscrollcommand=scroll.set, height=15)
        scroll.config (command=select.yview)
        select.grid(row=12,column=0)
        AddButton = Button(GUIFrame, text="Search this Player in Web",command=lambda: GenerateURL(1)).grid(row=12, column=3)
        

     

        #Display Club
        DisplayClubLabel = Label(GUIFrame, text="Select any Club").grid(row=11,column=4)
        scroll_1 = Scrollbar(GUIFrame, orient=VERTICAL)
        select_1 = Listbox(GUIFrame, yscrollcommand=scroll_1.set, height=15)
        scroll_1.config (command=select_1.yview)
        select_1.grid(row=12,column=4)
        AddButton = Button(GUIFrame, text="Search this Club in Web",command=lambda: GenerateURL(2)).grid(row=12, column=7,padx=20)


        #Display Nationalities
        DisplayNationalityLabel = Label(GUIFrame, text="Select any Nationality").grid(row=11,column=8)
        scroll_2 = Scrollbar(GUIFrame, orient=VERTICAL)
        select_2 = Listbox(GUIFrame, yscrollcommand=scroll_2.set, height=15)
        scroll_2.config (command=select_2.yview)
        select_2.grid(row=12,column=8)
        AddButton = Button(GUIFrame, text="Search this Nationality in Web",command=lambda: GenerateURL(3)).grid(row=12, column=10,padx=20)

        Val_1="Extracting Players Data - Personal Details"
        DB.InsertLogs(Val_1)  
        #Extact Players Data
        Players_Data=ER.extractRecords()

        Val_1="Pass Players Data to the list box - Personal Details"
        DB.InsertLogs(Val_1)  
        #Extract Players Data
        setList(Players_Data)

        Val_1="Pass Players Data(Club) to the list box - Personal Details"
        DB.InsertLogs(Val_1)         
        #Extract Club Details
        setClubList(Players_Data)

        Val_1="Pass Players Data (Nationality) to the list box - Personal Details"
        DB.InsertLogs(Val_1) 
        #Extract Nationality details
        setNationalityList(Players_Data)
        root.mainloop()
        return GUIFrame
    
    except Exception as e:
        DB.InsertExceptionStmtTable(e,"Personal Details - buildFrame")

#Extract Players Name
def setList (Players_Data):
    try:
        Val_1="Populate Players Data to the listbox"
        DB.InsertLogs(Val_1)         
        for i in range(0,len(Players_Data)):
            Personal_Details.append(Players_Data[i][1])
            select.insert(END, Players_Data[i][1])
    except Exception as e:
        DB.InsertExceptionStmtTable(e,"Personal Details - setList")

#Extract Club Name
def setClubList (Players_Data):
    #Players_Data=ER.extractRecords()
    try:
        Val_1="Populate Club Details Data to the listbox"
        DB.InsertLogs(Val_1)            
        Club_Details=[]
        for i in range(0,len(Players_Data)):
            Club_Details.append(Players_Data[i][8])

        Val_1="Remove Duplicates from Club Data"
        DB.InsertLogs(Val_1)        
        Club_Details = set(Club_Details)
        Club_Details = list(Club_Details)

        #Delete Null Values
        del Club_Details[0]
        Val_1="Populate Club Data to the listbox"
        DB.InsertLogs(Val_1)
        for i in range(len(Club_Details)):
            select_1.insert(0, Club_Details[i])
            
    except Exception as e:
        DB.InsertExceptionStmtTable(e,"Personal Details - setClubList")

#Extract Nationality  Name
def setNationalityList (Players_Data):
    #Players_Data=ER.extractRecords()
    try:
        Val_1="Populate Nationality Details Data to the list"
        DB.InsertLogs(Val_1)            
        Nationality_Details=[]
        for i in range(0,len(Players_Data)):
            Nationality_Details.append(Players_Data[i][4])

        Val_1="Remove Duplicates from Nationalities"
        DB.InsertLogs(Val_1)
        Nationality_Details = set(Nationality_Details)
        Nationality_Details=list(Nationality_Details)
        #printNationality_Details)
        #print(Nationality_Details[5])
        Val_1="Populate Nationality Details Data to the listbox"
        DB.InsertLogs(Val_1)
        for i in range(len(Nationality_Details)):
            select_2.insert(END, Nationality_Details[i])
    except Exception as e:
        DB.InsertExceptionStmtTable(e,"Personal Details - setNationalityList")
    

#Generate URL and Open web browser based on the parameter
#Parameters == 1 --> Player 2 --> Club Details 3 --> Nationality
        
def GenerateURL(x):
     try:
         print("X Value",x)
        
         if x ==1:
             a = select.curselection()
             if a == ():
                 tkinter.messagebox.showinfo("Error","Select Any Player to View")
                 DB.InsertExceptionStmtTable("Player not selected","Personal Details - setNationalityList")
             else:
                 a=select.get(ACTIVE)
                 print(a)
                 link=url_Link+a
                 webbrowser.open_new(link)
         elif x ==2:
             a = select_1.curselection()
             if a == ():
                 tkinter.messagebox.showinfo("Error","Select Any Club to View")
                 DB.InsertExceptionStmtTable("Club not selected","Personal Details - setNationalityList")
             else:
                 a=select_1.get(ACTIVE)
                 print(a)
                 link=url_Link+a+"+Football+Club"
                 webbrowser.open_new(link)
         elif x ==3:
             a = select_2.curselection()
             if a == ():
                 tkinter.messagebox.showinfo("Error","Select Any Nationality to View")
                 DB.InsertExceptionStmtTable("Nationality not selected","Personal Details - setNationalityList")
             else:
                 a=select_2.get(ACTIVE)
                 print(a)
                 link=url_Link+a+"+National+Football+Team"
                 webbrowser.open_new(link)
         else:
            print("Error")
                 
        
         
        
         
     except Exception as e:
         print(e)
         DB.InsertExceptionStmtTable(e,"Personal Details - GenerateURL")


#buildFrame()
