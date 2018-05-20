#############################################################################
# Author     : Anantharaman Chandar                                         #
# CWID       : A20403439                                                    #
# Course     : ITMD 513 Open Source Programming Final Project               #
# Instructor : James Papademas                                              #
# Description: This script gives you a bar char based on players age        #
#              based on the .csv file                                       #                      
#                                                                           #
#                                                                           #
#############################################################################


##Import Libraries needed
import sys,time,io,os,tkinter.messagebox,csv,sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#Import specifc modules from the libraries 
from tkinter import *
from importlib import reload

reload(sys)  
sys.getdefaultencoding()
plt.rcdefaults()

#Import other python files
import Extract_Records as File 
import DB_Objects as DB



#Selection Index
def selection () :
    print ("At %s of %d" % (select.curselection(), len(contactlist)))
    return int(select.curselection()[0])

#Classifies age of each players and groups it in a dictionary
def PlayersBasedOnAge():
    
    try:

        ##Log Statement
        Val_1="Started Age Distribution"
        DB.InsertLogs(Val_1)
        Players_Data = File.extractRecords() #Extract Record from the .csv file

        ##Declare variables for grouping players age
        Under10=0
        Under20=0
        Under30=0
        Under40=0
        Under50=0
        Undefined=0
        age=[]

        #Run through for loop, 2nd index value in the .csv file is the age
        
        for i in range(0,len(Players_Data)-1):
            #print(i)
            age.append(Players_Data[i][2])
        #print(age[0])

        #Group each age and increment the counter
        for i in age:
            if int(i)>=0 and int(i)<10:
                Under10= Under10+1
            elif int(i)>=10 and int(i)<20:
                Under20= Under20+1
            elif int(i)>=20 and int(i)<30:
                Under30= Under30+1
            elif int(i)>=30 and int(i)<40:
                Under40= Under40+1
            elif int(i)>=40 and int(i)<50:
                Under50= Under50+1
            else:
                Undefined=Undefined+1

        #Map it to the dictionary        
        Age_Dictionary={"Under10":Under10,"Under20":Under20,"Under30":Under30,"Under40":Under40,"Under50":Under50,"Undefined":Undefined}
        print(Age_Dictionary)


        ## Backgroud format
        colors = ['white',]
        plt.rcParams['axes.facecolor'] = '#AA0000'
        X_Axis = ('0-10', '10-20', '20-30', '30-40', '40-50', 'Undefined')
        y_pos = np.arange(len(X_Axis))
        plt.ylim(0, 20000)
        Age_Distribution = [Under10,Under20,Under30,Under40,Under50,Under10]

        ##v is y values, i is location for the legend
        for i,v in enumerate(Age_Distribution):
            plt.text(i-.25,v+100,str(v),fontweight='bold')
        plt.bar(y_pos, Age_Distribution, align='center',bottom=10,alpha=1,color=colors,edgecolor='black')
        plt.xticks(y_pos, X_Axis)
        font = 0
        plt.xlabel('Age Distribution')
        plt.ylabel('Total Players')
        plt.title('Age Classification')
        plt.show()
        
        Val_1="Completed Age Distribution"
        DB.InsertLogs(Val_1)
    except Exception as e:
        print("Error",e)
        DB.InsertExceptionStmtTable(e,"Age Screen")

#PlayersBasedOnAge()
