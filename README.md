             How to Make a Program Run 80 Times Faster

A particular Python program is made to run 80 times faster by a change in
algorithm which avoids excessive hits on the harddrive.  For a description
of the original program and how it was changed click 
<a href="http://rogerfhouse.com/programming/80-times/index.html">here</a>.

NOTE:  The programs are Python 2.7, not Python 3.

The following file structure is used:

    tf-01.py                    The original program(*)
    my-tf-01.py                 The new modified version of the program
    pride-and-prejudice.txt     The main input text file to process
    stop_words.txt              A file of words to be skipped
    run-original                Linux script to run the original program
    run-new                     Linux script to run the new program
    LICENSE                     An MIT license
    README.md                   The file you are now reading
    run-original.bar            Windows script to run the original program
    run-new.bat                 Windows script to run the new program

(*) One small change has been made to the original program:  The stop words
file is read from the current directory, not the parent of the current
directory


On a GNU/Linux platform

Run the original program (THIS CAN TAKE A WHILE)

    ./run-original

The output file is original-out.txt.  Add the user time and sys time to get
the total time for the run, original_time.

Run the new program

    ./run-new

The output file is new-out.txt.  Add the user time and sys time to get
the total time for the run, new_time.

Make sure the two programs produce the same output:

    diff original-out.txt new-out.txt

Divide original_time by new_time to get a number around 80, showing that 
the new program runs about 80 times faster than the original one.


On a Windows platform

Run the original program (THIS CAN TAKE A WHILE)

    run-original.bat

The output file is original-out.txt.  Subtract the finish time from the
start time to get the total time for the run, original_time.

Run the new program

    run-new.bat

The output file is new-out.txt.  Subtract the finish time from the
start time to get the total time for the run, new_time.

Make sure the two programs produce the same output:

    comp original-out.txt new-out.txt

Divide original_time by new_time to get a number around 80, showing that 
the new program runs about 80 times faster than the original one.


Thanks to Steve Bursch for his QA work, and, especially, for getting it 
all to work on Windows.
