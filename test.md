To retrieve the top 5 scoring students from the 1st quarter of 2024 (which consists of January, February, and March), you need to join the `exam_results` and `students` tables. You may also need to filter the results based on the exam dates. Here's an SQL query that does this:

```sql
SELECT 
    s.student_id,
    s.first_name,
    s.last_name,
    SUM(er.score) AS total_score
FROM 
    exam_results er
JOIN 
    students s ON er.student_id = s.student_id
JOIN 
    exams e ON er.exam_id = e.exam_id
WHERE 
    e.exam_date BETWEEN '2024-01-01' AND '2024-03-31'
GROUP BY 
    s.student_id
ORDER BY 
    total_score DESC
LIMIT 5;
```

### Explanation:
1. **SELECT**: Selects the student's ID, first name, last name, and the total score calculated by summing up scores from exams.
2. **FROM and JOIN**: Joins the `exam_results`, `students`, and `exams` tables on the relevant keys.
3. **WHERE**: Filters results to include only those records where the exam date is between January 1, 2024, and March 31, 2024.
4. **GROUP BY**: Groups the results by student ID to aggregate scores for each student.
5. **ORDER BY**: Orders results by the total score in descending order so that the highest scores come first.
6. **LIMIT**: Limits the result to the top 5 scoring students.get top 5 scoring students from 1st quarter of 2024