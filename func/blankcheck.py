class blankck:

    def blankcheck(blank,df):
        for row,i in enumerate(df["Message_Original"]):
            element = str(i)
            if i == "0":
                blank+= 1
                df.loc[row , 'N/A'] = "Yes"
            else:

                df.loc[row , 'N/A'] = "No"
        return blank