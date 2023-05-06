-- Find the average score on the stream (across the entire scoreboard).
SELECT round(avg(grade),2) AS avg_grade
FROM grades;