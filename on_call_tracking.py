## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
##   Calendar App for Keeping Track of On Call                                               ##
##   Written by Daniel Mulder, April 2022                                                    ##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

## Preamble
# This script does not constitute medical advice and is only to be used for the purposes of learning or preparing personal templates
# This script contains no real medical information, any information contained within is fictional example information

import calendar
import numpy as np
import pandas as pd
import os
import csv
import datetime
from dateutil import parser

# load the shift list
os.chdir('/Users/danielmulder/Documents/GitHub/on_call_tracking')
my_shifts = pd.read_csv('on_call_shifts.csv')
my_shifts.Date = my_shifts.Date.astype(str)
print(my_shifts)

# define calendar
c = calendar.TextCalendar(calendar.SUNDAY)

# function to calculate number of days in the month
def days_this_month(this_year, this_month):
  count = 0
  for i in c.itermonthdays(this_year, this_month):
    if i != 0:
      count += 1
  return count

# function to add shifts from this month
def call_shifts_this_month(this_year, this_month, shift_day):
  this_year = str(this_year)
  this_month = str(this_month)
  shift_day = str(shift_day)
  if int(this_month) <10:
    this_month = '0' + this_month
  if int(shift_day) <10:
    shift_day = '0' + shift_day
  new_shift = this_year + '-' + this_month + '-' + shift_day
  new_shifts = pd.DataFrame([{'Date':new_shift}])
  return pd.concat([my_shifts, new_shifts])

updated_shifts = call_shifts_this_month(2022, 6, 1)

updated_shifts.to_csv('new_on_call_shifts.csv')

# create a new column with just month number
updated_shifts['Month'] = pd.DatetimeIndex(updated_shifts['Date']).month

# print call rate by month
def monthly_coverage(month):
  day_count = days_this_month(2022, month)
  shift_count = sum(updated_shifts['Month'] == month)
  monthly_coverage = day_count/shift_count
  if monthly_coverage > 4.0:
    coverage_conclusion = "NOT ENOUGH"
  else:
    coverage_conclusion = "enough"
  month_num = str(month)
  datetime_object = datetime.datetime.strptime(month_num, "%m")
  month_name = full_month_name = datetime_object.strftime("%B")
  print('1 in', "{:.2f}".format(monthly_coverage), 'coverage for', month_name)
  print(coverage_conclusion)

monthly_coverage(4)
monthly_coverage(5)
monthly_coverage(6)


