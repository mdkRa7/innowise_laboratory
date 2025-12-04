-- school_queries.sql
-- Complete SQL script for School Database Assignment
-- Contains: Table creation, data insertion, indexes, and queries

-- ======================================================
-- PART 1: DATABASE SCHEMA CREATION
-- ======================================================

-- Students table: Stores basic student information
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,      -- Unique identifier for each student
    full_name TEXT NOT NULL,                   -- Student's full name
    birth_year INTEGER NOT NULL                -- Year of birth
);

-- Grades table: Stores academic performance records
CREATE TABLE grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,      -- Unique identifier for each grade record
    student_id INTEGER NOT NULL,               -- Reference to student (foreign key)
    subject TEXT NOT NULL,                     -- Name of the subject/course
    grade INTEGER NOT NULL,                    -- Grade value (0-100 scale)

    -- Foreign key constraint ensures data integrity
    FOREIGN KEY (student_id) REFERENCES students(id)
        ON DELETE CASCADE                      -- If student is deleted, grades are also deleted
        ON UPDATE CASCADE                      -- If student id changes, grades are updated
);

-- ======================================================
-- PART 2: SAMPLE DATA INSERTION
-- ======================================================

-- Insert 9 sample students with their birth years
INSERT INTO students (full_name, birth_year) VALUES
('Alice Johnson', 2005),    -- Student 1
('Brian Smith', 2004),      -- Student 2
('Carla Reyes', 2006),      -- Student 3
('Daniel Kim', 2005),       -- Student 4
('Eva Thompson', 2003),     -- Student 5
('Felix Nguyen', 2007),     -- Student 6
('Grace Patel', 2005),      -- Student 7
('Henry Lopez', 2004),      -- Student 8
('Isabella Martinez', 2006); -- Student 9

-- Insert 27 grade records (3 per student)
INSERT INTO grades (student_id, subject, grade) VALUES
-- Alice Johnson's grades (Student 1)
(1, 'Math', 88),
(1, 'English', 92),
(1, 'Science', 85),

-- Brian Smith's grades (Student 2)
(2, 'Math', 75),
(2, 'History', 83),
(2, 'English', 79),

-- Carla Reyes's grades (Student 3)
(3, 'Science', 95),
(3, 'Math', 91),
(3, 'Art', 89),

-- Daniel Kim's grades (Student 4)
(4, 'Math', 84),
(4, 'Science', 88),
(4, 'Physical Education', 93),

-- Eva Thompson's grades (Student 5)
(5, 'English', 90),
(5, 'History', 85),
(5, 'Math', 88),

-- Felix Nguyen's grades (Student 6)
(6, 'Science', 72),
(6, 'Math', 78),
(6, 'English', 81),

-- Grace Patel's grades (Student 7)
(7, 'Art', 94),
(7, 'Science', 87),
(7, 'Math', 90),

-- Henry Lopez's grades (Student 8)
(8, 'History', 77),
(8, 'Math', 83),
(8, 'Science', 80),

-- Isabella Martinez's grades (Student 9)
(9, 'English', 96),
(9, 'Math', 89),
(9, 'Art', 92);

-- ======================================================
-- PART 3: INDEXES FOR PERFORMANCE OPTIMIZATION
-- ======================================================

-- Index for searching students by name (speeds up WHERE clauses)
CREATE INDEX idx_students_name ON students(full_name);

-- Index for filtering students by birth year
CREATE INDEX idx_students_birth_year ON students(birth_year);

-- Index for joining grades with students (speeds up JOIN operations)
CREATE INDEX idx_grades_student_id ON grades(student_id);

-- Index for grouping and filtering by subject
CREATE INDEX idx_grades_subject ON grades(subject);

-- ======================================================
-- PART 4: ASSIGNMENT QUERIES
-- ======================================================

-- Query 3: Find all grades for a specific student (Alice Johnson)
-- Purpose: Retrieve complete academic record for a single student
SELECT s.full_name, g.subject, g.grade
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE s.full_name = 'Alice Johnson'
ORDER BY g.subject;

-- Query 4: Calculate the average grade per student
-- Purpose: Determine each student's overall academic performance
SELECT
    s.full_name,
    ROUND(AVG(g.grade), 2) as average_grade,
    COUNT(g.id) as number_of_grades
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.id, s.full_name
ORDER BY average_grade DESC;

-- Query 5: List all students born after 2004
-- Purpose: Filter students based on birth year criteria
SELECT
    full_name,
    birth_year
FROM students
WHERE birth_year > 2004
ORDER BY birth_year DESC, full_name;

-- Query 6: Create a query that lists all subjects and their average grades
-- Purpose: Analyze subject difficulty based on average scores
SELECT
    subject,
    ROUND(AVG(grade), 2) as average_grade,
    COUNT(*) as number_of_students,
    MIN(grade) as lowest_grade,
    MAX(grade) as highest_grade
FROM grades
GROUP BY subject
ORDER BY average_grade DESC;

-- Query 7: Find the top 3 students with the highest average grades
-- Purpose: Identify top performers in the class
SELECT
    s.full_name,
    ROUND(AVG(g.grade), 2) as average_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.id, s.full_name
ORDER BY average_grade DESC
LIMIT 3;

-- Query 8: Show all students who have scored below 80 in any subject
-- Purpose: Identify students who may need academic support
SELECT DISTINCT
    s.full_name,
    g.subject,
    g.grade
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE g.grade < 80
ORDER BY g.grade, s.full_name;

