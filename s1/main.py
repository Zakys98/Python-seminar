from d_shelter import *
from datetime import date

s = Shelter()
a = s.add_animal(name='Hoo', year_of_birth=197, gender='as',
                 date_of_entry=date(1995, 10, 9), species='sad', breed='fd')
b = s.add_animal(name='Pisk', year_of_birth=1, gender='2',
                 date_of_entry=date(1995, 10, 9), species='asd', breed='fd')
s.add_foster_parent(name='ZOO Liberec', address='sdf',
                    phone_number='241', max_animals=1)
l = s.available_foster_parents(date=date(2020, 10, 9))
print(l)

a.start_foster(date(2018, 5, 10), l[0])
l = s.available_foster_parents(date=date(2018, 5, 11))
a.end_foster(date(2018, 5, 12))
l = s.available_foster_parents(date=date(2018, 5, 13))
a.start_foster(date(2018, 5, 5), l[0])
try:
    a.start_foster(date(2018, 5, 1), l[0])
except RuntimeError:
    print('1')
a.end_foster(date(2018, 5, 9))

a.start_foster(date(2010, 6, 15), l[0])
try:
    a.start_foster(date(2010, 6, 15), l[0])
except RuntimeError:
    print('2')
try:
    a.start_foster(date(2010, 5, 5), l[0])
except RuntimeError:
    print('3')
try:
    a.start_foster(date(2010, 7, 25), l[0])
except RuntimeError:
    print('4')
a.end_foster(date(2010, 6, 17))


#after
a.start_foster(date(2020, 10, 8), l[0])
try:
    b.start_foster(date(2020, 10, 9), l[0])
except RuntimeError:
    print('5')
a.start_foster(date(2020, 9, 9), l[0], date(2020, 9, 15))
a.start_foster(date(2020, 9, 17), l[0], date(2020, 9, 20))
try:
    a.start_foster(date(2020, 9, 8), l[0])
except RuntimeError:
    print('6')
try:
    a.start_foster(date( 2020, 11, 8 ), l[0])
except RuntimeError:
    print('7')
l = s.available_foster_parents(date=date(2020, 10, 15))
print(l)
a.end_foster(date(2020, 10, 15))
try:
    a.end_foster(date(2020, 10, 15))
except RuntimeError:
    print('8')
l = s.available_foster_parents(date=date(2020, 10, 7))
try:
    a.start_foster(date(2020, 10, 8), l[0])
except RuntimeError:
    print('9')

try:
    a.start_foster(date(2020, 9, 18), l[0], date(2020, 9, 19))
except RuntimeError:
    print('10')
try:
    a.start_foster(date(2020, 9, 16), l[0], date(2020, 9, 21))
except RuntimeError:
    print('11')
try:
    a.start_foster(date(2020, 9, 19), l[0], date(2020, 9, 21))
except RuntimeError:
    print('12')
try:
    a.start_foster(date(2020, 9, 16), l[0], date(2020, 9, 18))
except RuntimeError:
    print('13')
try:
    a.start_foster(date(2020, 9, 16), l[0], date(2020, 9, 17))
except RuntimeError:
    print('14')
try:
    a.start_foster(date(2020, 9, 20), l[0], date(2020, 9, 25))
except RuntimeError:
    print('15')

a.adopt(date(2021, 6, 30))
a.start_foster(date(2010, 7, 25), l[0], date(2010, 7, 28))
try:
    a.start_foster(date(2010, 4, 25), l[0])
except RuntimeError:
    print('16')
try:
    a.start_foster(date(2021, 6, 29), l[0], date(2021, 7, 28))
except RuntimeError:
    print('17')
try:
    a.start_foster(date(2021, 7, 1), l[0], date(2021, 7, 28))
except RuntimeError:
    print('18')

#a.adopt(date( 2020, 10, 7 ), 'name')
l = s.available_foster_parents(date=date(2020, 10, 16))
print(l)



s = Shelter()
a = s.add_animal(name='Hoo', year_of_birth=1000, gender='as',
                 date_of_entry=date(1000, 10, 15), species='sad', breed='fd')
try:
    b = s.add_animal(name='Hoo', year_of_birth=1500, gender='as',
                     date_of_entry=date(1000, 10, 15), species='sad', breed='fd')
except RuntimeError:
    print('nice catch')
#c = s.add_animal( name = 'Hoo', year_of_birth = 2007, gender = 'as', date_of_entry = date( 1000, 10, 7 ), species = 'sad', breed = 'fd', adoption_date=(date(1000, 10, 9)))
# try:
#    s.add_animal( name = 'Hoo', date_of_entry = date( 1000, 10, 5 ), species = 'sad', breed = 'fd', adoption_date=(date(1000, 10, 10)))
# except RuntimeError:
#    print('nice catch')
#s.add_animal( name = 'Hoo', date_of_entry = date( 1000, 10, 10 ), species = 'sad', breed = 'fd', adoption_date=(date(1000, 10, 12)))
# try:
#    s.add_animal( name = 'Hoo', date_of_entry = date( 1000, 10, 13 ), species = 'sad', breed = 'fd', adoption_date=(date(1000, 10, 15)))
# except RuntimeError:
#    print('nice catch')
# try:
#    s.add_animal( name = 'Hoo', date_of_entry = date( 1000, 10, 19 ), species = 'sad', breed = 'fd')
# except RuntimeError:
#    print('nice catch')
# try:
#    s.add_animal( name = 'Hoo', date_of_entry = date( 1000, 10, 17 ), species = 'sad', breed = 'fd', adoption_date=(date(1000, 10, 18)))
# except RuntimeError:
#    print('nice catch')
a.adopt(date=date(1000, 10, 19), adopter_name='name')
# try:
#    s.add_animal( name = 'Hoo', date_of_entry = date( 1000, 10, 19 ), species = 'sad', breed = 'fd')
# except RuntimeError:
#    print('nice catch')
#s.add_animal(name='Hoo', date_of_entry=date(1000, 10, 20),
#             species='sad', breed='fd', adoption_date=(date(1000, 10, 22)))
#s.add_animal(name='Hoo', date_of_entry=date(1000, 10, 22),
#             species='sad', breed='fd', adoption_date=(date(1000, 10, 23)))
# jeste to radsi zkontrolovat jestli to je vsechno
