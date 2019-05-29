# Used to classsify the postive,neutral and the negetive messages
class classck:
    def ClassCheck(df):
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