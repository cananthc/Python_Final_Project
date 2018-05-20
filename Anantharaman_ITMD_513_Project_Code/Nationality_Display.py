#############################################################################
# Author     : Anantharaman Chandar                                         #
# CWID       : A20403439                                                    #
# Course     : ITMD 513 Open Source Programming Final Project               #
# Instructor : James Papademas                                              #
# Description: This script is used for extracting the nationalities         #
#              from the file and incrementing the count                     #
#                                                                           #                      
#                                                                           #
#                                                                           #
#############################################################################


#Import necessary Libraries
import matplotlib.pyplot as plt

#Import other files
import Extract_Records as File
import DB_Objects as DB


#Extracts Nationalities record and count of each nationality
def Nationality_Selection():
    try:
        Val_1="Extracting Records"
        DB.InsertLogs(Val_1)
        
        Countries=[]
        Players_Data=[]
        #File.extractRecords()
        Players_Data = File.extractRecords()
        print("Completed Nationality_Display")
        #Countries=[] #17979
        print(len(Players_Data))
        
        Val_1="Appending Nationalities to a list"
        DB.InsertLogs(Val_1)

        #Append countries alone from the file
        for i in range(0,len(Players_Data)):
            Countries.append(Players_Data[i][4]) #Column index of nationalities
        print("Initalizing Final_Count")
        Final_Count={}
        print(len(Countries))
        
        Val_1="Eliminating the Duplicates"
        DB.InsertLogs(Val_1)
        #Remove Duplicates and populate it to a new list
        Countries_New = list(set(Countries))
        print(len(Countries_New))

        Val_1="Appending values to 0 for all the nationalities"
        DB.InsertLogs(Val_1)
        #Update Value of all the distinct Nationalitis to 0
        for i in range(0,len(Countries_New)):
            j=0
            Name = Countries_New[i]
            Final_Count[Name]=j
        #print(Players_Data[0][0])
        x=0

        Val_1="Update the count for all the nationalities"
        DB.InsertLogs(Val_1)
        #Update the count of each Nationality which was updated to 0 earlier
        for i in range(0,len(Players_Data)):
            for j in range(0,len(Countries_New)):
                if Players_Data[i][4] ==Countries_New[j]:
                    x+=1
                    Final_Count[str(Countries_New[j])]=Final_Count.get(str(Countries_New[j]))+1

        #Converting List to Dictionary
        print("Convert Dict to List")        
        #print(Final_Count)
        Val_1="Converting list to Dictionary"
        DB.InsertLogs(Val_1)        
        Countries=list(Final_Count.items())

        print("Success")
        return Final_Count
        
    except Exception as e:
        print(e)
        DB.InsertExceptionStmtTable(e,"Nationality_Display - Nationality_Selection")





#Nationality_Selection()
