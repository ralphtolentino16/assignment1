#!/usr/bin/env python3
 
 
'''
OPS445 Assignment 1 - Winter 2025
Program: assignment1.py 
Author: "Ralph Louisse Tolentino"
The python code in this file (a1_rltolentino.py) is original work written by
"Ralph Louisse Tolentino". No code in this file is copied from any other source
except those provided by the course instructor, including any person,
textbook, or on-line resource. I have not shared this python script
with anyone or anything except for submission for grading. I understand
that the Academic Honesty Policy will be enforced and
violators will be reported and appropriate action will be taken.
'''
 
 
import sys

def day_of_week(year: int, month: int, date: int) -> str:
    "Based on the algorithm by Tomohiko Sakamoto"
    days = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'] 
    offset = {1:0, 2:3, 3:2, 4:5, 5:0, 6:3, 7:5, 8:1, 9:4, 10:6, 11:2, 12:4}
    if month < 3:
        year -= 1
    num = (year + year//4 - year//100 + year//400 + offset[month] + date) % 7
    return days[num]
 
  
def mon_max(month:int, year:int) -> int:
    "returns the maximum day for a given month. Includes leap year check"
    # last day of feb depends if leap year
    if leap_year(year):
        mon_max = { 1:31, 2:29, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
    else:
        mon_max = { 1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
    return mon_max[month] 
 

def after(date: str) -> str:
    '''
    after() -> date for next day in YYYY-MM-DD string format
 
 
    Return the date for the next day of the given date in YYYY-MM-DD format.
    This function takes care of the number of days in February for leap year.
    This fucntion has been tested to work for year after 1582
    '''

    year, month, day = splitdate(date) # splits the date into year month day
    tmp_day = day + 1  # next day
    last_day = mon_max(month, year) # gets last day of month

    if tmp_day > last_day:
        to_day = tmp_day % last_day # if tmp_day > this month's max, reset to 1 
        tmp_month = month + 1
    else:
        to_day = tmp_day
        tmp_month = month + 0

    if tmp_month > 12:
        to_month = 1
        year = year + 1
    else:
        to_month = tmp_month + 0
 
    next_date = f"{year}-{to_month:02}-{to_day:02}"
  
    return next_date


def splitdate(date: str) -> tuple[int, int, int]:
    "Splits the date into year, month, day - created for reusable purpose"
    "Returns int tuple of year, month, day"
    str_year, str_month, str_day = date.split('-')
    year = int(str_year)
    month = int(str_month)
    day = int(str_day)
    return year, month, day 


def usage():
    "Print a usage message to the user"
    print("Usage: assignment1.py YYYY-MM-DD YYYY-MM-DD")
 

def leap_year(year: int) -> bool:
    "return True if the year is a leap year"
    lyear = year % 4
    isleap = False

    if lyear == 0:
        #feb_max = 29 # this is a leap year
        isleap = True
    else:
        #feb_max = 28 # this is not a leap year
        isleap = False

    lyear = year % 100
    if lyear == 0:
        #feb_max = 28 # this is not a leap year
        isleap = False

    lyear = year % 400
    if lyear == 0:
        #feb_max = 29 # this is a leap year
        isleap = True

    return isleap


def valid_date(date: str) -> bool:
    "check validity of date and return True if valid"
    # check for incorrect format
    if len(date) != 10 or date[4] != '-' or date[7] != '-':
        return False
    
    year, month, day = splitdate(date) # split the date into year month day for checking
    
    # check if month is within valid range
    if month < 1 or month > 12:
        return False
    
    # check if day is less than 1
    if day < 1:
        return False

    # check if day exceeds last day of month
    if day > mon_max(month, year):
        return False

    return True

def day_count(start_date: str, end_date: str) -> int:
    "Counts the number of weekend days betweej two dates)"
    count = 0
    current_date = start_date # set start date as current date

    # loop until end date reached
    while current_date <= end_date:
        year, month, day = splitdate(current_date)
        weekday = day_of_week(year, month, day)

        # check if weekday is weekend (sat/sun)
        if weekday in ['sat', 'sun']:
            count += 1 # increase count of weekend days

        current_date = after(current_date)  # move to next day

    return count

 
def sort_dates(date1: str, date2: str) -> tuple[str, str]:
    "Ensures the earlier date is always the start date."
    "Returns a tuple (earlier_date, later_date) to still use the two dates. "

    year1, month1, day1 = splitdate(date1)
    year2, month2, day2 = splitdate(date2)

    if (year1, month1, day1) > (year2, month2, day2):
        return date2, date1  # swap if in wrong order
    return date1, date2  # dont change if in order 
 
if __name__ == "__main__":
    # to check number of arguments
    if len(sys.argv) != 3:
        usage() #show usage message to user if incomplete arguments
        sys.exit(1)

    start_date = sys.argv[1]
    end_date = sys.argv[2]

    # check if dates are valid date format
    for date in [start_date, end_date]:
        if not valid_date(date):
            usage() # show usage message if invalid date
            sys.exit(1)
    
    start_date, end_date = sort_dates(start_date, end_date)

    weekend_count = day_count(start_date, end_date)
    print(f"The period between {start_date} and {end_date} includes {weekend_count} weekend days.")
