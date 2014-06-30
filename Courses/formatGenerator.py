# -*- coding: cp1252 -*-
import time
from Users import userfunctions
from xlwt import*
import datetime
from Courses.models import BatchDetails, Course
def make_l4pa1(batch,employees ,trainers ,file_location):
    trainerNames = []
    for trainer in trainers:
        trainerNames.append(trainer.userObj.first_name + " " + trainer.userObj.last_name)
    hods = []
    for department in batch.course.department.all():
        hods.extend(userfunctions.get_hod_of_department(department))
    hodNames = []
    for hod in hods:
        hodNames.append(hod.userObj.first_name + " " + hod.userObj.last_name)
        
    wb = Workbook(encoding='latin-1')
    wsheet = wb.add_sheet('L4PA1(new)')
    wsheet.show_grid = False

    wsheet.col(0).width = 1500 
    wsheet.col(1).width = 3333
    wsheet.col(2).width = 6666
    wsheet.col(3).width = 5000 
    wsheet.col(4).width = 6666
    wsheet.col(5).width = 6666
    j=17

    for j in range (18,100):
        wsheet.row(j).height_mismatch = True
        wsheet.row(j).height = 500
    
    fontname = Font()
    fontname.name = "Arial"
    fontname.colour_index = 0

    fontnew = Font()
    fontnew.name = "Arial"
    fontnew.colour_index = 0
    fontnew.bold = (True)

    alignment = Alignment()
    alignment.horz = Alignment.HORZ_LEFT
    alignment.vert = Alignment.VERT_CENTER

    alignment1 = Alignment()
    alignment1.horz = Alignment.HORZ_CENTER
    alignment1.vert = Alignment.VERT_CENTER

    bordername = Borders()
    bordername.left = 1
    bordername.right = 1 
    bordername.top = 1
    bordername.bottom = 1


    stylename = XFStyle()
    stylename.font = fontname
    stylename.alignment = alignment

    stylenew = XFStyle()
    stylenew.font = fontnew
    stylenew.alignment = alignment
    stylenew.borders = bordername

    stylenew1 = XFStyle()
    stylenew1.font = fontname
    stylenew1.alignment = alignment1
    stylenew1.borders = bordername

    stylehead = XFStyle()
    stylehead.font = fontnew
    stylehead.alignment = alignment1
    

    wsheet.write_merge(0,0,0,4,"TRAINING DEPUTATION",stylehead)
    wsheet.write_merge(0,0,5,5,"L4-PA1",stylehead)
    wsheet.write_merge(2,2,0,2,"TVL/HRA/TRNG/" +time.strftime("%m")+"/" +time.strftime("%Y"),stylename)
    wsheet.write_merge(2,2,5,5,"Date:"+ time.strftime("%d.%m.%Y"),stylename) 
    wsheet.write_merge(4,4,0,2,"Programme Title" + batch.course.course_name ,stylename) #course name
    wsheet.write_merge(6,6,0,2,"Conducted By:" + ','.join(trainerNames), stylename)#Instructor name
    wsheet.write_merge(8,8,0,2,"Venue: " +  batch.venue,stylename)#Course Address
    wsheet.write_merge(10,10,0,2,"Date and Time: " + str(batch.start_date),stylename)# {Date and time of the course}
    wsheet.write_merge(12,12,0,5,"Below mentioned employees are deputed to the above Programme. Kindly make it conveinient to attend",stylename)
    wsheet.write_merge(14,14,0,5,"Kindly return the duly filled “Feed-back” format to the HR & Administration department within 3 days of attending the Programme.",stylename)


#table begins
    wsheet.write_merge(16,17,0,0," Sl. No. ",stylenew) 
    wsheet.write_merge(16,17,1,1," CL- Code ",stylenew)    
    wsheet.write_merge(16,17,2,2," Employee Name ",stylenew)       
    wsheet.write_merge(16,17,3,3," Department ",stylenew)
    wsheet.write_merge(16,17,4,4," Designation ",stylenew)
    wsheet.write_merge(16,17,5,5," Signature ",stylenew)

    i=1
    for i in range(1,len(employees)+1):                   #range till total no of employees selected
        wsheet.write(17+i,0,i,stylenew1)    #s no.
        wsheet.write(17+i,1,employees[i-1].userId,stylenew1)   #CL-CODE
        wsheet.write(17+i,2,employees[i-1].userObj.first_name +" " + employees[i-1].userObj.last_name,stylenew1)   #Employee Name
        wsheet.write(17+i,3,employees[i-1].department.dept_name,stylenew1)   #Department
        wsheet.write(17+i,4,employees[i-1].designation,stylenew1)   #Designation
        wsheet.write(17+i,5,"",stylenew1)   #Signature .. Intentionally left blank

    i = i + 17 + 3            # fixed values... only change if length of prev loop is change (ie i changes)
    wsheet.write( i, 1, "CC to HOD's:" ,stylehead)
    wsheet.write( i, 4, "Authorized Signatory",stylehead)

    j=1
    for j in range (1,len(hods)+1):       #range is equal to no of hod's to cc
        wsheet.write(i+j , 1 , hod.designation + "-" + hod.department.dept_name , stylename) # "{designation}" + "-" + "{department}" eg . SM-HR

    return wb.save(file_location) 

