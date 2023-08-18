import pandas as pd
import mysql.connector
import argparse

def insert_to_table(host, user, password, database, df):
    # Establish the connection
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    table_name = 'salary_per_hours'

    sql = f"INSERT INTO {table_name} (year, month, branch_id, total_salary, total_hours, salary_per_hour) VALUES (%s, %s, %s, %s, %s, %s)"

    values = [tuple(row) for row in df.values]

    cursor = conn.cursor()
    cursor.executemany(sql, values)
    conn.commit()
    cursor.close()

def get_max_date_from_destination(host, user, password, database):
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = conn.cursor()

    query = "SELECT MAX(date) AS id FROM timesheets"
    cursor.execute(query)

    # Fetch the result
    result = cursor.fetchone()
    max_date = result[0]  # The maximum timesheet_id
    cursor.close()
    return max_date

def main(host, username, password, database):
    # Read File
    emp_df = pd.read_csv("employees.csv")
    ts_df = pd.read_csv("timesheets.csv")

    # Make it as datetime type
    ts_df['checkin'] = pd.to_datetime(ts_df['checkin'].fillna('09:00:00'))
    ts_df['checkout'] = pd.to_datetime(ts_df['checkout'].fillna('17:00:00'))
    ts_df['date'] = pd.to_datetime(ts_df['date'])

    # GET ONLY NEW DATA
    max_date = get_max_date_from_destination(host, username, password, database)
    ts_df = ts_df[ts_df['date'] > max_date]

    # Get hours difference
    ts_df['hours_difference'] = (ts_df['checkout'] - ts_df['checkin']).dt.total_seconds() / (60*60)

    # Add year and month column
    ts_df["year"] = ts_df['date'].dt.year
    ts_df["month"] = ts_df['date'].dt.month

    # Merge timesheet with employee
    merged_df = pd.merge(ts_df, emp_df, left_on='employee_id', right_on='employe_id', how='left')

    ### Get unique sum salary for each year, month, branch_id
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

    # Get Salary Per Hour
    final_agg_data["salary_per_hour"] = final_agg_data["salary_total"]/final_agg_data["hours_difference"]

    # print(final_agg_data)

    insert_to_table(host, username, password, database, final_agg_data)

    # To make sure this is working, we need to also insert new timesheet data (ts_df) to timesheets table
    # insert_to_timesheet_table() 
    # Not implemented yet


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Python script with command-line arguments')
    
    parser.add_argument('--host', required=False, default='localhost', help='Database host')
    parser.add_argument('--username', required=False, default='root', help='Database username')
    parser.add_argument('--password', required=False, default='', help='Database password')
    parser.add_argument('--database', required=False, default='mekari', help='Database name')
    args = parser.parse_args()

    main(args.host, args.username, args.password, args.database)