-- Find the student with the highest GPA in a particular subject.
SELECT subjects.name, students.fullname, round(avg(grades.grade), 2) AS avg_grade
FROM grades
LEFT JOIN students ON students.id = grades.student_id
LEFT JOIN subjects ON subjects.id = grades.subject_id
WHERE subjects.id = 1
GROUP BY students.id, subjects.id
ORDER BY avg_grade DESC LIMIT 1;