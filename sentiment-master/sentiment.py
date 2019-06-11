import pandas as pd
import numpy as np
import re
import nltk
from nltk.sentiment.util import *
from func import sentimfunc as stm
from func import datavil as dvl
from func import blankck as blk
from func import classck as clck
from func import  likecount as lk
from func import heatmap as hmp
import MySQLdb
import pandas.io.sql as psql


# Initialization of variables
neg = 0
pos = 0
neu = 0
blank = 0
s = 0
values = []
list = {}
'''
query1 used to select all the data from the target sql table
query2 used to insert data from Message_Id of message_table to Message_Id of message_new 
query3 used to select all the data from message_new iff it corresponds to the current message_table
query4 used to update message_new table with NA-sentiment-Category values

'''
# Queries
query1 = "SELECT * FROM message_table"
query2 = "INSERT INTO message_new (Message_Id) " \
       " SELECT Message_Id FROM message_table" \
       " WHERE message_table.Message_Id" \
       " NOT IN (SELECT message_new.Message_Id FROM message_new)" \
       " ORDER BY Message_Id"
query3 = "SELECT * FROM message_new " \
       "WHERE message_new.Message_Id IN " \
       "(SELECT message_table.Message_Id  FROM message_table) " \
       "ORDER BY Message_Id"
query4 = "UPDATE message_new SET NA = %s, sentiment  = %s, Category = %s, Intermediate_Sentiment =%s, Difference = %s " \
         " WHERE (Message_Id=%s) "


# Connecting to the database
db = MySQLdb.connect( user='roger', passwd='roger', db='test')

# Using query1 to assign the results to a pandas dataframe
df1 = psql.read_sql(query1, con=db)

# Initializing the cursor
cursor=db.cursor()

# Filling in 0s in place of blank values
df1.fillna('0', axis=1, inplace=True)
df1 = df1.astype(str)

# Remove special characters to normalize the data
removeSpecialCharacters = ['\.', '\;', '\:', '\!', '\?', '\-', '\#[A-Za-z0-9]+', "\'", '\(', '\)']
for item in removeSpecialCharacters:
    df1['Message_Original'].replace(item, '', regex=True, inplace=True)

# Executing queries 2
cursor.execute(query2)
db.commit()

# Using query3 to assign the results to a pandas dataframe
df2=psql.read_sql(query3,con=db)

# Lists for positive and negative words
filePath = "positive-words.txt"
positivewords = []
wordCount = 0

# Read lines into a list
file = open(filePath, 'rU')
for line in file:
    for word in line.split():
        positivewords.append(word)
        wordCount += 1

filePath2 = "negative-words.txt"
negativewords = []
wordCount = 0

file = open(filePath2, 'rU')
for line in file:
    for word in line.split():
        negativewords.append(word)
        wordCount += 1
poscount = 0
negcount = 0
difcount = 0

for row,i in enumerate(df1["Message_Original"]):
    posres = [f for f in positivewords if(f in i)]
    poscount=len(posres)
    negres = [f for f in negativewords if(f in i)]
    negcount=len(negres)
    difcount = poscount - negcount
    df2.loc[row,'Difference'] = difcount

# Applying sentiment analysis function
A = df1['Message_Original'] = df1['Message_Original'].apply(str)
df2['sentiment'] = A.apply(stm.sentimentP)

# Checking for Blank Messages
blank = blk.blankcheck(df1,df2)
'''
#df1['subjectivity'] = A.apply(stm.sentimentS)                       
#subjectivity = df1['subjectivity']                                      To be used in the future
#Polarity = df1['sentiment']

'''
# Modifying the sentiment values to deal with the relative sentiment analysis problem
for z in list:
    if df1.loc[z, 'IsOP'] == 'Y':
        s = df2.loc[z, 'sentiment']
        for i in list:
            if df1.loc[i, 'IsOP'] == 'N':
                if s < 0 and df2.loc[i,'sentiment'] > 0:
                    df2.loc[i, 'sentiment'] = -0.5
                elif s < 0 and df2.loc[i, 'sentiment'] < 0:
                    df2.loc[i, 'sentiment'] = 0.5
                else:
                    pass

# Dealing with image data
for index,i in enumerate(df1["Is_Image"]):
    if i=="Y" and df1.loc[index,"IsOP"]=="N":
        df2.loc[index,"sentiment"]=-0.551
        df2.loc[index,"Category"]="Negative"
    else:
        pass

# Tinkering with the sentiment of the data to improve upon it
lk.likedislike(df1, df2)
for i in range(len(df2)):
    if i < len(df2.index) - 1:  # the index starts from 0 so that is the reason for the -1
        df2.loc[i,'Intermediate_Sentiment'] = df2.loc[i,'sentiment']

# Adding the difference between positive and negative words to the sentiment
for index,i in enumerate(df2['sentiment']):
    df2.loc[index,'sentiment'] += (df2.loc[index,'Difference'])/10

# Visualising the data
pos, neg, neu = clck.ClassCheck(df2)
dvl.dataVisualization(pos, neg, neu)

print(f'Number of blank spaces : {blank}')

# Making a temp dataframe to use it's len function
tempVariable=pd.DataFrame(df2)

# Making all the data into str type
df2['Intermediate_Sentiment']=df2['Intermediate_Sentiment'].apply(str)
df2['Difference']=df2['Difference'].apply(str)

# Selecting the values to be inserted into the table
for index in range(len(df2)):
    if index < len(df2.index)-1:             # The minus 1 is there due to the records starting at 0
        msgID=df2.loc[index,"Message_Id"]
        NA = df2.loc[index, "NA"]
        sentiment = df2.loc[index, "sentiment"]
        category = df2.loc[index, "Category"]
        intSent = df2.loc[index,"Intermediate_Sentiment"]
        diff = df2.loc[index,"Difference"]
        values.append((NA,sentiment,category,intSent,diff,msgID))
        # Print statement for debugging purposes
        print ('insert into db')

# Executing query4
cursor.executemany(query4, values)

hmp.heatmap(df1)

# Closing the cursor object, committing the changes to the database and closing the database
cursor.close()
db.commit()
db.close()



