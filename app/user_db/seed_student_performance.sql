-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- Generate submissions data
WITH generate_submissions AS (
    SELECT 1 AS submission_id, 1 AS assignment_id, 1 AS student_id, '2024-09-08' AS submission_date, 
           90 AS score, 'Well done!' AS feedback
    UNION ALL
    SELECT 2, 1, 2, '2024-09-09', 85, 'Good work'
    UNION ALL
    SELECT 3, 2, 1, '2024-09-14', 75, 'Satisfactory'
    UNION ALL
    SELECT 4, 2, 2, '2024-09-13', NULL, 'Incomplete submission'
    -- Add more submission records here
)
INSERT INTO submissions (submission_id, assignment_id, student_id, submission_date, score, feedback)
SELECT submission_id, assignment_id, student_id, submission_date, score, feedback FROM generate_submissions;
