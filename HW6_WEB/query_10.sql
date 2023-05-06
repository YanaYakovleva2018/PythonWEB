-- A list of courses taught to a particular student by a particular teacher.
SELECT students.fullname,subjects.name, teachers.fullname
FROM grades
LEFT JOIN students ON students.id = grades.student_id
LEFT JOIN subjects ON subjects.id = grades.subject_id
LEFT JOIN teachers ON teachers.id = grades.subject_id
WHERE grades.student_id = 1 AND teachers.id = 2
GROUP BY subjects.id, students.fullname, teachers.fullname ;