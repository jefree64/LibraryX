

def date_format(date,x = None):
	date = str(date)
	
	day = int(date[-2:])
	month = int(date[5:-3])
	year = int(date[:4])
	
	day1 = day + 15
	month1 = month
	year1 = year
	
	if month == 12 or month % 2 != 0:
		if day1 > 31:
			if month == 12:
				day1 = day1 - 31
				month1 = month + 1 - month
				year1 = year + 1
			else:
				day1 = day1 - 31
				month1 = month + 1
	else:
		if month == 2:
			if day1 > 28:
				day1 = day1
				month = month + 1
		else:
			if day1 > 30:
				day1 -=  30
				month1 += 1
	if month1 < 10:
		month1 = "0" + str(month1)
	if day1 < 10 :
		day1 = "0" + str(day1)
		
	return "{}-{}-{}".format(year1,month1,day1)

