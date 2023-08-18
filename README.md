
# Mekari Code Challenge
## Salary Per Hour

### Pre-Requisite
Since the destination table will be used by BI tools, then we need to make sure that the the table exist. If it didn't, that we can make the table using query below, assuming that we use mekari database.

**employees table**
```sql
CREATE TABLE mekari.employees (
	employee_id INT NOT NULL,
	branch_id INT NOT NULL,
	salary INT NULL,
	join_date DATE NULL,
	resign_date DATE NULL
)
```

**timesheets table**
```sql
CREATE TABLE mekari.timesheets (
	timesheet_id INT NOT NULL,
	employee_id INT NULL,
	`date` DATE NULL,
	checkin TIME NULL,
	checkout TIME NULL
)
```

also the destination table

**salary_per_hour** table
```sql
CREATE TABLE mekari.salary_per_hours (
	`year` YEAR NULL,
	`month` TINYINT NULL,
	branch_id INT NULL,
	total_salary INT null,
	total_hours INT null,
	salary_per_hour INT NULL
)
```


## Tasks
### Task 1 : SQL

Lets assume that the destination table which is employees and timesheets already created and the data from csv already loaded.

To make it run by a scheduler in a daily basis, then i will make the script as a procedure.
```sql
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
```
You can also view the script from **Repository/Task 1 SQL/Stored Procedure/calculate_salary_per_hours.sql**
If we already create the procedure, then for a daily basis we can run it directly by calling the procedure
```sql
CALL CalculateSalaryPerHours()
```

But since we want to run it through scheduler, then we can use batch for this like below

```batch
@echo off

set DB_USER=root
set DB_PASSWORD=
set DB_NAME=mekari

mysql -u %DB_USER% -p%DB_PASSWORD% -D %DB_NAME% -e "CALL CalculateSalaryPerHours();"
```

You can also see the batch file in **Repository/Task 1 SQL/run.bat**

### Task 2 : Python