# -*- coding: cp1252 -*-
import xlrd
import time
from xlwt import*


# -*- coding: cp1252 -*-
import xlrd
import time
from xlwt import*

def make_l4pa3(batch,employees,trainers,file_location):
    trainerNames = []
    for trainer in trainers:
        trainerNames.append(trainer.userObj.first_name + " " + trainer.userObj.last_name)
    wb = Workbook()
    wsheet = wb.add_sheet('L4PA3')
    wsheet.show_grid = False

    wsheet.col(0).width = 2000 
    wsheet.col(1).width = 8000
    wsheet.col(2).width = 4000
    wsheet.col(3).width = 2000 
    wsheet.col(4).width = 8000

    for j in range(4,50):
        wsheet.row(j).height_mismatch = True
        wsheet.row(j).height = 600

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

    wsheet.write_merge(2,2,0,4,"TRITON VALVES LIMITED, Mysore",stylehead)
    wsheet.write(3,4,"L4-PA.3",stylenew)
    wsheet.write_merge(4,4,0,4,"ATTENDANCE - LIST",stylenew1)

    wsheet.write_merge(5,5,0,4,"Title of the Programme: " + batch.course.course_name,stylebody)
    wsheet.write_merge(6,6,0,1,"Faculty: "+ ','.join(trainerNames),stylebody)
    wsheet.write_merge(6,6,2,4,"Date & Time: " + str(batch.start_date),stylebody)
    wsheet.write_merge(7,7,0,4,"Venue: " + batch.venue,stylebody)
    wsheet.write(9,0,"Sl.No ",styletitle)
    wsheet.write(9,1,"Name ",styletitle)
    wsheet.write(9,2,"Emp. No. ",styletitle)
    wsheet.write(9,3,"Shift ",styletitle)
    wsheet.write(9,4,"Signature ",styletitle)
    i=1
    for i in range(1,len(employees)+1):                   #here 1 is fixed and 18 is the number of names from the database
        wsheet.write(i+9,0,i,stylebody1)    #slno
        wsheet.write(i+9,1,employees[i-1].userObj.first_name + employees[i-1].userObj.last_name,stylebody)    #Name of the employee from the database
        wsheet.write(i+9,2,employees[i-1].userId,stylebody)    #employee no from the database
        wsheet.write(i+9,3,employees[i-1].current_shift,stylebody)    #shift from the database
        wsheet.write(i+9,4,"",stylebody)    # signature ...  intentionally left blank

    wsheet.write_merge(10 +18,10 +18,0,2,"Trainer's Name:",stylebody) # here 8 is the number of names from the database
    wsheet.write_merge(10 +18,10 +18,3,4,"Signature:",stylebody)
    wb.save(file_location)

# -*- coding: cp1252 -*-

