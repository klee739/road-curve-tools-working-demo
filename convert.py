import pandas as pd
import csv

df = pd.read_csv('Sample_input.csv')



interval = '500'
same_interval = '50'

with open('eggs.csv', 'w', newline='') as csvfile:
	cw = csv.writer(csvfile)
	curve_id = 0
	sub_id = 0
	starting = 0

	for index,row in df.iterrows():
		
		if index == 0:
			cw.writerow(["line",starting])
		elif curve_id == row["Curve_ID"] and sub_id != row["Sub_ID"]:
			cw.writerow(["line",same_interval])
		else:
			cw.writerow(["line",interval])


		if row["Curve_Angle"] > 0:
			cw.writerow(["curve",row["Curve_Angle"],"right",row["Cruve_Radius"]])
			
		else:
			cw.writerow(["curve",row["Curve_Angle"],"left",row["Cruve_Radius"]])

		
		


		curve_id = row["Curve_ID"]
		sub_id = row["Sub_ID"]