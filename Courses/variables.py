'''
Created on Jun 17, 2014

@author: Arjun
'''
name_choices = (('L4PA1','L4PA1'),('L4PA2','L4PA2'),('L4PA3','L4PA3'),('L4PA4','L4PA4'),
                    ('L4PA5','L4PA5'),('L4PA6','L4PA6'),('L4PA7','L4PA7'),('L4PA8','L4PA8'),
                    ('L4PA9','L4PA9'),('L4PA10','L4PA10'),('L4PA11','L4PA11'),('AC','Annual Calendar'),
                    ('TI','Training Indent'),('ITR','Training Records'),('OTH','Others'),)   

year_choices = (('2014','2014'),)  
for year in range(2015, 2060):
    year_choices = year_choices + ((str(year),str(year)),)
    