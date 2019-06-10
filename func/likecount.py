class likecount:
    def likedislike(df1,df2):
        for index in range(len(df1)):
            if index < len(df1.index) - 1:
                A = float(df1.loc[index, 'DisLikingCount'])
                B = float(df1.loc[index, 'LikingCount'])
                s = float(df2.loc[index, 'sentiment'])
                if df1.loc[index, 'IsOP'] == 'Y':
                    if A > B:
                        df2.loc[index, 'sentiment'] = s - ((A - B) / 100)
                    elif A < B:
                        df2.loc[index, 'sentiment'] = s + ((B - A) / 100)
                elif df1.loc[index, 'IsOP'] == 'N':
                    if s < 0:
                        if A > B:
                            df2.loc[index, 'sentiment'] = s + ((A - B) / 150)
                        elif B > A:
                            df2.loc[index, 'sentiment'] = s - ((B - A) / 150)
                    elif s > 0:
                        if A > B:
                            df2.loc[index, 'sentiment'] = s - ((A - B) / 150)
                        elif B > A:
                            df2.loc[index, 'sentiment'] = s + ((B - A) / 150)


