#############################################################################
# Author     : Anantharaman Chandar                                         #
# CWID       : A20403439                                                    #
# Course     : ITMD 513 Open Source Programming Final Project               #
# Instructor : James Papademas                                              #
# Description: This script appends exception details to a .txt file         #
#              and generates WordCloud                                      #
#                                                                           #                      
#                                                                           #
#                                                                           #
#############################################################################

#Import necessary Libraries
import matplotlib.pyplot as plt
import csv

#Import specific modules from the libraries
from wordcloud import WordCloud, STOPWORDS

#Import other files
import DB_Objects as DB


#Append the exceptions to a .txt file
def GenerateExceptionFile():
    try:
        Val_1="Opening connection to write the exception"
        DB.InsertLogs(Val_1)            
        conn = DB.OpenConnection()
        c = conn.cursor()
        c.execute("SELECT * FROM AC_FIFA18_EXCEPTION;")
        rows = c.fetchall()
        Val_1="Writing Records"
        DB.InsertLogs(Val_1)
        with open("Exception.txt","a",encoding='utf-8', newline = '' ) as f:
            writer = csv.writer(f,lineterminator='\n')
            for row in rows:
                #print(str(list(row)))
                writer.writerow(list(row))
        Val_1="Records are appended to the existing file"
        DB.InsertLogs(Val_1)  
        GenerateWordCloud()
    except Exception as e:
        DB.InsertExceptionStmtTable(e,"WC - GenerateExceptionFile")
        
#Generate word cloud    
def GenerateWordCloud():
    try:
        Val_1="Word Cloud image started"
        DB.InsertLogs(Val_1)  
               
        file_content=open ("Exception.txt").read()


        wordcloud = WordCloud(
                                    stopwords=STOPWORDS,
                                    background_color = 'white',
                                    width=1200,
                                    height=1000
                                    ).generate(file_content)

        plt.imshow(wordcloud)
        plt.axis('off')
        plt.show()
    except Exception as e:
        DB.InsertExceptionStmtTable(e,"WC - GenerateWordCloud")
        