"""
from xlwt import*
from random import randint
import numpy as np
import matplotlib.pyplot as plt
from array import array
from PIL import Image

def make_l4pa5(file_location, batch , trainers ,employeeFeedbacks):
    trainerNames = []
    for trainer in trainers:
        trainerNames.append(trainer.first_name + " " + trainer.last_name)
    wb = Workbook()
    wsheet = wb.add_sheet('L4PA5')

    wsheet.col(1).width = 6666
    wsheet.col(2).width = 4000
    wsheet.col(3).width = 4000
    wsheet.col(4).width = 4000
    wsheet.col(5).width = 4000
    wsheet.col(6).width = 4000
    wsheet.col(7).width = 4000
    wsheet.col(8).width = 4000
    wsheet.col(9).width = 4000
    wsheet.col(10).width = 4000

    fontbold = Font()
    fontbold.name = "Arial"
    fontbold.colour_index = 0
    fontbold.bold = True

    fontnotbold = Font()
    fontnotbold.name = "Arial"
    fontnotbold.colour_index = 0
    fontnotbold.bold = True

    alignmentcenter = Alignment()
    alignmentcenter.horz = Alignment.HORZ_CENTER
    alignmentcenter.vert = Alignment.VERT_CENTER

    alignmentleft = Alignment()
    alignmentleft.horz = Alignment.HORZ_LEFT
    alignmentleft.vert = Alignment.VERT_CENTER

    bordername = Borders()
    bordername.left = 1
    bordername.right = 1 
    bordername.top = 1
    bordername.bottom = 1


    stylehead = XFStyle()
    stylehead.font = fontbold
    stylehead.alignment = alignmentcenter
    stylehead.borders = bordername

    styletitle = XFStyle()
    styletitle.font = fontnotbold
    styletitle.alignment = alignmentleft
    styletitle.borders = bordername

    stylebody = XFStyle()
    stylebody.font = fontnotbold
    stylebody.alignment = alignmentleft
    stylebody.borders = bordername

    wsheet.write_merge(0,0,0,10,"TRITON VALVES LIMITED",stylehead)
    wsheet.write_merge(1,1,0,10,"PROGRAMME EVALUATION STATEMENT",stylehead)
    wsheet.write_merge(2,2,9,10,"L4-PA-5",stylehead)
    wsheet.write_merge(3,3,0,4,"Programme Title:" + batch.course.course_name,styletitle) # Title of the course from database
    wsheet.write_merge(3,3,5,8,"Conducted by: " + ",".join(trainerNames),styletitle)# trainer from the data base
    wsheet.write_merge(3,3,9,10,"Date: " + batch.start_date ,styletitle)#date of the course from the database
    wsheet.write_merge(4,4,2,6,"PROGRAMME EVALUATION",stylehead)
    wsheet.write_merge(4,4,7,10,"FACULTY EVALUATION",stylehead)

    wsheet.write(5,0,"Sl.No",stylehead)
    wsheet.write(5,1,"Name",stylehead)
    wsheet.write(5,2,"Methodology",stylehead)
    wsheet.write(5,3,"Audio Vision",stylehead)
    wsheet.write(5,4,"Course Material",stylehead)
    wsheet.write(5,5,"Arrangement",stylehead)
    wsheet.write(5,6,"Overall Opinion",stylehead)
    wsheet.write(5,7,"Subject Knowledge",stylehead)
    wsheet.write(5,8,"Presentation Skill",stylehead)
    wsheet.write(5,9,"Communication",stylehead)
    wsheet.write(5,10,"Interation skills",stylehead)

    a = array('i')
    b = array('i')
    
    a.append(0)
    a.append(0)
    a.append(0)
    a.append(0)
    a.append(0)
    a.append(0)
    a.append(0)
    a.append(0)
    a.append(0)

    b.append(0)
    b.append(0)
    b.append(0)
    b.append(0)
    b.append(0)
    b.append(0)
    b.append(0)
    b.append(0)
    b.append(0)

    k=0

    ranking_pe = []
    ranking_fe = []

    for i in range(0,len(employeeFeedbacks)): #for reference "20" is a variable its just the number of people giving the feedback
        wsheet.write(i+7,0,i+1,stylebody)
        wsheet.write(i+7,1,employeeFeedbacks[i].employee.userObj.first_name + " " + employeeFeedbacks[i].employee.userObj.last_name,stylebody) #name of the employee giving the feedback

        a[0] = (employeeFeedbacks[i].feedback.training_methodology)#methodolgy feedback
        wsheet.write(i+7,2,a[0],stylebody)
        a[1] =(employeeFeedbacks[i].feedback.use_of_AV_techniques)#audio visio feedback
        wsheet.write(i+7,3,a[1],stylebody)
        a[2] =(employeeFeedbacks[i].feedback.quality_of_courseMaterial)#course material feedback
        wsheet.write(i+7,4,a[2],stylebody)
        a[3] = (employeeFeedbacks[i].feedback.aoth)#Arrangement feedback
        wsheet.write(i+7,5,a[3],stylebody)
        a[4] = (employeeFeedbacks[i].feedback.opinion)#oveall opinion feedback
        wsheet.write(i+7,6,a[4],stylebody)
        a[5] = (employeeFeedbacks[i].feedback.subject_knowledge)#subject knowledge feedback
        wsheet.write(i+7,7,a[5],stylebody)
        a[6] = (employeeFeedbacks[i].feedback.presentation_skills)#Presentation Skill feedback
        wsheet.write(i+7,8,a[6],stylebody)
        a[7] = (employeeFeedbacks[i].feedback.communication_skills)#Communication feedback
        wsheet.write(i+7,9,a[7],stylebody)
        a[8] = (employeeFeedbacks[i].feedback.iwp)#Interation skills feedback
        wsheet.write(i+7,10,a[8],stylebody)
        k=0
        for k in range(0,9):
            b[k] = b[k] + a[k]

    #reminding again "20" is a variable and its just the numer of people giving the course
    length = len(employeeFeedbacks)
    wsheet.write(length+7,2,"Methodology",stylehead)
    wsheet.write(length+7,3,"Audio Vision",stylehead)
    wsheet.write(length+7,4,"Course Material",stylehead)
    wsheet.write(length+7,5,"Arrangement",stylehead)
    wsheet.write(length+7,6,"Overall Opinion",stylehead)
    wsheet.write(length+7,7,"Subject Knowledge",stylehead)
    wsheet.write(length+7,8,"Presentation Skill",stylehead)
    wsheet.write(length+7,9,"Communication",stylehead)
    wsheet.write(length+7,10,"Interation skills",stylehead)




    wsheet.write_merge(length+8,length+8,0,1,"Ranking",stylehead) # here the value "length" is variable and "8" is fixed

    wsheet.write(length+8,2,b[0],stylebody)
    ranking_pe.append(b[0])
    wsheet.write(length+8,3,b[1],stylebody)
    ranking_pe.append(b[1])
    wsheet.write(length+8,4,b[2],stylebody)
    ranking_pe.append(b[2])
    wsheet.write(length+8,5,b[3],stylebody)
    ranking_pe.append(b[3])
    wsheet.write(length+8,6,b[4],stylebody)
    ranking_pe.append(b[4])
    wsheet.write(length+8,7,b[5],stylebody)
    ranking_fe.append(b[5])
    wsheet.write(length+8,8,b[6],stylebody)
    ranking_fe.append(b[6])
    wsheet.write(length+8,9,b[7],stylebody)
    ranking_fe.append(b[7])
    wsheet.write(length+8,10,b[8],stylebody)
    ranking_fe.append(b[8])

    maximum_ranking_pe = []
    maximum_ranking_fe = []

    wsheet.write_merge(length+9,length+9,0,1,"Maximum Rating",stylehead)# here the value "length" is variable and "9" is fixed
    for i in range(2,7):
        wsheet.write(length+9,i, str(length*10) ,stylebody) # here also 'length' is the number of people
        maximum_ranking_pe.append((length*10)) # here also 'length' is the number of people

    for i in range(7,11):
        wsheet.write(length+9,i, str(length*10) ,stylebody) # here also 'length' is the number of people
        maximum_ranking_fe.append((length*10)) # here also 'length' is the number of people



    wsheet.write_merge(length+10,length+10,0,1,"% of Rating",stylehead)# here the value "length" is variable and "10" is fixed

    wsheet.write(length+10,2,Formula("SUM(C"+str(length+9)+"/C"+str(length+10)+")*100"),stylebody)#here also "C-length" is a variable
    wsheet.write(length+10,3,Formula("SUM(D"+str(length+9)+"/D"+str(length+10)+")*100"),stylebody)#here also "D-length" is a variable
    wsheet.write(length+10,4,Formula("SUM(E"+str(length+9)+"/E"+str(length+10)+")*100"),stylebody)#here also "E-length" is a variable
    wsheet.write(length+10,5,Formula("SUM(F"+str(length+9)+"/F"+str(length+10)+")*100"),stylebody)#here also "F-length" is a variable
    wsheet.write(length+10,6,Formula("SUM(G"+str(length+9)+"/G"+str(length+10)+")*100"),stylebody)#here also "G-length" is a variable
    wsheet.write(length+10,7,Formula("SUM(H"+str(length+9)+"/H"+str(length+10)+")*100"),stylebody)#here also "H-length" is a variable
    wsheet.write(length+10,8,Formula("SUM(I"+str(length+9)+"/I"+str(length+10)+")*100"),stylebody)#here also "I-length" is a variable
    wsheet.write(length+10,9,Formula("SUM(J"+str(length+9)+"/J"+str(length+10)+")*100"),stylebody)#here also "J-length" is a variable
    wsheet.write(length+10,10,Formula("SUM(K"+str(length+9)+"/K"+str(length+10)+")*100"),stylebody)#here also "K-length" is a variable

    wsheet.write_merge(length+11,length+11,0,1,"Average",stylehead)# here the value "length" is variable and "10" is fixed
    wsheet.write_merge(length+11,length+11,2,6,Formula("AVERAGE(C"+str(length+11)+":G" +str(length+11)+")"),stylehead)# here the value "length" is variable and "10" is fixed
    wsheet.write_merge(length+11,length+11,7,10,Formula("AVERAGE(H"+str(length+11)+":K" +str(length+11)+")"),stylehead)# here the value "length" is variable and "10" is fixed




    ind = 0
    P=5
    F=4

    ind = np.arange(P)  # @UndefinedVariable
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, ranking_pe, width, color='b',yerr=0)
    rects2 = ax.bar(ind +width,maximum_ranking_pe, width, color='r',yerr=0)

    ax.set_title('Programme Evaluation')
    ax.set_xticks(ind+width)
    ax.set_xticklabels( ('Methodology', 'Audio Vision', 'Course Material', 'Arrangement', 'Overall Opinion') )
    ax.legend( (rects1[0], rects2[0]), ('Ranking', 'Maximum Ranking') )

    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                    ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    plt.savefig("figure.jpg",dpi=(75))
    ######################################################################33

    ind = np.arange(F)  
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, ranking_fe, width, color='b',yerr=0)
    rects2 = ax.bar(ind+width, maximum_ranking_fe , width, color='r', yerr=0)

    ax.set_title('Faculty Evaluation')
    ax.set_xticks(ind+width)
    ax.set_xticklabels( ('Subject Knowledge', 'Presentation Skill', 'Communication', 'Interation skills') )
    ax.legend( (rects1[0], rects2[0]), ('Ranking', 'Maximum Ranking') )

    def autolabel1(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                    ha='center', va='bottom')

    autolabel1(rects1)
    autolabel1(rects2)

    plt.savefig("figure1.jpg",dpi=(75))

    ######################################################################

    Image.open('figure.jpg').convert("RGB").save('figure.bmp')    
    wsheet.insert_bitmap('figure.bmp',20 + 13 ,0)

    Image.open('figure1.jpg').convert("RGB").save('figure1.bmp')    
    wsheet.insert_bitmap('figure1.bmp',20 + 13,5)

    wb.save(file_location)

"""

