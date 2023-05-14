from sqlalchemy import   func, desc, select, and_

from database.models import Teacher, Student, Discipline, Grade, Group
from database.connect_db import session

def select_1():
    """
    SELECT students.fullname, ROUND(AVG(grades.grade), 2) AS avg_grade
    FROM grades
    LEFT JOIN students ON students.id = grades.student_id
    GROUP BY students.id
    ORDER BY avg_grade DESC LIMIT 5;
    """
    result = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade'))\
        .select_from(Grade).join(Student)\
        .group_by(Student.id).order_by(desc('average_grade')).limit(5).all()
    return result


def select_2(discipline_id):
    """
    SELECT subjects.name, students.fullname, round(avg(grades.grade), 2) AS avg_grade
    FROM grades
    LEFT JOIN students ON students.id = grades.student_id
    LEFT JOIN subjects ON subjects.id = grades.subject_id
    WHERE subjects.id = 1
    GROUP BY students.id, subjects.id
    ORDER BY avg_grade DESC LIMIT 1;
    """
    result = session.query(Discipline.name, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Student)\
        .join(Discipline).filter(Discipline.id == discipline_id)\
        .group_by(Student.id, Discipline.name)\
        .order_by(desc('average_grade')).limit(1).all()
    return result


def select_3(discipline_id):
    """
    SELECT subjects.name, groups.name, round(avg(grades.grade), 2) AS grade
    FROM grades
    LEFT JOIN students ON students.id = grades.student_id
    LEFT JOIN subjects ON subjects.id = grades.subject_id
    LEFT JOIN groups ON groups.id = students.group_id
    WHERE subjects.id = 2
    GROUP BY groups.id
    ORDER BY grade DESC;
    """
    result = session.query(Discipline.name, Group.name, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Student)\
        .join(Discipline).join(Group).filter(Discipline.id == discipline_id)\
        .group_by(Group.name, Discipline.name).order_by(desc('average_grade')).all()
    return result


def select_4():
    """
    SELECT round(avg(grade),2) AS avg_grade
    FROM grades;
    """
    result = session.query(func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).all()
    return result


def select_5(teacher_id):
    """
    SELECT teachers.fullname, subjects.name
    FROM teachers
    LEFT JOIN subjects ON subjects.teacher_id = teachers.id
    WHERE teachers.id = 2;
    """
    result = session.query(Teacher.fullname, Discipline.name) \
        .select_from(Discipline).join(Teacher)\
        .filter(Teacher.id == teacher_id)\
        .order_by(Discipline.name).all()
    return result


def select_6(group_id):
    """
    SELECT students.id, students.fullname, groups.name
    FROM students
    LEFT JOIN groups ON groups.id = students.group_id
    WHERE groups.id = 1;
    """
    result = session.query(Group.name, Student.fullname) \
        .select_from(Student).join(Group)\
        .filter(Group.id == group_id)\
        .order_by(Student.fullname).all()
    return result


def select_7(group_id, discipline_id):
    """
    SELECT subjects.name, groups.name, students.fullname, grades.date_of, grades.grade
    FROM grades
    LEFT JOIN students ON students.id = grades.student_id
    LEFT JOIN subjects ON subjects.id = grades.subject_id
    LEFT JOIN groups ON groups.id = students.group_id
    WHERE subjects.id = 2 AND groups.id = 1;
    """
    result = session.query(Group.name, Discipline.name, Student.fullname, Grade.grade, Grade.date_of) \
        .select_from(Grade).join(Student)\
        .join(Group).join(Discipline)\
        .filter(and_(Group.id == group_id, Discipline.id == discipline_id))\
        .order_by(Student.fullname, Grade.date_of).all()
    return result


def select_8(teacher_id):
    """
    SELECT teachers.fullname, round(avg(grades.grade), 2) AS avg_grade
    FROM grades
    LEFT JOIN subjects ON subjects.id = grades.subject_id
    LEFT JOIN teachers ON teachers.id = subjects.teacher_id
    WHERE teachers.id = 3
    GROUP BY teachers.fullname;
    """
    result = session.query(Teacher.fullname, Discipline.name, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Teacher).join(Discipline)\
        .join(Grade).filter(Teacher.id == teacher_id)\
        .group_by(Discipline.name, Teacher.fullname)\
        .order_by(Discipline.name).all()
    return result


