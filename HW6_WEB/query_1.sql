-- Find the 5 students with the highest GPA across all subjects.
SELECT students.fullname, ROUND(AVG(grades.grade), 2) AS avg_grade
FROM grades
LEFT JOIN students ON students.id = grades.student_id
GROUP BY students.id
ORDER BY avg_grade DESC LIMIT 5;