# -*- coding: cp1252 -*-
import xlrd
import time
from xlwt import*

def make_calendar(file_location , coursedata ,year):


    wb = Workbook()
    wsheet = wb.add_sheet('Training Plan Staff & Workmen')
    wsheet.set_panes_frozen(True)
    wsheet.set_vert_split_pos(3)  

    wsheet.col(0).width = 1500 
    wsheet.col(1).width = 6666
    wsheet.col(2).width = 6666
    wsheet.col(3).width = 3333
    wsheet.col(4).width = 3333

    i=5
    for i in range(5 , 66 ):
        wsheet.col(i).width = 2222

    wsheet.col(67).width = 3333 

    fontname = Font()
    fontname.size = 10
    fontname.name = "Arial"
    fontname.colour_index = 0
    fontname.bold = True

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


    stylename = XFStyle()
    stylename.font = fontname
    stylename.alignment = alignment
    stylename.borders = bordername

    stylename1 = XFStyle()
    stylename1.font = fontname
    stylename1.alignment = alignmentleft
    stylename1.borders = bordername


    wsheet.write_merge(0,0,0,67,"",stylename)
    wsheet.write_merge(1,1,3,67,"TRAINING CALENDAR -"+year,stylename)
    wsheet.write_merge(3,3,0,65,"",stylename)
    wsheet.write_merge(3,3,66,67,"L4-PA-12-CR ",stylename)
    wsheet.write_merge(1,1,0,2," Fill it with Capital 'P' ",stylename)

    j=1
    wsheet.write_merge(4,5,0,0,"SL. NO.",stylename) # sno heading
    wsheet.write_merge(4,5,1,1,"TOPICS",stylename) #coursename heading
    wsheet.write_merge(4,5,2,2, "DEPTS",stylename) #depts heading
    wsheet.write_merge(4,5,3,3, "CAT",stylename) #cat heading
    wsheet.write_merge(4,5,4,4,"NO. of PERSONS",stylename1) #no of persons heading


    for row in range(6,5 + 2*(len(coursedata)),2):          # 81 + 1 = 6 + 2*no.of courses "here 38"...from the database   
        wsheet.write_merge(row,row+1,0,0,j,stylename) # sno
        wsheet.write_merge(row,row+1,1,1,coursedata[j-1].course_name,stylename) #coursename
        wsheet.write_merge(row,row+1,2,2,coursedata[j-1].departments,stylename) #depts
        wsheet.write_merge(row,row+1,3,3,"W/S",stylename) #cat
        wsheet.write_merge(row,row+1,4,4,coursedata[j-1].wscount,stylename) # no. of persons
        j = j + 1
    i=5
    wsheet.write_merge(4,4,5,9,"January",stylename)
    wsheet.write_merge(4,4,10,14,"February",stylename)
    wsheet.write_merge(4,4,15,19,"March",stylename)
    wsheet.write_merge(4,4,20,24,"April",stylename)
    wsheet.write_merge(4,4,25,29,"May",stylename)
    wsheet.write_merge(4,4,30,34,"June",stylename)
    wsheet.write_merge(4,4,35,39,"July",stylename)
    wsheet.write_merge(4,4,40,44,"August",stylename)
    wsheet.write_merge(4,4,45,49,"September",stylename)
    wsheet.write_merge(4,4,50,54,"October",stylename)
    wsheet.write_merge(4,4,55,59,"November",stylename)
    wsheet.write_merge(4,4,60,64,"December",stylename)

    wsheet.write_merge(4,5,65,65,"I",stylename)
    wsheet.write_merge(4,5,66,66,"E",stylename)
    wsheet.write_merge(4,5,67,67,"Faculty/Name",stylename)
    i=5
    j= 1
    k=1
    for i in range(5,65):
        if(j == 6):
            j = 1
            k = k + 1
        wsheet.write(5,i,"week "+ str(j),stylename)
        j = j + 1
    i=5
    j=6
    for j in range(6,6 + 2*(len(coursedata)),2):
        for i in range(5,68):
            wsheet.write_merge(j,j+1,i,i,"",stylename)

    wb.save(file_location)

