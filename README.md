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
