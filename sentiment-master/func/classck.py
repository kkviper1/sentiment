# Used to classsify the postive,neutral and the negetive messages
class classck:
    def ClassCheck(df2):
        negative = 0;
        positive = 0;
        neutral = 0;
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
        return positive, negative, neutral