# -*- coding: cp1252 -*-
import xlrd
import time
from xlwt import*

def read_calendar(file_location,year):
    workbookread = xlrd.open_workbook(file_location);
    sheetread = workbookread.sheet_by_index(0)
    i=6
    j=5
    for i in range (6,81,2):             # 81 + 1 (one merged cell) = 6 + 2*no.of courses "here 38 courses"...from the database
        k=0
        for j in range(5,65):
            if(sheetread.cell_value(i,j) == 'P'):
                k=k+1
                s = 'batch '+ str(k) +' of ' + str(sheetread.cell_value(i,1)) + ' is on ' + str(sheetread.cell_value(5,j)) + '  ' + str(sheetread.cell_value(4,j - j%5))
                start_date,stop_date = to_date(str(sheetread.cell_value(5,j)) , str(sheetread.cell_value(4,j - j%5)) , year)
                course = Course.objects.get(course_name = str(sheetread.cell_value(i,1)) )
                BatchDetails.objects.create()
                print s
def get_month(month):
    if month.lower() == 'january':
        return 1
    if month.lower() == 'february':
        return 2
    if month.lower() == 'march':
        return 3
    if month.lower() == 'april':
        return 4
    if month.lower() == 'may':
        return 5
    if month.lower() == 'june':
        return 6
    if month.lower() == 'july':
        return 7
    if month.lower() == 'august':
        return 8
    if month.lower() == 'september':
        return 9
    if month.lower() == 'october':
        return 10
    if month.lower() == 'november':
        return 11
    if month.lower() == 'december':
        return 12
