# -*- coding: cp1252 -*-
import xlrd
from xlwt import*  # @UnusedWildImport

class Employee:
    def __init__(self, idno,name, department, cat,unit):
        self.idno =  idno
        self.cat = cat

        self.name = name
        self.unit = unit
        self.department = department
        
def readEmployees(file_location):
    emplist = []
    workbookread = xlrd.open_workbook(file_location)
    for index in range(0,6):
        sheetread = workbookread.sheet_by_index(index)
        for row in range(4, sheetread.nrows ):
            
            idno = sheetread.cell_value(row,1).encode('ascii','ignore')
            name = sheetread.cell_value(row,2).encode('ascii','ignore')
            cat = sheetread.cell_value(row,3).encode('ascii','ignore')
            department =sheetread.cell_value(row,4).encode('ascii','ignore')
            unit = sheetread.cell_value(row,5).encode('ascii','ignore')
            employee = Employee(idno = idno , name = name , unit = unit ,department = department, cat = cat )
            emplist.append(employee)
    return emplist
        
