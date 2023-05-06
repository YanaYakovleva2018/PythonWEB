-- Find the average score given by a certain teacher in his subjects.
SELECT teachers.fullname, round(avg(grades.grade), 2) AS avg_grade
FROM grades
LEFT JOIN subjects ON subjects.id = grades.subject_id
LEFT JOIN teachers ON teachers.id = subjects.teacher_id
WHERE teachers.id = 3
GROUP BY teachers.fullname;