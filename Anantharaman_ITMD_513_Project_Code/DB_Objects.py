import sqlite3, datetime
import sys,time,io,os,tkinter.messagebox
from tkinter import *

import Extract_Records as ER
import Nationality_Display as ND

result=list()
##Declare necessary variables
DBFile = "AC_FIFA18.db"

CreateLogTable = "CREATE TABLE AC_LOG_DETAILS ( \
                 ID INTEGER PRIMARY KEY AUTOINCREMENT,   Start_Time  TIME     DEFAULT (CURRENT_TIMESTAMP), \
                 Description TEXT,     End_Time    DATETIME DEFAULT (CURRENT_TIMESTAMP) ); "


InsertLogStmts = "INSERT INTO AC_LOG_DETAILS (Description) VALUES (?)"


CreateExceptionTableStmt = "CREATE TABLE AC_FIFA18_EXCEPTION ( \
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,           Exception_Details TEXT(300), \
                            Screen TEXT,                                    Date TIME     DEFAULT (CURRENT_TIMESTAMP)    );"

InsertExceptionStmts = "INSERT INTO AC_FIFA18_EXCEPTION (Exception_Details, Screen) VALUES (?,?)"

 
CreateMasterDataTableStmt = "CREATE TABLE AC_FIFA18_MASTERDATA (  \
    SNO                INTEGER     PRIMARY KEY NOT NULL, \
    Name               TEXT (50),  Age                INTEGER (3),      Nationality        TEXT (20),    Overall            INTEGER, \
    Potential          INTEGER,    Club               TEXT (30),        Value              INTEGER,      Wage               INTEGER, \
    Acceleration       INTEGER,    Aggression         INTEGER,          Agility            INTEGER,      Balance            INTEGER, \
    BallControl        INTEGER,    Composure          INTEGER,          Crossing           INTEGER,      Curve              INTEGER, \
    Dribbling          INTEGER,    Finishing          INTEGER,          FreeKickAccuracy   INTEGER,      GKDiving           INTEGER, \
    GKHandling         INTEGER,    GKKicking          INTEGER,          GKPositioning      INTEGER,      GKReflexes         INTEGER, \
    HeadingAccuracy    INTEGER,    Interception       INTEGER,          Jumping            INTEGER,      LongPassing        INTEGER, \
    LongShots          INTEGER,    Marking            INTEGER,          Penalties          INTEGER,      Positioning        INTEGER, \
    Reaction           INTEGER,    ShortPassing       INTEGER,          ShotPower          INTEGER,      SlidingTackle      INTEGER, \
    SprintSpeed        INTEGER,    Stamina            INTEGER,          StandingTackle     INTEGER,      Strength           INTEGER, \
    Vision             INTEGER,    Volleys            INTEGER,          CAM                INTEGER,      CB                 INTEGER, \
    CDM                INTEGER,    CF                 INTEGER,          CM                 INTEGER,      LAM                INTEGER, \
    LB                 INTEGER,    LCB                INTEGER,          LCM                INTEGER,      LDM                INTEGER, \
    LF                 INTEGER,    LM                 INTEGER,          LS                 INTEGER,      LW                 INTEGER, \
    LWB                INTEGER,    PreferredPositions TEXT,             RAM                INTEGER,      RB                 INTEGER, \
    RCB                INTEGER,    RCM                INTEGER,          RDM                INTEGER,      RF                 INTEGER, \
    RM                 INTEGER,    RS                 INTEGER,          RW                 INTEGER,      RWB                INTEGER, \
    ST                 INTEGER );"

##70 Values
InsertMasterDataTableStmt = "INSERT INTO AC_FIFA18_MASTERDATA \
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?); "



