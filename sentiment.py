import pandas as pd
import numpy as np
import re
import nltk
from nltk.sentiment.util import *
from func import sentimfunc as stm
from func import datavil as dvl
from func import blankck as blk
from func import classck as clck
from func import heatmap as hmp
import MySQLdb
import pandas.io.sql as psql

# Initialization of variables
neg = 0
pos = 0
neu = 0
intneg = 0
intpos = 0
intneut = 0
blank = 0
s = 0
values = []
list = {}
'''
query1 used to select all the data from the target sql table
query2 used to delete previously made sentiment-category-NA table for previous values
query3 used to create a new table called message_new which contains sentiment, category &NA columns
query4 used to copy message_Ids from target table to message_new
query5 used to select all dat from message_new
query6 used to update message_new table with NA-sentiment-Category values

'''
#Queries
query1 = "SELECT * FROM Message_Table"
query2="DROP TABLE IF EXISTS message_new"
query3="CREATE TABLE message_new ( " \
       " `id` INT NOT NULL AUTO_INCREMENT ," \
       "`sentiment` VARCHAR(145) NULL," \
       "`Category` VARCHAR(145) NULL," \
       "`NA` VARCHAR(145) NULL," \
       "`Difference` VARCHAR(145) NULL," \
       "`IntermediateSentiment` VARCHAR(145) NULL, "\
       "`Message_Id` VARCHAR(145) NULL, " \
       "PRIMARY KEY  (id) )"
query4="INSERT INTO message_new (Message_Id) SELECT Message_Id FROM Message_Table"
query5="SELECT * FROM message_new"
query6="UPDATE message_new SET NA = %s, sentiment  = %s, Category = %s, Difference = %s, IntermediateSentiment = %s WHERE (Message_Id = %s)"

#Connecting to the database
db=MySQLdb.connect( user='root', passwd='password', db='babbles')

# Using query1 to assign the results to a pandas dataframe
df1 = psql.read_sql(query1, con=db)

#initializing the cursor
cursor=db.cursor()

#Filling in 0s in place of blank values
df1.fillna('0', axis=1, inplace=True)
df1 = df1.astype(str)

# Remove special characters to normalize the data
removeSpecialCharacters = ['\.', '\;', '\:', '\!', '\?', '\-', '\#[A-Za-z0-9]+', "\'", '\(', '\)']
for item in removeSpecialCharacters:
    df1['Message_Original'].replace(item, '', regex=True, inplace=True)




#Executing queries 2 to 4
cursor.execute(query2)
db.commit()
cursor.execute(query3)
db.commit()
cursor.execute(query4)
db.commit()

#Using query5 to assign the results to a pandas dataframe
df2=psql.read_sql(query5,con=db)


#Lists for positive and negative words
filePath = "positive-words.txt"
positivewords = []
wordCount = 0

#Read lines into a list
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
#print(wordList)
#print("Total words = %d" % wordCount)
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

#Applying sentiment analysis function
A = df2['Message_Original'] = df1['Message_Original'].apply(str)
df2['sentiment'] = A.apply(stm.sentimentP)

#Checking for Blank Messages
blank = blk.blankcheck(df1,df2)
'''
#df1['subjectivity'] = A.apply(stm.sentimentS)                       
#subjectivity = df1['subjectivity']                                      To be used in the future
#Polarity = df1['sentiment']

'''

#Modifying the sentiment values to deal with the relative sentiment analysis problem

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

for i in range(len(df2)):
    if i < len(df2.index) - 1:  # the index starts from 0 so that is the reason for the -1
        df2.loc[i,'Intermediate Sentiment'] = df2.loc[i,'sentiment']

#Adding the difference between positive and negative words to the sentiment
for index,i in enumerate(df2['sentiment']):
    df2.loc[index,'sentiment'] += (df2.loc[index,'Difference'])/10

#Visualising the data
pos, neg, neu, intneg, intpos, intneut = clck.ClassCheck(df2)
dvl.dataVisualization(pos, neg, neu)
dvl.dataVisualization(intpos,intneg,intneut)

print(f'Number of blank spaces : {blank}')

#Making a temp dataframe to use it's len function
tempVariable=pd.DataFrame(df2)

#Selecting the values to be inserted into the table
for index in range(len(df2)):
    if index < len(df2.index)-1:             #The minus 1 is there due to the records starting at 0
        msgID=df2.loc[index,"Message_Id"]
        '''
        threadID=df1.loc[index,"Thread_Id"]
        mobileNo=df1.loc[index,"Mobile_Number"]
        lat=df1.loc[index,"Latitude"]
        long=df1.loc[index,"Longitude"]
        isOp=df1.loc[index,"IsOP"]
        avatarID=df.loc[index,"Avatar_Id"]
        DNDT=df.loc[index,"Do_Not_Display_To"]
        msg=df.loc[index,"Message"]
        timestamp=df.loc[index,"Timestamp"]
        dispMsg=df.loc[index,"Display_Message"]
        country=df.loc[index,"Country_Name"]
        img=df.loc[index,"Image_Path"]
        imgRating=df.loc[index,"Image_Rating"]
        isImg=df.loc[index,"Is_Image"]
        editFlag=df.loc[index,"EditFlag"]
        FF1=df.loc[index,"Free_Field1"]
        FF2=df.loc[index,"Free_Field2"]
        FF3=df.loc[index,"Free_Field3"]
        FF4=df.loc[index,"Free_Field4"]
        loc=df.loc[index,"Location_Name"]
        grpID=df.loc[index,"Group_Id"]
        preGrpID=df.loc[index,"Predefine_Group_Id"]
        replyCount=df.loc[index,"ReplyCount"]
        disLikeCount=df.loc[index,"DisLikingCount"]
        likeCount=df.loc[index,"LikingCount"]
        height=df.loc[index,"Height"]
        width=df.loc[index,"Width"]
        imageOrientation=df.loc[index,"Image_Orientation"]
        contentURL=df.loc[index,"Content_Url"]
        thumbnailURL=df.loc[index,"Thumbnail_Url"]
        msgType=df.loc[index,"Message_Type"]
        userMobileNo=df.loc[index,"User_Mobile_Number"]
        rssFeed=df.loc[index,"RssFeed"]
        duration=df.loc[index,"Duration"]
        is_Liked=df.loc[index,"isLiked"]
        msgOriginal=df.loc[index,"Message_Original"]
        '''
        NA = df2.loc[index, "NA"]
        sentiment = df2.loc[index, "sentiment"]
        category = df2.loc[index, "Category"]
        DifCount = df2.loc[index, "Difference"]
        IntSent = df2.loc[index, "Intermediate Sentiment"]
        values.append((NA,sentiment,category,DifCount,IntSent,msgID))
    #Print statement for debugging purposes
    #print ('insert into db')

#Executing query6
cursor.executemany(query6, values)

hmp.heatmap(df1)

#closing the cursor object, committing the changes to the database and closing the database
cursor.close()
db.commit()
db.close()



