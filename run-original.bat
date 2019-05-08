@echo off
echo Run original version of tf-01.py
set start_Time=%time%
echo.
echo Start Time: %start_Time%
REM echo out the python command
echo python tf-01.py pride-and-prejudice.txt ^>original-out.txt
python tf-01.py pride-and-prejudice.txt >original-out.txt
set end_Time=%time%
echo Finish Time: %end_Time%
echo.
echo Output file original-out.txt
type original-out.txt
