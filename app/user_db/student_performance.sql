-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- Create the Students table
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_of_birth DATE NOT NULL,
    gender TEXT CHECK (gender IN ('Male', 'Female')),
    email TEXT UNIQUE NOT NULL,
    phone_number TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    registration_date DATE NOT NULL
);

-- Create the Courses table
CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY,
    course_name TEXT NOT NULL,
    course_code TEXT UNIQUE NOT NULL,
    department TEXT NOT NULL,
    credits INTEGER NOT NULL,
    semester TEXT NOT NULL,
    instructor TEXT,
    syllabus TEXT,
    max_enrollment INTEGER,
    current_enrollment INTEGER,
    start_date DATE,
    end_date DATE
);

-- Create the Enrollments table
CREATE TABLE enrollments (
    enrollment_id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    enrollment_date DATE NOT NULL,
    status TEXT CHECK (status IN ('Active', 'Completedls', 'Dropped')),
    grade TEXT CHECK (grade IN ('A', 'B', 'C', 'D', 'F', NULL)),
    feedback TEXT,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- Create the Exams table
CREATE TABLE exams (
    exam_id INTEGER PRIMARY KEY,
    course_id INTEGER NOT NULL,
    exam_name TEXT NOT NULL,
    exam_date DATE NOT NULL,
    max_score INTEGER NOT NULL,
    average_score REAL,
    exam_location TEXT,
    duration_minutes INTEGER,
    type TEXT CHECK (type IN ('Midterm', 'Final', 'Quiz')),
    remarks TEXT,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- Create the Exam Results table
CREATE TABLE exam_results (
    result_id INTEGER PRIMARY KEY,
    exam_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    grade TEXT CHECK (grade IN ('A', 'B', 'C', 'D', 'F')),
    comments TEXT,
    FOREIGN KEY (exam_id) REFERENCES exams(exam_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

-- Create the Assignments table
CREATE TABLE assignments (
    assignment_id INTEGER PRIMARY KEY,
    course_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    due_date DATE NOT NULL,
    max_score INTEGER NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- Create the Submissions table
CREATE TABLE submissions (
    submission_id INTEGER PRIMARY KEY,
    assignment_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    submission_date DATE NOT NULL,
    score INTEGER,
    feedback TEXT,
    FOREIGN KEY (assignment_id) REFERENCES assignments(assignment_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

-- Create the Teachers table
CREATE TABLE teachers (
    teacher_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    department TEXT NOT NULL,
    hire_date DATE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone_number TEXT,
    address TEXT,
    salary REAL NOT NULL,
    expertise TEXT,
    supervisor_id INTEGER,
    FOREIGN KEY (supervisor_id) REFERENCES teachers(teacher_id)
);

-- Create the Attendance table
CREATE TABLE attendance (
    attendance_id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    date DATE NOT NULL,
    status TEXT CHECK (status IN ('Present', 'Absent', 'Late', 'Excused')),
    remarks TEXT,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- Create the Departments table
CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY,
    department_name TEXT NOT NULL,
    head_of_department INTEGER,
    contact_email TEXT,
    FOREIGN KEY (head_of_department) REFERENCES teachers(teacher_id)
);

-- Create the Clubs table
CREATE TABLE clubs (
    club_id INTEGER PRIMARY KEY,
    club_name TEXT NOT NULL,
    description TEXT,
    president_id INTEGER,
    meeting_schedule TEXT,
    FOREIGN KEY (president_id) REFERENCES students(student_id)
);

-- Create the Club Memberships table
CREATE TABLE club_memberships (
    membership_id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    club_id INTEGER NOT NULL,
    join_date DATE NOT NULL,
    role TEXT CHECK (role IN ('Member', 'President', 'Vice President', 'Secretary')),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (club_id) REFERENCES clubs(club_id)
);

-- Create the Libraries table
CREATE TABLE libraries (
    library_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    librarian_id INTEGER,
    FOREIGN KEY (librarian_id) REFERENCES teachers(teacher_id)
);

-- Create the Borrow Records table
CREATE TABLE borrow_records (
    borrow_id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    library_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    borrow_date DATE NOT NULL,
    return_date DATE,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (library_id) REFERENCES libraries(library_id)
);

-- Create a Books table
CREATE TABLE books (
    book_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    library_id INTEGER NOT NULL,
    author TEXT NOT NULL,
    genre TEXT,
    published_year INTEGER,
    isbn TEXT UNIQUE NOT NULL,
    FOREIGN KEY (library_id) REFERENCES libraries(library_id)
);
