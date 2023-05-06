-- Find a list of courses that the student is taking.
SELECT students.fullname, subjects.name
FROM grades
LEFT JOIN students ON students.id = grades.student_id
LEFT JOIN subjects ON subjects.id = grades.subject_id
WHERE grades.student_id = 1
GROUP BY subjects.name;