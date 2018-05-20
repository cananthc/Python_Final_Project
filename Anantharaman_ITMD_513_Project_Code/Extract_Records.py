#############################################################################
# Author     : Anantharaman Chandar                                         #
# CWID       : A20403439                                                    #
# Course     : ITMD 513 Open Source Programming Final Project               #
# Instructor : James Papademas                                              #
# Description: This script reads data from the csv file and gives the       #
#              output as a list when the function is called                 #
#                                                                           #                      
#                                                                           #
#                                                                           #
#############################################################################

#Import Necessary Libraries
import csv,sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


#Import Specific modules from the libraries
from importlib import reload

#Import other files
import DB_Objects as DB

reload(sys)  
sys.getdefaultencoding()
plt.rcdefaults()

    

data=[]
ColNames=[]
Players_Data=[]
Source_Data = 'Football_Data.csv'

#Extract Records
def extractRecords():
    try:
        Val_1="Extract Records from the source Data"
        DB.InsertLogs(Val_1)           
        data=[]
        print("Executing Extract Records")
        with open(Source_Data,"r",encoding="utf8") as DataSet:
            printData =csv.reader(DataSet,delimiter=' ')
            for row in printData:
                data.append(row)
            
            Val_1="Split Records"
            DB.InsertLogs(Val_1)                 
            #Splitting ColNames into a seperate list
            for x in data[0]:
                x = x.split(",")
                ColNames.append(x)
                
            #Deleting the first row becuase we have written it in a seperate list
            del data[0]
            
            Players_Data=[]
            print("DAta", len(data))
            print("Before appending", len(Players_Data))
            print("I'm Here Now in Extract Recorods")
            Val_1="Splitting Player Attributes into a seperate list based on the whitespaces"
            DB.InsertLogs(Val_1)
            #Splitting Player Attributes into a seperate list based on the whitespaces
            for i in range(0,len(data)-1):
                if len(data[i]) == 8:
                    x =(data[i][0],data[i][1],data[i][2],data[i][3],data[i][4],data[i][5],data[i][6],data[i][7])
                    y =(x[0] +" " +x[1]+" "+x[2]+" "+x[3]+" "+x[4]+" "+x[5]+" "+x[6]+" "+x[7])
                    y = y.split(",")
                    Players_Data.append(y)
                    
                elif len(data[i]) == 7:
                    x =(data[i][0],data[i][1],data[i][2],data[i][3],data[i][4],data[i][5],data[i][6])
                    y =(x[0] +" " +x[1]+" "+x[2]+" "+x[3]+" "+x[4]+" "+x[5]+" "+x[6])
                    y = y.split(",")
                    Players_Data.append(y)
                    
                elif len(data[i]) == 6:
                    x =(data[i][0],data[i][1],data[i][2],data[i][3],data[i][4],data[i][5])
                    y =(x[0] +" " +x[1]+" "+x[2]+" "+x[3]+" "+x[4]+" "+x[5])
                    y = y.split(",")
                    Players_Data.append(y)
                    
                elif len(data[i]) == 5:
                    x =(data[i][0],data[i][1],data[i][2],data[i][3],data[i][4])
                    y =(x[0] +" " +x[1]+" "+x[2]+" "+x[3]+" "+x[4])
                    y = y.split(",")
                    Players_Data.append(y)
                    
                elif len(data[i]) == 4:
                    x =(data[i][0],data[i][1],data[i][2],data[i][3])
                    y =(x[0] +" " +x[1]+" "+x[2]+" "+x[3])
                    y = y.split(",")
                    Players_Data.append(y)
                elif len(data[i]) == 3:
                    x =(data[i][0],data[i][1],data[i][2])
                    y =(x[0] +" " +x[1]+" "+x[2])
                    y = y.split(",")
                    Players_Data.append(y)
                elif len(data[i]) == 2:
                    x =(data[i][0],data[i][1])
                    y =(x[0] +" " +x[1])
                    y = y.split(",")
                    Players_Data.append(y)
                elif len(data[i]) == 1:
                    x =(data[i][0])
                    y =(x[0])
                    y = y.split(",")
                    Players_Data.append(y)
                else:
                    #print("Not Empty")
                    print(data[i])
            
            print("Completed Extract of Records")
            print(len(data))
            print("Here in Extract Records",len(Players_Data))
            Val_1="Extract Completed"
            DB.InsertLogs(Val_1)
            return Players_Data
    except Exceptoion as e:
        DB.InsertExceptionStmtTable(e,"Extract Records - extractRecords")

#Extract Columns alone
def extractColumnNames():
    try:
        Val_1="Extract Columns"
        DB.InsertLogs(Val_1)       
        data=[]
        print("Executing Extract Records")
        with open(Source_Data,"r",encoding="utf8") as DataSet:
            printData =csv.reader(DataSet,delimiter=' ')
            for row in printData:
                data.append(row)
            print(data[0])
                
            #Splitting ColNames into a seperate list
            for x in data[0]:
                x = x.split(",")
                ColNames.append(x)
        return ColNames
        Val_1="Extract Columns Completed"
        DB.InsertLogs(Val_1)
    except Exception as e:
        DB.InsertExceptionStmtTable(e,"Extract Records - extractColumnNames")
        
#extractColumnNames()