def select_9(student_id):
    """
    SELECT students.fullname, subjects.name
    FROM grades
    LEFT JOIN students ON students.id = grades.student_id
    LEFT JOIN subjects ON subjects.id = grades.subject_id
    WHERE grades.student_id = 1
    GROUP BY subjects.name;
    """
    result = session.query(Student.fullname, Discipline.name) \
        .select_from(Discipline).join(Grade).join(Student)\
        .filter(Student.id == student_id)\
        .group_by(Discipline.name, Student.fullname)\
        .order_by(Discipline.name).all()
    return result


def select_10(teacher_id, student_id):
    """
    SELECT students.fullname,subjects.name, teachers.fullname
    FROM grades
    LEFT JOIN students ON students.id = grades.student_id
    LEFT JOIN subjects ON subjects.id = grades.subject_id
    LEFT JOIN teachers ON teachers.id = grades.subject_id
    WHERE grades.student_id = 1 AND teachers.id = 2
    GROUP BY subjects.id, students.fullname, teachers.fullname ;
    """
    result = session.query(Teacher.fullname, Student.fullname, Discipline.name) \
        .select_from(Discipline).join(Teacher)\
        .join(Grade).join(Student)\
        .filter(and_(Teacher.id == teacher_id, Student.id == student_id))\
        .group_by(Discipline.name, Teacher.fullname, Student.fullname)\
        .order_by(Discipline.name).all()
    return result


def select_11(teacher_id, student_id):
    """
    SELECT students.fullname, teachers.fullname, round(avg(grades.grade), 2) AS avg_grade
    FROM grades
    LEFT JOIN students ON students.id = grades.student_id
    LEFT JOIN subjects ON subjects.id = grades.subject_id
    LEFT JOIN teachers ON teachers.id = subjects.teacher_id
    WHERE grades.student_id = 1 AND teachers.id = 2
    GROUP BY students.fullname, teachers.fullname;
    """
    result = session.query(Teacher.fullname, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Discipline)\
        .join(Teacher).join(Student)\
        .filter(and_(Teacher.id == teacher_id, Student.id == student_id))\
        .group_by(Teacher.fullname, Student.fullname).all()
    return result


def select_12(group_id, discipline_id):
    """
    SELECT subjects.name, groups.name, students.fullname, grades.date_of, grades.grade
    FROM grades
    LEFT JOIN students ON students.id = grades.student_id
    LEFT JOIN subjects ON subjects.id = grades.subject_id
    LEFT JOIN groups ON groups.id = students.group_id
    WHERE subjects.id = 1 AND groups.id = 2 AND grades.date_of = (SELECT MAX(g.date_of)
    FROM grades AS g
    LEFT JOIN students ON students.id = g.student_id
    LEFT JOIN groups ON groups.id = students.group_id
    WHERE g.subject_id = 1 AND g.id = 2)
    order BY grades.date_of DESC
    """
    subquery = (select(func.max(Grade.date_of)).join(Student).join(Group).filter(
        and_(Group.id == group_id, Grade.discipline_id == discipline_id)).scalar_subquery())
    result = session.query(Group.name, Student.fullname, Discipline.name, Grade.grade, Grade.date_of) \
        .select_from(Grade).join(Discipline)\
        .join(Student).join(Group)\
        .filter(and_(Group.id == group_id, Discipline.id == discipline_id, Grade.date_of == subquery))\
        .order_by(Student.fullname).all()
    return result


if __name__ == '__main__':
    print(select_1())
    #print(select_2(1))
    #print(select_3(1))
    #print(select_4())
    #print(select_5(1))
    #print(select_6(1))
    #print(select_7(1, 1))
    #print(select_8(1))
    #print(select_9(1))
    #print(select_10(1, 1))
    #print(select_11(1, 1))
    #print(select_12(1, 1))