CreateReadTableStmt = "CREATE TABLE AC_FIFA18_READ_DATA (  \
    SNO                INTEGER     PRIMARY KEY NOT NULL, \
    Name               TEXT (50),  Age                INTEGER (3),      Nationality        TEXT (20),    Overall            INTEGER, \
    Potential          INTEGER,    Club               TEXT (30),        Value              INTEGER,      Wage               INTEGER, \
    Acceleration       INTEGER,    Aggression         INTEGER,          Agility            INTEGER,      Balance            INTEGER, \
    BallControl        INTEGER,    Composure          INTEGER,          Crossing           INTEGER,      Curve              INTEGER, \
    Dribbling          INTEGER,    Finishing          INTEGER,          FreeKickAccuracy   INTEGER,      GKDiving           INTEGER, \
    GKHandling         INTEGER,    GKKicking          INTEGER,          GKPositioning      INTEGER,      GKReflexes         INTEGER, \
    HeadingAccuracy    INTEGER,    Interception       INTEGER,          Jumping            INTEGER,      LongPassing        INTEGER, \
    LongShots          INTEGER,    Marking            INTEGER,          Penalties          INTEGER,      Positioning        INTEGER, \
    Reaction           INTEGER,    ShortPassing       INTEGER,          ShotPower          INTEGER,      SlidingTackle      INTEGER, \
    SprintSpeed        INTEGER,    Stamina            INTEGER,          StandingTackle     INTEGER,      Strength           INTEGER, \
    Vision             INTEGER,    Volleys            INTEGER,          CAM                INTEGER,      CB                 INTEGER, \
    CDM                INTEGER,    CF                 INTEGER,          CM                 INTEGER,      LAM                INTEGER, \
    LB                 INTEGER,    LCB                INTEGER,          LCM                INTEGER,      LDM                INTEGER, \
    LF                 INTEGER,    LM                 INTEGER,          LS                 INTEGER,      LW                 INTEGER, \
    LWB                INTEGER,    PreferredPositions TEXT,             RAM                INTEGER,      RB                 INTEGER, \
    RCB                INTEGER,    RCM                INTEGER,          RDM                INTEGER,      RF                 INTEGER, \
    RM                 INTEGER,    RS                 INTEGER,          RW                 INTEGER,      RWB                INTEGER, \
    ST                 INTEGER );"


InsertReadDataTableStmt = "INSERT INTO AC_FIFA18_READ_DATA \
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?); "

CreateAdhocRequestTableStmt = "CREATE TABLE AC_FIFA18_ADHOC_REQUEST ( \
                               ID INTEGER PRIMARY KEY AUTOINCREMENT,         Description TEXT,              Created_By TEXT \
                               SCREEN TEXT,                                 DATE TIME DEFAULT (CURRENT_TIMESTAMP) )"

CreateLoginTableStmt = "CREATE TABLE AC_FIFA18_LOGIN ( \
    Name             TEXT,        Password         TEXT,    Confirm_Password TEXT,           Email_Id         TEXT     PRIMARY KEY, \
    Pin_Number       INTEGER,     Created_On       DATETIME DEFAULT (CURRENT_TIMESTAMP),     LAST_LOGIN       TEXT, \
    LAST_LOGOUT      TEXT,     STATUS           TEXT (1) );"

InsertLoginTableStmt = "INSERT INTO AC_FIFA18_LOGIN (NAME, Password, Confirm_Password, Email_Id, Pin_Number, Status) VALUES (?,?,?,?,?,?);" 

SelectLoginStmt = "SELECT EMAIL_ID, Password from AC_FIFA18_LOGIN WHERE EMAIL_ID = "



CreateNullValuesTableStmt = "CREATE TABLE AC_NULLL_VALUES (\
                             ID INTEGER,         Null_Column_Name TEXT,             Screen TEXT,            Date TEXT );"


CreateFormationTableStmt = "CREATE TABLE AC_FIFA18_FORMATIONS (\
                            Formation TEX PRIMARY KEY, Description TEXT, DEFENDERS INTEGER, MIDFIELDERS INTEGERS, ATTACKERS INTEGER ); "

InsertFormationTableStmt = "INSERT INTO AC_FIFA18_FORMATIONS VALUES (?,?,?,?,?);"

Formation = [
              ['4-3-2-1','Defend',4,5,1],
              ['5-3-2','Ultra-Defend',5,3,2],
              ['4-3-3','Natural',4,3,3],
              ['4-1-2-1-2','Attack',4,4,2],
              ['3-5-2','Ultra-Attack',3,5,2]
            ]


CreateDistinctCountriesTable = "CREATE TABLE AC_FIFA18_COUNTRIES ( Countries TEXT PRIMARY KEY );"

InsertCountriesStmt = "INSERT INTO AC_FIFA18_COUNTRIES VALUES (?) ;"
#Not to be changed
########################################################################
def OpenConnection():
    try:
        conn = sqlite3.connect(DBFile)
        print ("Opened database successfully");
        return conn
    except Exception as e:
        print(e)

    return None
#########################################################################


#########################################################################
#Table Creation
def CreateTable(TableName,TableSQL):
    try:
        Val_1 = "Connection Check For "+ str(TableName)
        print(Val_1)
        InsertLogStmt(Val_1)
        conn = OpenConnection()
        if conn is not None:
            c = conn.cursor()
            Val_2 = "Creation Started For " + str(TableName)
            InsertLogStmt(Val_2)
            c.execute(TableSQL)
            Val_3 = " Table Creation Success For " + str(TableName)
            InsertLogStmt(Val_3)
        else:
            Val_4 = "Table Not Created For " + str(TableName)
            InsertLogStmt(Val_4)
            print("Error")
    except Exception as e:
        InsertExceptionStmts(e,"DB_Objects")
############################################################################

##########################################################################
#Insert Command into DB
        
