from datetime import *

calendar_week = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
NOW = datetime.now() # get the current month and week
YEAR = int(NOW.strftime("%Y")) 
MONTH = int(NOW.strftime("%m"))
current_date = NOW.strftime("%d")


class Date_Month_Year:
    def __init__(self,calendar_date,month,year,calendar_month):
        self.calendar_date = calendar_date
        self.month = month
        self.year = year
        self.calendar_month = calendar_month