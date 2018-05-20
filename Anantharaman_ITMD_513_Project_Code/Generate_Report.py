#############################################################################
# Author     : Anantharaman Chandar                                         #
# CWID       : A20403439                                                    #
# Course     : ITMD 513 Open Source Programming Final Project               #
# Instructor : James Papademas                                              #
# Description: This script is used for Generating Report                    #
#                                                                           #
#                                                                           #                      
#                                                                           #
#                                                                           #
#############################################################################


#Import Necessary variables
import csv,os,fnmatch,sys,tkinter.messagebox

#Import specific modules from the libraries
from tkinter import *

#Import other files
import Extract_Records as ER
import DB_Objects as DB


#Declare necessary variables
ColValues=[]
SQLStatement = "SELECT * FROM AC_FIFA18_READ_DATA WHERE "
strConversion = ["Name","Club","Nationality","PreferredPosition"]
Value=""
FileValNotAccepted = ['.txt','csv','.json','.html']
directory=""
Final_Val=""


#GUI Formation Function 
def buildFrame():
    Val_1="Opening Generate Report Menu"
    DB.InsertLogs(Val_1)
    
    root = Tk()
    root.title("FIFA 18 Report Extraction")
    root.resizable(width=FALSE, height=FALSE)
    root.geometry('1000x650')
     
    # Add a grid
    GUIFrame = Frame(root)
    GUIFrame.grid(column=0,row=0, sticky=(N,W,E,S) )
    
     
    # Create a Tkinter variable
    global Colvar,Condvar,Valuevar,Formatvar,Filevar
    Colvar   = StringVar(GUIFrame)
    Condvar  = StringVar(GUIFrame)
    Valuevar = StringVar(GUIFrame)
    Filevar = StringVar(GUIFrame)
    Formatvar=StringVar(GUIFrame)
    

    #Headingx
    Heading = Label(GUIFrame, text = "Welcome To FIFA 18 Report Extraction").grid(row=1, column=5)  
    Heading1 = Label(GUIFrame, text = "Stats").grid(row=2, column=5)
   
    #Below columns are ignored as it is not necessary and append Column Names 
    ColNames = ER.extractColumnNames()
    for i in range(0,75):
        if i in(3,5,9,12,52):
            pass
        else:
            ColValues.append(ColNames[0][i])

    #Columns are stored here 
    Columns = ColValues
       
    Colvar.set('') # set the default option
    popupMenu = OptionMenu(GUIFrame, Colvar, *Columns)
    Label(GUIFrame, text="Choose a Column ").grid(row = 6, column = 1)
    popupMenu.grid(row = 7, column =1)

    # Conditions
    Conditons = { '<','>','<=','>=','!=', '=='}
    Condvar.set('') # set the default option
    ConditionMenu = OptionMenu(GUIFrame, Condvar, *Conditons)
    Label(GUIFrame, text="Choose a Condition ").grid(row = 6, column = 3)
    ConditionMenu.grid(row = 7, column =3)


    #Get Value
    Label(GUIFrame, text="Enter The Value").grid(row = 6, column = 4)
    Value = Entry(GUIFrame, textvariable=Valuevar).grid(row=7, column=4)

    #FileName Value
    Label(GUIFrame, text="Enter The FileName").grid(row = 8, column = 1)
    Value = Entry(GUIFrame, textvariable=Filevar).grid(row=8, column=3)


    #FileFormat
    Format = { '.txt','.csv'}
    Formatvar.set('') # set the default option
    FileFormatMenu = OptionMenu(GUIFrame, Formatvar, *Format)
    Label(GUIFrame, text="Choose a Format ").grid(row = 8, column = 4)
    FileFormatMenu.grid(row = 8, column =5)


    #Generate button
    GenerateButton = Button(GUIFrame, text="Generate",command=generateSQL).grid(row=7, column=5)
    ClearButton = Button(GUIFrame, text="Clear",command=clearSQL).grid(row=7, column=6)

     
    root.mainloop()

def clearSQL():
    Condvar.set('')
    Valuevar.set('')
    Colvar.set('')
    Filevar.set('')
    Formatvar.set('')
    
    
