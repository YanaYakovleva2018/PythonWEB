import sqlite3
import sys

help_for_user = """Choose which request you want to perform?
0  -- Exit
1  -- Find the 5 students with the highest GPA in all subjects.
2  -- Find the student with the highest GPA in a particular subject.
3  -- Find the average score in groups for a certain subject.
4  -- Find the average score on the stream (across the entire scoreboard).
5  -- Find what courses a particular teacher teaches.
6  -- Find a list of students in a specific group.
7  -- Find the grades of students in a separate group for a specific subject.
8  -- Find the average score given by a certain teacher in his subjects.
9  -- Find the list of courses that the student is attending.
10 -- List of courses taught to a specific student by a specific teacher.
11 -- The average score given by a particular teacher to a particular student.
12 -- Grades of students in a certain group on a certain subject in the last session.
"""

def execute_query(file):
    with open(file) as f:
        sql = f.read()

    with sqlite3.connect('university.db') as con:
        cursor = con.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    
def main():
    print(help_for_user)
   
    while True:
        number = int(input("Choose the request number: "))
        if number == 0:
            sys.exit()
        result = execute_query(f'query_{number}.sql')
        print(result)

if __name__ == '__main__':
    try:
        exit(main())
    except KeyboardInterrupt:
        exit()