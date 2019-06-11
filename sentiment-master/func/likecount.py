#A module #to compare the like to dislike ratio to improve the sentiment
class likecount:
    def likedislike(df1,df2):
        for index in range(len(df1)):
            if index < len(df1.index) - 1:
                A = float(df1.loc[index, 'DisLikingCount'])   # Initialization of dislike count from df1 dataframe
                B = float(df1.loc[index, 'LikingCount'])  # Initialization of like count from df1 dataframe
                s = float(df2.loc[index, 'sentiment']) # Initialization of sentiment variable that we calculated from sentimfunc module
                # If messsage is original then perform relative analysis based on likes and dislikes
                if df1.loc[index, 'IsOP'] == 'Y':
                    if A > B:
                        df2.loc[index, 'sentiment'] = s - ((A - B) / 100)
                    elif A < B:
                        df2.loc[index, 'sentiment'] = s + ((B - A) / 100)
                #If message is not original then it checks the original sentiment and accordingly assigns positive and negetive sentiment based on the original message
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