def generateSQL():

    try:
        Val_1="Validating Conditions"
        DB.InsertLogs(Val_1)
        if Colvar.get() == "":
            tkinter.messagebox.showinfo("Error", "Choose a Column to Continue")
            DB.InsertExceptionStmtTable("Column Empty","Generate Report - generateSQL")
        elif Valuevar.get() == "":
            tkinter.messagebox.showinfo("Error", "Choose a Value to Extract Report")
            DB.InsertExceptionStmtTable("Value Empty","Generate Report - generateSQL")
        elif Filevar.get() == "":
            tkinter.messagebox.showinfo("Error", "Choose a FileName for the Report")
            DB.InsertExceptionStmtTable("File Name","Generate Report - generateSQL")
        elif Formatvar.get() == "":
            tkinter.messagebox.showinfo("Error", "Choose a FileName Format for the Report")
            DB.InsertExceptionStmtTable("File Format Empty","Generate Report - generateSQL")
        elif Condvar.get()=="":
            tkinter.messagebox.showinfo("Error", "Choose a Condition")
            DB.InsertExceptionStmtTable("Condition Empty","Generate Report - generateSQL")
        else:
            Val_1="Generating SQL for Qualitative Values"
            DB.InsertLogs(Val_1)
            ## Append necessary conditions for the SQL statment
            ## If Qualitative Values are Chosen
            print("I'm in Else Part")
            if Colvar.get() in strConversion:
                Condvar.set("")
                Final_Val = directory+Filevar.get()+Formatvar.get()
                ColCheck = Colvar.get()
                Value=Valuevar.get()
                if str(ColCheck) in strConversion: #Refer Document for explanation
                    Value = "'%"+Valuevar.get().capitalize()+"%'"
                    DynamicSQL = SQLStatement +Colvar.get() +" LIKE "+ Value +""
                    print(DynamicSQL)
                    OpenDBandGenerate(Final_Val,DynamicSQL)
                else:
                    DynamicSQL = SQLStatement +Colvar.get() +" " +Condvar.get()+ " " + Value
                    print(DynamicSQL)
                    OpenDBandGenerate(Final_Val,DynamicSQL)
                
            else:
                ## If Quantitative Values are Chosen
                Val_1="Generating SQL for Quantitative Values"
                DB.InsertLogs(Val_1)
                
                Final_Val = directory+Filevar.get()+Formatvar.get()
                ColCheck = Colvar.get()
                
                print(ColCheck)
                Value=Valuevar.get()
                if str(ColCheck) in strConversion:
                    Value = "'%"+Valuevar.get().capitalize()+"%'"
                    DynamicSQL = SQLStatement +Colvar.get() +" LIKE "+ Value +""
                    print(DynamicSQL)
                    OpenDBandGenerate(Final_Val,DynamicSQL)
                else:
                    DynamicSQL = SQLStatement +Colvar.get() +" " +Condvar.get()+ " " + Value
                    print(DynamicSQL)
                    OpenDBandGenerate(Final_Val,DynamicSQL)
                    
    except Exception as e:
        print(e)
        DB.InsertExceptionStmtTable(e,"Generate Report - generateSQL")


##Generate SQL and Records
def OpenDBandGenerate(Final_Val,DynamicSQL):
    try:
        print("Passing here")
        Val_1="Generating SQL Records"
        DB.InsertLogs(Val_1)
        conn = DB.OpenConnection()
        c = conn.cursor()
        c.execute(DynamicSQL)
        rows = c.fetchall()
        print("length is",len(rows))
        if len(rows) ==0:
            tkinter.messagebox.showinfo("No Records", "No Records avaiable for this search")
            DB.InsertExceptionStmtTable("No Records avaiable for this search","Generate Report - OpenDBandGenerate")
        else:
            Val_1="Writing Records"
            DB.InsertLogs(Val_1)
            with open(Final_Val,"w",encoding='utf-8', newline = '' ) as f:
                writer = csv.writer(f,lineterminator='\n')
                writer.writerow(ColValues)
                for row in rows:
                    print(str(list(row)))
                    writer.writerow(list(row))
    except Exception as e:
        print(e)
        DB.InsertExceptionStmtTable(e,"Generate Report - OpenDBandGenerate")
    
    
# buildFrame()
