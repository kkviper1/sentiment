# Used to classsify the postive,neutral and the negetive messages
class classck:
    def ClassCheck(df2):
        negative = 0;
        positive = 0;
        neutral = 0;
        intneg = 0
        intpos = 0
        intneut = 0

        for index in range(len(df2)):
            if index < len(df2.index) - 1:  # the index starts from 0 so that is the reason for the -1
                if df2.loc[index, 'sentiment'] < 0:
                    df2.loc[index, 'Category'] = "Negetive"
                    negative += 1
                elif df2.loc[index, 'sentiment'] > 0:
                    df2.loc[index, 'Category'] = "Positive"
                    positive += 1
                elif df2.loc[index,'sentiment'] == 0:
                    df2.loc[index, "Category"] = 'Neutral'
                    neutral+=1
                else:
                    pass
        for index in range(len(df2)):
            if index < len(df2.index) - 1:  # the index starts from 0 so that is the reason for the -1
                if df2.loc[index, 'Intermediate Sentiment'] < 0:
                    intneg += 1
                elif df2.loc[index, 'Intermediate Sentiment'] > 0:
                    intpos += 1
                elif df2.loc[index, 'Intermediate Sentiment'] == 0:
                    intneut += 1
                else:
                    pass
        #print ('class check going on')
        return positive, negative, neutral, intneg, intpos, intneut