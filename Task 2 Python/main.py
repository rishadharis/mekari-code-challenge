import pandas as pd

emp_df = pd.read_csv("employees.csv")

ts_df = pd.read_csv("timesheets.csv")

ts_df['checkin'] = pd.to_datetime(ts_df['checkin'].fillna('09:00:00'))
ts_df['checkout'] = pd.to_datetime(ts_df['checkout'].fillna('17:00:00'))
ts_df['date'] = pd.to_datetime(ts_df['date'])

ts_df['hours_difference'] = (ts_df['checkout'] - ts_df['checkin']).dt.total_seconds() / (60*60)

ts_df["year"] = ts_df['date'].dt.year
ts_df["month"] = ts_df['date'].dt.month
merged_df = pd.merge(ts_df, emp_df, left_on='employee_id', right_on='employe_id', how='left')

agg_data = merged_df.groupby(['year', 'month', 'branch_id', 'employee_id']).agg({
    'salary': 'first',            # Get the first salary (assuming salaries are the same for the same employee)
    'hours_difference': 'sum'          # Sum of hour_worked
}).reset_index()

agg_data = merged_df.groupby(['year', 'month', 'branch_id', 'employee_id']).agg({
    'salary': 'first',            # Get the first salary (assuming salaries are the same for the same employee)
    'hours_difference': 'sum'          # Sum of hour_worked
}).reset_index()

# Group by year, month, and branch_id again to calculate the sum of salaries and total hour worked
final_agg_data = agg_data.groupby(['year', 'month', 'branch_id']).agg({
    'salary': 'sum',               # Sum of unique salaries
    'hours_difference': 'sum'           # Sum of hour_worked
}).reset_index()

final_agg_data.rename(columns={'salary': 'salary_total'}, inplace=True)

final_agg_data["salary_per_hour"] = final_agg_data["salary_total"]/final_agg_data["hours_difference"]

print(final_agg_data)