def InsertLogs(Value):
    try:
        conn = OpenConnection()
        with conn:
            c = conn.cursor()
            c.execute(InsertLogStmts,[Value])
    except Exception as e:
        print(e)

def InsertExceptionStmtTable(Value,Screen):
    try:
        print(Value)
        print(Screen)
        conn = OpenConnection()
        with conn:
            c = conn.cursor()
            c.execute(InsertExceptionStmts,(str(Value),str(Screen)))
    except Exception as e:
        print(e)

def InsertMasterData():
    try:
            
        try:
            Val_1 = "Extracting Records from the other ER.extractRecords"
            InsertLogs(Val_1)
            Players_Data = ER.extractRecords()
            Val_2 = "Extraction Completed from ER.extractRecords"
            InsertLogs(Val_2)
            print(len(Players_Data))
            Val_3 = "Connection check before insert"
            InsertLogs(Val_3)
            conn = OpenConnection()
            with conn:
                Val_4 = "Connection check success before insert"
                InsertLogs(Val_4)
                Val_5 = "Insertion Started for Master Data Table "
                InsertLogs(Val_5)
                for i in range(0,len(Players_Data)):
                    c = conn.cursor()
                    c.execute(InsertMasterDataTableStmt,(
                        Players_Data[i][0],   Players_Data[i][1],  Players_Data[i][2],  Players_Data[i][4],    Players_Data[i][6],
                        Players_Data[i][7],   Players_Data[i][8],  Players_Data[i][10], Players_Data[i][11],   Players_Data[i][13],
                        Players_Data[i][14],  Players_Data[i][15], Players_Data[i][16], Players_Data[i][17],   Players_Data[i][18],
                        Players_Data[i][19],  Players_Data[i][20], Players_Data[i][21], Players_Data[i][22],   Players_Data[i][23],
                        Players_Data[i][24],  Players_Data[i][25], Players_Data[i][26], Players_Data[i][27],   Players_Data[i][28],
                        Players_Data[i][29],  Players_Data[i][30], Players_Data[i][31], Players_Data[i][32],   Players_Data[i][33],
                        Players_Data[i][34],  Players_Data[i][35], Players_Data[i][36], Players_Data[i][37],   Players_Data[i][38],
                        Players_Data[i][39],  Players_Data[i][40], Players_Data[i][41], Players_Data[i][42],   Players_Data[i][43],
                        Players_Data[i][44],  Players_Data[i][45], Players_Data[i][46], Players_Data[i][47],   Players_Data[i][48],
                        Players_Data[i][49],  Players_Data[i][50], Players_Data[i][51], Players_Data[i][53],   Players_Data[i][54],
                        Players_Data[i][55],  Players_Data[i][56], Players_Data[i][57], Players_Data[i][58],   Players_Data[i][59],
                        Players_Data[i][60],  Players_Data[i][61], Players_Data[i][62], Players_Data[i][63],   Players_Data[i][64],
                        Players_Data[i][65],  Players_Data[i][66], Players_Data[i][67], Players_Data[i][68],   Players_Data[i][69],
                        Players_Data[i][70],  Players_Data[i][71], Players_Data[i][72], Players_Data[i][73],   Players_Data[i][74]))
            
            Val_6 = "Insertion Completed for Master Data Table Stmt "
            InsertLogs(Val_6)    
            conn.close()
            #c.execute(InsertMasterDataTableStmt,
        except Exception as e:
                  InsertExceptionStmts(e,"Insert Master Data Table")
    except  Exception as e:
        print(e)
        InsertExceptionStmts(e,"Master Data Table Outer Exception")
############################################################################