def to_date(week,month,year):
    num = week[5]
    num = int(num)
    month = get_month(month)
    if num == 1:
        start_date = datetime(year,month )
# k is the batch number
# sheetread.cell_value(i,1) is the course name .. match it with the data base
# sheetread.cell_value(5,j) is the week in which P is marked
# sheetread.cell_value(4,j - j%5) is the name of the month


# -*- coding: cp1252 -*-
import xlrd
import time
from xlwt import*

def make_l4pa9(batch , departments, trainers , grades ,file_location):
    trainerNames = []
    for trainer in trainers:
        trainerNames.append(trainer.userObj.first_name + " " + trainer.userObj.last_name)
    wb = Workbook()
    for department in departments:
        wsheet = wb.add_sheet(department.dept_name)
        wsheet.show_grid = False
        i=0
        for i in range(1,16):
            wsheet.col(i).width = 2700
        i=0
        for i in range(1,100):
            wsheet.row(i).height_mismatch = True
            wsheet.row(i).height = 400


        fontname = Font()
        fontname.name = "Arial"
        fontname.colour_index = 0
        fontname.bold = True


        fonthead = Font()
        fonthead.name = "Arial"
        fonthead.height = 360
        fonthead.colour_index = 0
        fonthead.bold = True

        fontbody = Font()
        fontbody.name = "Arial"
        fontbody.height = 230
        fontbody.colour_index = 0
        fontbody.bold = False

        fontnew = Font()
        fontnew.name = "Arial"
        fontnew.underline = True
        fontnew.height = 280
        fontnew.colour_index = 0
        fontnew.bold = True

        fontnew2 = Font()
        fontnew2.name = "Arial"
        fontnew2.height = 230
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
        stylehead.borders = bordername

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

        wsheet.write_merge(0,0,0,14, "TRAINING EVALUATION FORMAT",stylehead)
        wsheet.write_merge(1,1,14,14,"L4-PA-9",stylebody)
        wsheet.write_merge(2,2,0,7,"Title of the Programme:" + batch.course.course_name, stylebody) ####
        wsheet.write_merge(2,2,8,14,"Faculty:" + ','.join(trainerNames) , stylebody)   ###
        wsheet.write_merge(3,3,0,7,"Date:" + str(datetime.datetime.today()) , stylebody)        ###
        wsheet.write_merge(3,3,8,14,"Duration:" + batch.course.duration , stylebody)  ###
        wsheet.write_merge(4,4,0,14, "Nature of the programme:",styletitle)
        wsheet.write_merge(5,5,0,7,"Technical:" , stylebody)   ###
        wsheet.write_merge(5,5,8,14,"Behavioral:"  , stylebody)    ###

        wsheet.write_merge(6,7,0,14,"Objective of the Programme:" + batch.course.objective, stylebody)  ###
        wsheet.write_merge(8,8,0,14,"PART A", styletitle)
        wsheet.write_merge(9,9,0,14,"Expectations from the Programme being Evaluated" , styletitle)

        #headings only
        wsheet.write_merge(10,10,0,2,"Productivity",styletitle)
        wsheet.write_merge(10,10,3,5,"Quality Improvement",styletitle)
        wsheet.write_merge(10,10,6,8,"Improvement in M/c Uptime",styletitle)
        wsheet.write_merge(10,10,9,11,"Reduction of wastages",styletitle)
        wsheet.write_merge(10,10,12,14,"Others( Pls Specify )",styletitle)

        wsheet.write_merge(11,14,0,2,batch.course.productivity,stylebody) ### Productiveity
        wsheet.write_merge(11,14,3,5,batch.course.quality_improvement,stylebody) ### Quality improvement
        wsheet.write_merge(11,14,6,8,batch.course.reduction_time,stylebody) ### Improvement in m/c uptime
        wsheet.write_merge(11,14,9,11,batch.course.reduction_wastage,stylebody) ### Reduction of wastages
        wsheet.write_merge(11,14,12,14,batch.course.others,stylebody)### others (pls specify)


        #heading only
        wsheet.write_merge(15,15,0,14,"PART B", styletitle)
        wsheet.write_merge(16,17,0,0,"Sl. No.", styletitle)
        wsheet.write_merge(16,17,1,3,"Names", styletitle)
        wsheet.write_merge(16,16,4,7,"Assessment in Scale of 1 - 10", styletitle)
        wsheet.write_merge(16,16,8,14,"", styletitle)
        wsheet.write_merge(17,17,4,5,"Pre-Training", styletitle)
        wsheet.write_merge(17,17,6,7,"Post-Training", styletitle)
        wsheet.write_merge(17,17,8,10,"Retraining is Required", styletitle)
        wsheet.write_merge(17,17,11,14,"Probable date of retraining", styletitle)
        i=0

        for i in range (1,len(grades)+1):
            wsheet.write_merge(17+i,17+i,0,0,i, styletitle)
            wsheet.write_merge(17+i,17+i,1,3,grades[i-1].employee.userObj.first_name + " " + grades[i-1].employee.userObj.last_name, styletitle) #name
            wsheet.write_merge(17+i,17+i,4,5,grades[i-1].pre_training, styletitle)    #pre-training assesment
            wsheet.write_merge(17+i,17+i,6,7,grades[i-1].post_training, styletitle)    #post-training assesment
            wsheet.write_merge(17+i,17+i,8,10,str(grades[i-1].retraning_needed), styletitle)   #retraining required?
            wsheet.write_merge(17+i,17+i,11,14,str(grades[i-1].probable_date_of_retraining), styletitle)  #Probable date of retraining

        wsheet.write_merge(18 + 4, 18+4,0,14,"",stylebody)
        wsheet.write_merge(19 + 4, 19+4,0,14,"*Scale: 0-1: No Improvements, 2-3: Very Small Improvements, 4-5: Reasonable Improvements, 6-8: Significant Improvements, 9-10: Excellent ",stylebody)
        wsheet.write_merge(20 + 4, 20+4,0,14,"Significant Improvements:",stylebody)
        wsheet.write_merge(21 + 4, 23+4,0,14,"#",stylebody) ## significant improvements if any
        wsheet.write_merge(24 + 4, 24+4,0,4,"Supporting data if any for Training effectiveness:",styletitle)
        wsheet.write_merge(24 + 4, 24+4,5,14,"",stylebody) 

        wsheet.write_merge(25 + 4, 28+4,0,14,"#",stylebody)#supporting data if any for training effectivness

        wsheet.write_merge(29 + 4, 29+4,0,4,"Signature of HOD",styletitle)
        wsheet.write_merge(29 + 4, 29+4,10,14,"Signature of HR",styletitle)
        wsheet.write_merge(29 + 4, 29+4,5,9,"",stylebody)




    wb.save(file_location)
   
