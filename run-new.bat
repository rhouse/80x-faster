@echo off
echo Run new version of tf-01.py
set start_Time=%time%
echo.
echo Start Time: %start_Time%
REM echo out the python command
echo python my-tf-01.py pride-and-prejudice.txt ^>new-out.txt
python my-tf-01.py pride-and-prejudice.txt >new-out.txt
set end_Time=%time%
echo Finish Time: %end_Time%
echo.
echo Output file new-out.txt
type new-out.txt
