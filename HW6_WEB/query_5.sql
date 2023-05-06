-- Find what courses a particular teacher teaches.
SELECT teachers.fullname, subjects.name
FROM teachers
LEFT JOIN subjects ON subjects.teacher_id = teachers.id
WHERE teachers.id = 2;