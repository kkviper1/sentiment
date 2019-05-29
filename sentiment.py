import pandas as pd
import re
import nltk
from nltk.sentiment.util import *
from func import sentimfunc as stm
from func import datavil as dvl
import sqlite3

# Initialization of variable
neg = 0
pos = 0
neu = 0


# Open the csv file using dataframes from pandas
df = pd.read_csv('Data_Dump.csv')
df.fillna('0', axis=1, inplace=True)
df = df.astype(str)

# Remove special characters to normalize the data
removeSpecialCharacters = ['\.', '\;', '\:', '\!', '\?', '\-', '\#[A-Za-z0-9]+', "\'", '\(', '\)']
for item in removeSpecialCharacters:
    df.replace(item, '', regex=True, inplace=True)



A = df.loc['Message_Original'] = df['Message_Original'].apply(str)
df['sentiment'] = A.apply(stm.sentimentP)
#df['subjectivity'] = A.apply(stm.sentimentS)
#subjectivity = df['subjectivity']
Polarity = df['sentiment']

list = {}
'''
for index, cell in enumerate(df['IsOP']):
    if cell == 'N':
        tempThreadID = df.loc[index, 'thread_id']
        for ind, i in enumerate(df['thread_id']):
            if i == tempThreadID:
                list[ind] = i
'''
s = 0
for z in list:
    if df.loc[z, 'IsOP'] == 'Y':
        s = df.loc[z, 'sentiment']
        for i in list:
            if df.loc[i, 'IsOP'] == 'N':
                if s < 0 and df.loc[i,'sentiment'] > 0:
                    df.loc[i, 'sentiment'] = -0.5
                elif s < 0 and df.loc[i, 'sentiment'] < 0:
                    df.loc[i, 'sentiment'] = 0.5
                else:
                    pass

                    # for index in enumerate(df['sentiment'])
                    # print(len(df))
                    # print(df.loc[2413,:])
                    # negative=0;positive=0;neutral=0
                    # for index, i in enumerate(df['sentiment']):
                    # 	if index<=len(df)-2:
                    # 		if df.loc[index, 'sentiment'] < 0:
                    # 			#df.loc[index, 'Category'] = "Negetive"
                    # 			negative += 1
                    # 			print('negative',index)
                    # 		elif df.loc[index, 'sentiment'] > 0:
                    # 			df.loc[index, 'Category'] = "Positive"
                    # 			print('positive',index)
                    # 			positive += 1
                    # 		else:
                    # 			df.loc[index, "Category"] = 'Neutral'
                    # 			print('neutral',index)
                    # 			neutral = neutral + 1
                    # = df['sentiment'].apply(float)
                    # df['sentiment'] = Polarity
                    # print(df['sentiment'])

                    # Used to classsify the postive,neutral and the negetive messages


def ClassCheck():
    negative = 0;
    positive = 0;
    neutral = 0;
    for index, i in enumerate(df['sentiment']):
        if index <= len(df) - 2:  # the last entry of the table is in row 2413 so thats the reason for the -2
            if df.loc[index, 'sentiment'] < 0:
                df.loc[index, 'Category'] = "Negetive"
                negative += 1
            elif df.loc[index, 'sentiment'] > 0:
                df.loc[index, 'Category'] = "Positive"
                positive += 1
            else:
                df.loc[index, "Category"] = 'Neutral'
                neutral = neutral + 1
    return positive, negative, neutral


pos, neg, neu = ClassCheck()
print(df)
dvl.dataVisualization(pos, neg, neu)

# This is used to convert the data elements into a output file.Commented because of data would keep writing into the outputfile in each run of the code

df1 = pd.DataFrame(df)
#df1.drop(['classification_flag'], 1)
writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1')
writer.save()

ClassCheck()
#conn = sqlite3.connect('C:\\Users\\vardan\\AppData\\Local\\Programs\\Python\\Python36-32\\BestFitSlope.py\\test.sqlite')
#df.to_sql('tab', conn, if_exists='replace', index=False)
#pd.read_sql('select * from tab', conn)
