# -*- coding: cp1252 -*-
import xlrd
from xlwt import*  # @UnusedWildImport

class Employee:
    def __init__(self, idno,name, department, cat,unit ,staff):
        self.idno =  idno
        self.cat = cat

        self.name = name
        self.unit = unit
        self.department = department
        self.staff = staff
        
def readEmployees(file_location):
    emplist = []
    workbookread = xlrd.open_workbook(file_location)
    
    sheetread = workbookread.sheet_by_name('STAFF')
    for row in range(1, sheetread.nrows ):
        
        idno = str(int(sheetread.cell_value(row,0)))
        name = sheetread.cell_value(row,1).encode('ascii','ignore')
        cat = sheetread.cell_value(row,2).encode('ascii','ignore')
        department =sheetread.cell_value(row,3).encode('ascii','ignore')
        unit = sheetread.cell_value(row,4).encode('ascii','ignore')
        
        employee = Employee(idno = idno , name = name , unit = unit ,department = department, cat = cat,staff = True )
        emplist.append(employee)

    row=1
    sheetread = workbookread.sheet_by_name('Non-STAFF')
    for row in range(1, sheetread.nrows):
        
        idno = sheetread.cell_value(row,0).encode('ascii','ignore')
        name = sheetread.cell_value(row,1).encode('ascii','ignore')
        cat = sheetread.cell_value(row,2).encode('ascii','ignore')
        department =sheetread.cell_value(row,3).encode('ascii','ignore')
        unit = sheetread.cell_value(row,4).encode('ascii','ignore')
        
        employee = Employee(idno = idno , name = name , unit = unit ,department = department, cat = cat,staff = False )
        emplist.append(employee)
    return emplist


# -*- coding: cp1252 -*-
import xlrd
import time
from xlwt import*

def generate_format(file_location):
    wb = Workbook()
    wsheet = wb.add_sheet('STAFF')


    wsheet.col(0).width = 6666
    wsheet.col(1).width = 6666
    wsheet.col(2).width = 6666
    wsheet.col(3).width = 6666 
    wsheet.col(4).width = 6666


    fontname = Font()
    fontname.name = "Arial"
    fontname.colour_index = 0
    fontname.bold = True


    fonthead = Font()
    fonthead.name = "Arial"
    fonthead.height = 400
    fonthead.colour_index = 0
    fonthead.bold = True

    fontbody = Font()
    fontbody.name = "Arial"
    fontbody.height = 200
    fontbody.colour_index = 0
    fontbody.bold = False

    fontnew = Font()
    fontnew.name = "Arial"
    fontnew.underline = True
    fontnew.height = 300
    fontnew.colour_index = 0
    fontnew.bold = True

    fontnew2 = Font()
    fontnew2.name = "Arial"
    fontnew2.height = 200
    fontnew2.colour_index = 0
    fontnew2.bold = True

    alignment = Alignment()
    alignment.horz = Alignment.HORZ_CENTER
    alignment.vert = Alignment.VERT_CENTER

    alignment1 = Alignment()
    alignment1.horz = Alignment.HORZ_LEFT
    alignment1.vert = Alignment.VERT_CENTER

    bordername = Borders()
    bordername.left = 1
    bordername.right = 1 
    bordername.top = 1
    bordername.bottom = 1


    stylehead = XFStyle()
    stylehead.font = fonthead
    stylehead.alignment = alignment

    stylenew = XFStyle()
    stylenew.font = fontname
    stylenew.alignment = alignment


    stylenew1 = XFStyle()
    stylenew1.font = fontnew
    stylenew1.alignment = alignment
    stylenew1.borders = bordername

    styletitle = XFStyle()
    styletitle.font = fontnew2
    styletitle.alignment = alignment
    styletitle.borders = bordername

    stylebody = XFStyle()
    stylebody.borders = bordername
    stylebody.font = fontbody
    stylebody.alignment = alignment1

    stylebody1 = XFStyle()
    stylebody1.borders = bordername
    stylebody1.font = fontbody
    stylebody1.alignment = alignment

    wsheet.write(0,0,"Employee No.",styletitle)
    wsheet.write(0,1,"Name",styletitle)
    wsheet.write(0,2,"Category",styletitle)
    wsheet.write(0,3,"Department",styletitle)
    wsheet.write(0,4,"Unit",styletitle)
    i=0
 #   for i in range (1,1000):
 #       wsheet.write(i,0,'',styletitle)
 #       wsheet.write(i,1,'',styletitle)
 #       wsheet.write(i,2,'',styletitle)
 #       wsheet.write(i,3,'',styletitle)
 #       wsheet.write(i,4,'',styletitle)

    wsheet2 = wb.add_sheet('Non-STAFF')

    wsheet2.col(0).width = 6666
    wsheet2.col(1).width = 6666
    wsheet2.col(2).width = 6666
    wsheet2.col(3).width = 6666 
    wsheet2.col(4).width = 6666

    wsheet2.write(0,0,"Employee No.",styletitle)
    wsheet2.write(0,1,"Name",styletitle)
    wsheet2.write(0,2,"Category",styletitle)
    wsheet2.write(0,3,"Department",styletitle)
    wsheet2.write(0,4,"Unit",styletitle)
    i=0
    """    for i in range (1,1000):
        wsheet2.write(i,0,'',styletitle)
        wsheet2.write(i,1,'',styletitle)
        wsheet2.write(i,2,'',styletitle)
        wsheet2.write(i,3,'',styletitle)
        wsheet2.write(i,4,'',styletitle)"""

    wb.save(file_location)
        
