-- The average score given by a particular teacher to a particular student.
SELECT students.fullname, teachers.fullname, round(avg(grades.grade), 2) AS avg_grade
FROM grades
LEFT JOIN students ON students.id = grades.student_id
LEFT JOIN subjects ON subjects.id = grades.subject_id
LEFT JOIN teachers ON teachers.id = subjects.teacher_id
WHERE grades.student_id = 1 AND teachers.id = 2
GROUP BY students.fullname, teachers.fullname;