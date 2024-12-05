-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- Insert data into Students
INSERT INTO students (first_name, last_name, date_of_birth, gender, email, phone_number, address, city, state, zip_code, registration_date)
SELECT 
    'Student'||i,
    'Last'||i,
    date('2000-01-01', '+'||(i%365)||' days'),
    CASE WHEN i%2 = 0 THEN 'Male' ELSE 'Female' END,
    'student'||i||'@example.com',
    '123456789'||i,
    'Address '||i,
    'City'||i%10,
    'State'||i%5,
    'ZIP'||(10000+i%5000),
    date('2022-01-01', '-'||(i%365)||' days')
FROM generate_series(1, 200) s(i);

-- Insert data into Courses
INSERT INTO courses (course_name, course_code, department, credits, semester, instructor, syllabus, max_enrollment, current_enrollment, start_date, end_date)
SELECT 
    'Course'||i, 
    'C'||(1000+i), 
    CASE WHEN i%3 = 0 THEN 'Science' WHEN i%3 = 1 THEN 'Arts' ELSE 'Commerce' END,
    (i%5)+1, 
    CASE WHEN i%2 = 0 THEN 'Fall' ELSE 'Spring' END,
    'Instructor'||i, 
    'Syllabus for Course'||i, 
    50, 
    (i%50)+1,
    date('2024-01-01', '+'||i||' days'), 
    date('2024-05-01', '+'||i||' days')
FROM generate_series(1, 15) s(i);

-- Insert data into Enrollments
INSERT INTO enrollments (student_id, course_id, enrollment_date, status, grade, feedback)
SELECT 
    (i%200)+1, 
    (i%15)+1, 
    date('2024-01-01', '-'||i||' days'),
    CASE WHEN i%3 = 0 THEN 'Active' WHEN i%3 = 1 THEN 'Completed' ELSE 'Dropped' END,
    CASE WHEN i%5 = 0 THEN 'A' WHEN i%5 = 1 THEN 'B' WHEN i%5 = 2 THEN 'C' WHEN i%5 = 3 THEN 'D' ELSE 'F' END,
    'Feedback for Enrollment '||i
FROM generate_series(1, 200) s(i);

-- Insert data into Exams
INSERT INTO exams (course_id, exam_name, exam_date, max_score, average_score, exam_location, duration_minutes, type, remarks)
SELECT 
    (i%15)+1, 
    'Exam'||i, 
    date('2024-01-01', '+'||i||' days'), 
    100, 
    75.5, 
    'Room'||(i%10), 
    120, 
    CASE WHEN i%2 = 0 THEN 'Midterm' ELSE 'Final' END, 
    'Remarks for Exam '||i
FROM generate_series(1, 15) s(i);

-- Insert data into Exam Results
INSERT INTO exam_results (exam_id, student_id, score, grade, comments)
SELECT 
    (i%15)+1, 
    (i%200)+1, 
    (i%100)+1, 
    CASE WHEN i%5 = 0 THEN 'A' WHEN i%5 = 1 THEN 'B' WHEN i%5 = 2 THEN 'C' WHEN i%5 = 3 THEN 'D' ELSE 'F' END, 
    'Comment for Exam Result '||i
FROM generate_series(1, 200) s(i);

-- Insert data into Assignments
INSERT INTO assignments (course_id, title, description, due_date, max_score)
SELECT 
    (i%15)+1, 
    'Assignment'||i, 
    'Description for Assignment'||i, 
    date('2024-02-01', '+'||i||' days'), 
    100
FROM generate_series(1, 200) s(i);

-- Insert data into Submissions
INSERT INTO submissions (assignment_id, student_id, submission_date, score, feedback)
SELECT 
    (i%200)+1, 
    (i%200)+1, 
    date('2024-02-15', '-'||i||' days'), 
    (i%100)+1, 
    'Feedback for Submission '||i
FROM generate_series(1, 200) s(i);

-- Insert data into Teachers
INSERT INTO teachers (first_name, last_name, department, hire_date, email, phone_number, address, salary, expertise, supervisor_id)
SELECT 
    'Teacher'||i, 
    'Last'||i, 
    CASE WHEN i%3 = 0 THEN 'Science' WHEN i%3 = 1 THEN 'Arts' ELSE 'Commerce' END,
    date('2015-01-01', '-'||i||' days'), 
    'teacher'||i||'@example.com', 
    '987654321'||i, 
    'Address'||i, 
    50000 + (i*100), 
    CASE WHEN i%2 = 0 THEN 'Expertise A' ELSE 'Expertise B' END, 
    CASE WHEN i%10 = 0 THEN NULL ELSE (i%50)+1 END
FROM generate_series(1, 50) s(i);

-- Insert data into Attendance
INSERT INTO attendance (student_id, course_id, date, status, remarks)
SELECT 
    (i%200)+1, 
    (i%15)+1, 
    date('2024-02-10', '-'||i||' days'), 
    CASE WHEN i%4 = 0 THEN 'Present' WHEN i%4 = 1 THEN 'Absent' WHEN i%4 = 2 THEN 'Late' ELSE 'Excused' END, 
    'Remarks for Attendance '||i
FROM generate_series(1, 200) s(i);

-- Insert data into Departments
INSERT INTO departments (department_name, head_of_department, contact_email)
SELECT 
    CASE WHEN i%3 = 0 THEN 'Science' WHEN i%3 = 1 THEN 'Arts' ELSE 'Commerce' END, 
    (i%50)+1, 
    'department'||i||'@example.com'
FROM generate_series(1, 10) s(i);

-- Insert data into Clubs
INSERT INTO clubs (club_name, description, president_id, meeting_schedule)
SELECT 
    'Club'||i, 
    'Description for Club'||i, 
    (i%200)+1, 
    'Schedule for Club '||i
FROM generate_series(1, 15) s(i);

-- Insert data into Club Memberships
INSERT INTO club_memberships (student_id, club_id, join_date, role)
SELECT 
    (i%200)+1, 
    (i%15)+1, 
    date('2024-03-01', '-'||i||' days'), 
    CASE WHEN i%4 = 0 THEN 'Member' WHEN i%4 = 1 THEN 'President' WHEN i%4 = 2 THEN 'Vice President' ELSE 'Secretary' END
FROM generate_series(1, 200) s(i);

-- Insert data into Libraries
INSERT INTO libraries (name, location, librarian_id)
SELECT 
    'Library'||i, 
    'Location'||i, 
    (i%50)+1
FROM generate_series(1, 10) s(i);

-- Insert data into Books
INSERT INTO books (title, author, genre, published_year, isbn)
SELECT 
    'Book'||i, 
    'Author'||i, 
    CASE WHEN i%3 = 0 THEN 'Fiction' WHEN i%3 = 1 THEN 'Non-Fiction' ELSE 'Science' END, 
    2000 + (i%21), 
    'ISBN'||(1000000+i)
FROM generate_series(1, 200) s(i);

-- Insert data into Borrow Records
INSERT INTO borrow_records (student_id, library_id, book_id, borrow_date, return_date)
SELECT 
    (i%200)+1, 
    (i%10)+1, 
    (i%200)+1, 
    date('2024-01-01', '-'||i||' days'), 
    date('2024-02-01', '-'||i||' days')
FROM generate_series(1, 200) s(i);