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
import tkinter.messagebox
import hashlib, sys,os

#Import Necessary variables from the Libraries
from tkinter import *

#Import Other Files
import Registration as RS
import DB_Objects as DB
import Build_Frame as BF


#Validate Login
def login_Validate(username,passvar):
    Val_1="Validating UserName and Password"
    DB.InsertLogs(Val_1)
    if username.get()!="" and passvar.get()!="":
        dbname,dbpass=DB.Uservalidations(username.get(),passvar.get())
        hashpass=hashlib.md5(passvar.get().encode())
        h=hashpass.hexdigest()

        if dbname==username.get() and dbpass==h :
            root.destroy()
            BF.buildFrame()     
            
        else:
            tkinter.messagebox.showinfo("Login- Failed", "Username-Password pair does not exist")
            DB.InsertExceptionStmtTable("Username-Password pair does not exist","Login - login_Validate")
            passvar.set('')
            username.set('')
    else:
        tkinter.messagebox.showinfo("Login- Failed", "Fields Empty")
        DB.InsertExceptionStmtTable("Fields Empty","Login - login_Validate")
		
#Validate Login		
def buildFrame () :             #Application interface
    Val_1="Generating GUI"
    DB.InsertLogs(Val_1)
    
    global username, passvar, root,UserLabel
    root=Tk()
    root.title('Fifa18 Data Visualization')
    root.resizable(width=FALSE, height=FALSE)
    root.geometry('1000x650')


    GUIFrame = Frame(root)
    GUIFrame.pack(side=TOP)

    #Heading
    Heading = Label(GUIFrame, text = "Welcome To FIFA 18 Data Visualization").grid(row=0, column=1)  

    #Email Id
    UserLabel = Label(GUIFrame, text="Email_Id:").grid(row=4, column=0, sticky=W,pady=10)
    username = StringVar(GUIFrame)
    name = Entry(GUIFrame, textvariable=username)
    name.grid(row=4, column=1, sticky=W,pady=10)

    #Password
    PasswordLabel= Label(GUIFrame, text="Password:").grid(row=5, column=0, sticky=W,pady=10)
    passvar= StringVar()
    password= Entry(GUIFrame,show='*', textvariable=passvar)
    password.grid(row=5, column=1, sticky=W,pady=10)
	
    #Login Button
    Loginbtn = Button(GUIFrame,text=" Login  ",command=lambda: login_Validate(username,passvar)).grid(row=6, column=0)

    
    ##Sign up button
    Signupbtn = Button(GUIFrame,text=" Sign Up!",command=RS.registration)
    Signupbtn.grid(row=6, column=1)

    ##Exit Button
    Exitbtn = Button(GUIFrame,text=" Exit ",width=7,command=exit)
    Exitbtn.grid(row=6, column=2);
 
             
    return root

#Main Function
try:
    buildFrame()
except Exception as e:
    DB.InsertExceptionStmtTable(e,"Login - BuildFrame")
