# -*- coding: cp1252 -*-
import xlrd
import time
from xlwt import*
import calendar
from calendar import datetime
def calendar_write(date_notification,year , file_location):
    wb = Workbook()
    wsheet = wb.add_sheet('Calendar')

    fontyear = Font()
    fontyear.size = 20
    fontyear.name = "Arial"
    fontyear.colour_index = 0
    fontyear.bold = True

    fontmonth = Font()
    fontmonth.size = 18
    fontmonth.name = "Arial"
    fontmonth.colour_index = 0
    fontmonth.bold = True

    fontday = Font()
    fontday.size = 10
    fontday.name = "Arial"
    fontday.colour_index = 0

    alignment = Alignment()
    alignment.horz = Alignment.HORZ_CENTER
    alignment.vert = Alignment.VERT_CENTER

    alignmentleft = Alignment()
    alignmentleft.horz = Alignment.HORZ_LEFT
    alignmentleft.vert = Alignment.VERT_CENTER

    bordername = Borders()
    bordername.left = 1
    bordername.right = 1 
    bordername.top = 1
    bordername.bottom = 1

    styleyear = XFStyle()
    styleyear.font = fontyear
    styleyear.alignment = alignment
    styleyear.borders = bordername

    stylemonth = XFStyle()
    stylemonth.font = fontmonth
    stylemonth.alignment = alignment
    stylemonth.borders = bordername

    styleday = XFStyle()
    styleday.font = fontday
    styleday.alignment = alignmentleft
    styleday.borders = bordername

    months_choices = []
    for i in range(1,13):
        months_choices.append((i, datetime.date(2014, i, 1).strftime('%B')))

    wsheet.write_merge(0,0,0,10,year,styleyear)

    k=2
    for i in range(1,13):
        wsheet.write_merge(k,k,0,10,months_choices[i-1][1],stylemonth)
        k = k + 1
        for day in range(1,calendar.monthrange(year,i)[1] + 1):
            wsheet.write(k,0,day,styleday)
            wsheet.write_merge(k,k,1,10, date_notification[i-1].get_message_for_day(day) ,styleday)#########
            wsheet.row(k).height_mismatch = True
            wsheet.row(k).height = 400
            k = k + 1
        k = k + 1
        
    wb.save(file_location)