def InsertReadData():
    try:
            
        try:
            Val_1 = "Extracting Records from the other ER.extractRecords"
            InsertLogs(Val_1)
            Players_Data = ER.extractRecords()
            Val_2 = "Extraction Completed from ER.extractRecords"
            InsertLogs(Val_2)
            print(len(Players_Data))
            Val_3 = "Connection check before insert"
            InsertLogs(Val_3)
            conn = OpenConnection()
            with conn:
                Val_4 = "Connection check success before insert"
                InsertLogs(Val_4)
                Val_5 = "Insertion Started for Read Data Table "
                InsertLogs(Val_5)
                for i in range(0,len(Players_Data)):
                    c = conn.cursor()
                    c.execute(InsertReadDataTableStmt,(
                        Players_Data[i][0],   Players_Data[i][1],  Players_Data[i][2],  Players_Data[i][4],    Players_Data[i][6],
                        Players_Data[i][7],   Players_Data[i][8],  Players_Data[i][10], Players_Data[i][11],   Players_Data[i][13],
                        Players_Data[i][14],  Players_Data[i][15], Players_Data[i][16], Players_Data[i][17],   Players_Data[i][18],
                        Players_Data[i][19],  Players_Data[i][20], Players_Data[i][21], Players_Data[i][22],   Players_Data[i][23],
                        Players_Data[i][24],  Players_Data[i][25], Players_Data[i][26], Players_Data[i][27],   Players_Data[i][28],
                        Players_Data[i][29],  Players_Data[i][30], Players_Data[i][31], Players_Data[i][32],   Players_Data[i][33],
                        Players_Data[i][34],  Players_Data[i][35], Players_Data[i][36], Players_Data[i][37],   Players_Data[i][38],
                        Players_Data[i][39],  Players_Data[i][40], Players_Data[i][41], Players_Data[i][42],   Players_Data[i][43],
                        Players_Data[i][44],  Players_Data[i][45], Players_Data[i][46], Players_Data[i][47],   Players_Data[i][48],
                        Players_Data[i][49],  Players_Data[i][50], Players_Data[i][51], Players_Data[i][53],   Players_Data[i][54],
                        Players_Data[i][55],  Players_Data[i][56], Players_Data[i][57], Players_Data[i][58],   Players_Data[i][59],
                        Players_Data[i][60],  Players_Data[i][61], Players_Data[i][62], Players_Data[i][63],   Players_Data[i][64],
                        Players_Data[i][65],  Players_Data[i][66], Players_Data[i][67], Players_Data[i][68],   Players_Data[i][69],
                        Players_Data[i][70],  Players_Data[i][71], Players_Data[i][72], Players_Data[i][73],   Players_Data[i][74]))
                
            Val_6 = "Insertion Completed for Read Data Table Stmt "
            InsertLogs(str(Val_6))
            conn.close()
            
        except Exception as e:
                  InsertExceptionStmts(e,"Insert Read Data Table")
    except  Exception as e:
        print(e)
        InsertExceptionStmts(e,"Read Data Table Outer Exception")

#############################################################################################

def InsertFormation():
    try:
        try:
            Val_1 = "Connection check before insert for Formation Table"
            InsertLogs(Val_1)
            conn = OpenConnection()
            with conn:
                Val_2 = "Connection check success before insert for Formation Table"
                InsertLogs(Val_2)
                Val_3 = "Insertion Started for Formation Table "
                InsertLogStmt(Val_3)
                for i in range(0,len(Formation)):
                    c = conn.cursor()
                    c.execute(InsertFormationTableStmt,(Formation[i][0],Formation[i][1],Formation[i][2],Formation[i][3],Formation[i][4]))
                Val_4 = "Insertion Completed for Formation Table "
                InsertLogs(Val_4)
                #conn.close()
        except Exception as e:
            InsertExceptionStmts(e,"Formation Data Table")
    except  Exception as es:
        InsertExceptionStmts(es,"Formation Table Outer Exception")
                    
                
def InsertCountries():
    try:
        try:
            Val_1 = "Extracting Countries "
            Countries = ND.Nationality_Selection()
            InsertLogs(Val_1)
            Val_2 = "Extraction Completed For countries"
            InsertLogs(Val_2)
            conn = OpenConnection()
            c = conn.cursor()
            Val_3 = "Connection check before insert for Formation Table"
            InsertLogs(Val_3)
            with conn:
                Val_4 = "Connection check success before insert for Formation Table"
                InsertLogs(Val_4)
                Val_5 = "Insertion Started for Formation Table "
                InsertLogs(Val_5)
                for i in Countries.keys():
                    c.execute(InsertCountriesStmt,[i])
                Val_6 = "Insertion Completed for Countries Table "
                InsertLogs(Val_6)
        except Exception as e:
             InsertExceptionStmts(e,"Countries Data Table Exception")
    except  Exception as es:
        InsertExceptionStmts(es,"Countries Table Outer Exception")
                    

                
def Uservalidations(name,password):
    conn = OpenConnection ()
    result=[]
    if conn is not None:
        try:
            c = conn.cursor()
            Email_ID = name
            Fetch = SelectLoginStmt+"'"+Email_ID+"';"
            print(Fetch)
            c.execute(Fetch)
            result=c.fetchall()
            print(result)    

        except Exception as e:
            conn.rollback()
            print ("Error occurred. Rolback sucessful!",e)          
    if result==[]:
        return('Null','Null')
    else:
        return(result[0][0],result[0][1])
            
        
    
    
        
###Insert your Reference Table Name and SQL Command 
##try:
##    
##   CreateTable("Countries Table",CreateDistinctCountriesTable )
##except Exception as e:
##    InsertExceptionStmts(e,"DB_Objects")

#InsertReadData()
#InsertMasterData()
#InsertFormation()
#InsertCountries()
#Countires = ND.Nationality_Selection()
#print(Countires.keys())
#for i in Countires.keys():
   # print(i)
