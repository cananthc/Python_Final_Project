#############################################################################
# Author     : Anantharaman Chandar                                         #
# CWID       : A20403439                                                    #
# Course     : ITMD 513 Open Source Programming Final Project               #
# Instructor : James Papademas                                              #
# Description: This script is used for creating a new account for the       #
#              user                                                     #
#                                                                           #                      
#                                                                           #
#                                                                           #
#############################################################################


#Import necessary Libraries
import tkinter.messagebox,re,hashlib

#Import necessary modules from the libraries 
from tkinter import *

#Import Necessary Filels
import DB_Objects as DB




#Registration Function
def registration():
    Val_1="Opening Registration GUI"
    DB.InsertLogs(Val_1)
    global finame,Conpwd,pwd,Number, emailname,root
    root = Tk()
    root.title('Registration Page')
    root.resizable(width=FALSE, height=FALSE)
    root.geometry('400x400')
    
    

    GUIFrame = Frame(root)       # add a row of buttons
    GUIFrame.grid(row=20,column=20)
    
    Heading = Label(GUIFrame, text = "Welcome To FIFA 18 Registration Page").grid(row=0, column=2)  

    #Name
    FnameLabel = Label(GUIFrame, text = "First Name").grid(row=2, column=1)
    finame = StringVar(GUIFrame)
    fname = Entry(GUIFrame, textvariable=finame).grid(row=2,column=2)

    #Email_id
    Email = Label(GUIFrame, text = "Email").grid(row=3, column=1)
    emailname = StringVar(GUIFrame)
    EmailTexbox = Entry(GUIFrame, textvariable=emailname).grid(row=3,column=2)

    #Password
    Password = Label(GUIFrame, text="Password").grid(row=4, column=1)
    pwd=StringVar(GUIFrame)
    password = Entry(GUIFrame,show='*', textvariable=pwd).grid(row=4,column=2)

    #Confirm Password
    ConPassword = Label(GUIFrame, text="Confirm Password").grid(row=5, column=1)
    Conpwd=StringVar(GUIFrame)
    Conpassword = Entry(GUIFrame,show='*', textvariable=Conpwd).grid(row=5,column=2)

    #Access Code
    NumberLabel = Label(GUIFrame, text = "Enter 4 Digit Code").grid(row=6, column=1)
    Number = StringVar(GUIFrame)
    NumberTexbox = Entry(GUIFrame, textvariable=Number).grid(row=6,column=2)

    #Register/Back/Clear
    Registerbut = Button(GUIFrame,text=" Register  ",command=Validations ).grid(row=8,column=1)
    BackButton = Button(GUIFrame,text=" Back ").grid(row=8, column=2)
    ClearButton = Button(GUIFrame,text=" Clear ",command=clearButton).grid(row=8, column=3)


#Sign up Validations
def Validations():
    Val_1="Register User Validations"
    DB.InsertLogs(Val_1)
    print(finame.get(),Conpwd.get(),pwd.get(),Number.get(),emailname.get())
    #Name Validation
    if finame.get()=="":
        tkinter.messagebox.showinfo("Error","Name is Empty")
        DB.InsertExceptionStmtTable("Name is Empty","Registration - Validations")

    #E-Mail Validation    
    elif emailname.get()=="":
        tkinter.messagebox.showinfo("Error","Email is Empty")
        DB.InsertExceptionStmtTable("Email is Empty","Registration - Validations")
        
    elif not re.search("@",emailname.get()):
        tkinter.messagebox.showinfo("Error","Email is not Valid")
        DB.InsertExceptionStmtTable("Email is not Valid","Registration - Validations")
        
    elif not re.search(".com",emailname.get()):
        tkinter.messagebox.showinfo("Error","Email is not Valid")
        DB.InsertExceptionStmtTable("Email is not Valid","Registration - Validations")

    #Password Validation     
    elif pwd.get()=="":
        tkinter.messagebox.showinfo("Error","Password is Empty")
        DB.InsertExceptionStmtTable("Password is Empty","Registration - Validations")
        
    elif Conpwd.get()=="":
        tkinter.messagebox.showinfo("Error","Confirm Password is Empty")
        DB.InsertExceptionStmtTable("Confirm Password is Empty","Registration - Validations")

    #4 Digit Validation     
    elif Number.get()=="":
        tkinter.messagebox.showinfo("Error","Access Number is Empty")
        DB.InsertExceptionStmtTable("Access Number is Empty","Registration - Validations")
    elif not Number.get().isdigit():
        tkinter.messagebox.showinfo("Error","Access Number Should be a Number")
        DB.InsertExceptionStmtTable("Access Number Should be a Number","Registration - Validations")

    #Password Validation     
    elif len(pwd.get()) < 8:
        tkinter.messagebox.showinfo("Error","Password must be Greater than 8 characters")
        DB.InsertExceptionStmtTable("Password must be Greater than 8 characters","Registration - Validations")
        
    elif len(Conpwd.get()) < 8:
        tkinter.messagebox.showinfo("Error","Confirm Password must be Greater than 8 characters")
        DB.InsertExceptionStmtTable("Confirm Password must be Greater than 8 characters","Registration - Validations")
        
    elif not re.search('[0-9]',pwd.get()):
        tkinter.messagebox.showinfo("Error","Make sure your Password has 1 Number atleast")
        DB.InsertExceptionStmtTable("Make sure your Password has 1 Number atleast","Registration - Validations")
        
    elif not re.search('[A-Z]',pwd.get()):
        tkinter.messagebox.showinfo("Error","Make sure your Password has 1 Upper character atleast")
        DB.InsertExceptionStmtTable("Make sure your Password has 1 Upper character atleast","Registration - Validations")
        
    elif pwd.get() != Conpwd.get():
        tkinter.messagebox.showinfo("Error","Password Mismatch")
        DB.InsertExceptionStmtTable("Password Mismatch","Registration - Validations")

    #Number Validation     
    elif len(Number.get()) !=4:
        tkinter.messagebox.showinfo("Error","Pin Length Mismatch")
        DB.InsertExceptionStmtTable("Pin Length Mismatch","Registration - Validations")
    else:
        Val_1="Validations are passed"
        DB.InsertLogs(Val_1)
        RegisterUser(finame.get(),Conpwd.get(),pwd.get(),Number.get(),emailname.get())

#Create login once Validations are passed                     
def RegisterUser(finame,Conpwd,pwd,Number,emailname):
    Pass_1 = hashlib.md5(pwd.encode())
    Pass_1 = Pass_1.hexdigest()
    print(Pass_1)
    Con_Pass = hashlib.md5(pwd.encode())
    Con_Pass = Con_Pass.hexdigest()
    print(Con_Pass)
    try:
        Val_1="Open DB and Create Login"
        DB.InsertLogs(Val_1)    
        conn = DB.OpenConnection()
        c = conn.cursor()
        c.execute(DB.InsertLoginTableStmt,(str(finame),str(Pass_1),str(Con_Pass),str(emailname),Number,'Y'))
        conn.commit()
        tkinter.messagebox.showinfo("Success","Login has been created. Proceed to Login page to View FIFA 18 Data Visualizations ")
        root.destroy()
        
    except Exception as e:
        print(e)
        tkinter.messagebox.showinfo("Error",e)
        DB.InsertExceptionStmtTable(e,"Registration - RegisterUser")
        
def clearButton():
    root.destroy()
    registration()


