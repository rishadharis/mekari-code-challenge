@echo off

set DB_USER=root
set DB_PASSWORD=
set DB_NAME=mekari

mysql -u %DB_USER% -p%DB_PASSWORD% -D %DB_NAME% -e "CALL CalculateSalaryPerHours();"