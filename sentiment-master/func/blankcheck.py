class blankck:
	def blankcheck(df1,df2):
		blank=0
		for row,i in enumerate(df1["Message_Original"]):
			i = str(i)
			if i == "0":
				blank+= 1
				df2.loc[row , 'NA'] ="Yes"
			else:
				df2.loc[row , 'NA'] = "No"
		#Print statement for debugging purposes
			print ('blank check going on')
		return blank