CREATE PROCEDURE CalculateSalaryPerHours()
BEGIN
    -- Truncate the target table
    TRUNCATE TABLE salary_per_hours;
    
    -- Insert data into the target table based on the query
    INSERT INTO salary_per_hours (`year`, `month`, branch_id, total_salary, total_hours, salary_per_hour)
    SELECT year, month, branch_id, total_salary, total_hours, total_salary/total_hours AS salary_per_hour FROM (
        SELECT 
            YEAR(`date`) AS year,
            MONTH(`date`) AS month,
            e.branch_id,
            SUM(DISTINCT e.salary) AS total_salary,
            SUM(TIMESTAMPDIFF(MINUTE,
                CASE WHEN checkin IS NULL THEN TIME('09:00:00') ELSE checkin END,
                CASE WHEN checkout IS NULL THEN TIME('17:00:00') ELSE checkout END)/60) AS total_hours
        FROM timesheets t  
        LEFT JOIN employees e ON e.employee_id = t.employee_id 
        GROUP BY year, month, e.branch_id 
    ) a;
END;