# -*- coding: cp1252 -*-
import xlrd
import time
from xlwt import*

def make_l4pa2(file_location,departments,courses):    ####

    wb = Workbook()
    
    for department in departments:     
        employees = department.get_employees()             ####
        wsheet = wb.add_sheet(department.department_name)      ####
        wsheet.col(0).width = 1500 
        wsheet.col(1).width = 3333
        wsheet.col(2).width = 6666
        i=3
        for i in range(3 , 23 ):
            wsheet.col(i).width = 1000 
           

        fontname = Font()
        fontname.name = "Arial"
        fontname.colour_index = 0
        fontname.bold = True

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


        stylename = XFStyle()
        stylename.font = fontname
        stylename.alignment = alignment
        
        stylenew = XFStyle()
        stylenew.font = fontname
        stylenew.alignment = alignment
        stylenew.borders = bordername
        
        stylenew1 = XFStyle()
        stylenew1.font = fontname
        stylenew1.alignment = alignment1
        stylenew.borders = bordername
        
        wsheet.write_merge(1,1,0,23,"TRAINING INDENT - ANNUAL",stylename)
        wsheet.write_merge(2,2,0,2,"Department: Prodution Unit 5",stylename)
        wsheet.write_merge(2,2,12,14,"Fillied on:",stylename)
        wsheet.write_merge(2,2,15,18,time.strftime("%d-%m-%Y"),stylename)
        wsheet.write_merge(2,2,19,22,time.strftime("%H:%M:%S"),stylename)
        wsheet.write_merge(3,3,20,23,"L4-PA-2",stylename)
        wsheet.write_merge(5,5,0,23,"Note: Please refer the below mentioned Modules and tick the relevant columns for specific training needs which you would like to be fulfilled.",stylename)

        #table begins
        wsheet.write_merge(7,8,0,0," Sl. No. ",stylenew) 
        wsheet.write_merge(7,8,1,1," EMP No. ",stylenew)    
        wsheet.write_merge(7,8,2,2," Name ",stylenew)
        wsheet.write_merge(7,7,3, len(courses) + 3 - 1," Module ",stylenew)  ####
        wsheet.write_merge(7,8,len(courses) + 3, len(courses) + 3," remarks ",stylenew)
        wsheet.col(len(courses) + 3).width = 3333 
        for i in range (3,len(courses) + 3 -1 + 1):                      ##
            wsheet.write_merge(8,8,i,i,i-2,stylenew)

        for row in range ( 9, 9 + len(employees)):
            wsheet.write(row,0,row-8,stylenew)
            wsheet.write(row,1,employees[row-9].userId,stylenew)
            wsheet.write(row,2,employees[row-9].name,stylenew)
            col = 3
            dictn= employees[row-9].getcourses()
            print dictn
            for col in range ( 3, 3 + len(courses) + 1):  
                wsheet.write(row,col,dictn.get(col-2 , ' '),stylenew)


        row = row + 4;
        wsheet.write_merge(row,row,0,2 ," DATE ",stylename)
        wsheet.write_merge(row,row,3,14 ," Name of HOD: "  + department.hod,stylename)
        wsheet.write_merge(row,row,15,23 ," Signature of HOD ",stylename)

        row = row + 2
        j=0

        # the course list(full) from the data base no need for you arjun
        i=1
        for course in courses:
            wsheet.write_merge(row,row,0,15 ,str(i) + ". " + course.course_name,stylenew1)
            i = i + 1
            row = row + 1
        

    wb.save(file_location)

