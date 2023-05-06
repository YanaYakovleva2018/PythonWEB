from datetime import datetime
import faker
from random import randint
import sqlite3
from create_db import *

fake_data = faker.Faker(locale='uk_UA')

NUMBER_STUDENTS = 30
NUMBER_GROUPS = 3
NUMBER_SUBJECTS = 8
NUMBER_TEACHERS = 5
NUMBER_GRADES = 150

def prepare_fake_data() -> tuple():

    for_fake_groups = []

    for _ in range(NUMBER_GROUPS):
        for_fake_groups.append((fake_data.bothify(text='Group ?#'),))

    for_fake_students = []

    for _ in range(NUMBER_STUDENTS ):
        name = fake_data.name()
        *_, firstname, lastname = name.split(' ')
        for_fake_students.append((name, firstname, lastname, randint(1, len(for_fake_groups))))

    for_fake_teachers = []

    for _ in range(NUMBER_TEACHERS):
        name = fake_data.name()
        *_, firstname, lastname = name.split(' ')
        for_fake_teachers.append((name, firstname, lastname))

    for_fake_subjects =[]

    for _ in range(NUMBER_SUBJECTS):
        for_fake_subjects.append((fake_data.job(), randint(1, len(for_fake_teachers))))

    for_fake_grades = []

    for _ in range(NUMBER_GRADES):
        for_fake_grades.append((randint(4, 12), randint(1, len(for_fake_students)), randint(1, len(for_fake_subjects)),
                           fake_data.date_between_dates(datetime(2022, 1, 1), datetime(2022, 12, 31))))
  
    return for_fake_students,for_fake_groups, for_fake_subjects, for_fake_teachers, for_fake_grades

def insert_data_to_db(students, groups, subjects, teachers, grades) -> None:

    with sqlite3.connect('university.db') as connect:
        cur = connect.cursor()

        sql_to_students = """INSERT INTO students(fullname, firstname, lastname, group_id)
                               VALUES (?, ?, ?, ?)"""
        cur.executemany(sql_to_students, students)

        sql_to_groups = """INSERT INTO groups(name)
                               VALUES (?)"""
        cur.executemany(sql_to_groups, groups)

        sql_to_subjects = """INSERT INTO subjects(name, teacher_id)
                              VALUES (?, ?)"""
        cur.executemany(sql_to_subjects, subjects)

        sql_to_teachers = """INSERT INTO teachers(fullname, firstname, lastname)
                              VALUES (?, ?, ?)"""
        cur.executemany(sql_to_teachers, teachers)

        sql_to_grades = """INSERT INTO grades(grade, student_id, subject_id, date_of)
                              VALUES (?, ?, ?, ?)"""
        cur.executemany(sql_to_grades, grades)

        connect.commit()
    
if __name__ == "__main__":
    create_db()
    students, groups, subjects, teachers, grades = prepare_fake_data()
    insert_data_to_db(students, groups, subjects, teachers, grades)

 

