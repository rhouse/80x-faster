#!/usr/bin/env python

# my-tf-01.py  --  A modification of tf-01.py to make it run faster

import sys, os, string

# The constrained memory should have no more than 1024 cells
data = []
# We're lucky:
# The stop words are only 556 characters and the lines are all 
# less than 80 characters, so we can use that knowledge to 
# simplify the problem: we can have the stop words loaded in 
# memory while processing one line of the input at a time.
# If these two assumptions didn't hold, the algorithm would 
# need to be changed considerably.

# Overall strategy: (PART 1) read the input file, count the 
# words, increment/store counts in secondary memory (a file) 
# (PART 2) find the 25 most frequent words in secondary memory

# PART 1: 
# - read the input file one line at a time
# - filter the characters, normalize to lower case
# - identify words, increment corresponding counts in file

# Load the list of stop words
f = open('./stop_words.txt')
data = [f.read(1024).split(',')] # data[0] holds the stop words
f.close()

data.append([])    # data[1] is line (max 80 characters)
data.append(None)  # data[2] is index of the start_char of word
data.append(0)     # data[3] is index on characters, i = 0
data.append(False) # data[4] is flag indicating if word was found
data.append('')    # data[5] is the word
data.append('')    # data[6] is word,NNNN
data.append(0)     # data[7] is frequency

# File names
words_file_name        = "the_words"
sorted_words_file_name = "the_words.srt"
temp_file_name_prefix  = "tempfile"
word_freqs_file_name   = "word_freqs"

max_records_per_temp_file = 1000

# Open the secondary memory
words_file = open(words_file_name, 'wb')

# Open the input file
f = open(sys.argv[1])
# Loop over input file's lines
num_stop_words = 0
while True:
    data[1] = [f.readline()] 
    if data[1] == ['']: # end of input file
        break
    if data[1][0][len(data[1][0])-1] != '\n': # If it does not end with \n
        data[1][0] = data[1][0] + '\n' # Add \n
    data[2] = None
    data[3] = 0 
    # Loop over characters in the line
    for c in data[1][0]: # elimination of symbol c is exercise
        if data[2] == None:
            if c.isalnum():
                # We found the start of a word
                data[2] = data[3]
        else:
            if not c.isalnum():
                # We found the end of a word. Process it
                data[4] = False 
                data[5] = data[1][0][data[2]:data[3]].lower()
                # Ignore words with len < 2, and stop words
                if len(data[5]) >= 2 and data[5] not in data[0]:
                    words_file.writelines("%s\n" % (data[5]))
                else:
                    num_stop_words += 1
                # Let's reset
                data[2] = None
        data[3] += 1
# We're done with the input file
f.close()
words_file.close()
#print "num_stop_words = ", num_stop_words
# Begin external sort of words_file

# The next two lines are a quick and easy external sort, but maybe cheating 
# a bit since we are supposed to be in the good old days of extremely limited
# resources.
#import os
#os.system('cat the_words | sort > the_words.srt')

# Read lines from the input words_file in chunks of max_records_per_temp_file,
# sort each chunk, and write to a temp file.

words_file = open(words_file_name, 'rb')

temp_file_extension = 0;

while True:
    # Read a chunk of no more than max_records_per_temp_file into data[]
    del data[:]
    num_records = 0
    while True:
        data.append(words_file.readline()) 
        if data[num_records] == '': # end of input file
            if num_records > 0:
                del data[-1]
            break
        num_records += 1
        if num_records == max_records_per_temp_file:
            break

    if num_records == 0:
        break

    # data contains a chunk of records to sort and write to a temp file

    data.sort()

    temp_file_extension += 1
    temp_file_name = temp_file_name_prefix + "." + str(temp_file_extension)
    temp_file = open(temp_file_name, 'wb')
    for i in range(num_records):
        temp_file.writelines("%s" % (data[i]))
    temp_file.close() 

words_file.close()

# Open all the temp files and read one record from each into cur_temp_record[]

temp_files = []
cur_temp_record = []
num_temp_files = temp_file_extension
#print "num_temp_files =", num_temp_files
for i in range(num_temp_files):
    temp_file_name = temp_file_name_prefix + "." + str(i+1)
    temp_files.append(open(temp_file_name, 'rb'))
    cur_temp_record.append(temp_files[i].readline()) 

# Open the sorted output file
sorted_words_file = open(sorted_words_file_name, 'wb')

# Merge the temp files into the sorted output file.
# In the real world we would use a heap data structure (priority queue) so
# that it would not be necessary to look at all elements in the 
# cur_temp_record list in order to find the smallest one.

while True:
    smallest = '~'
    j = -1
    for i in range(num_temp_files):
        if cur_temp_record[i] == '':
            continue
        if cur_temp_record[i] < smallest:
            smallest = cur_temp_record[i]
            j = i
    if j == -1:
        break
    cur_temp_record[j] = temp_files[j].readline()
    sorted_words_file.writelines("%20s" % (smallest))


sorted_words_file.close()

# Close all the temp files and remove them

for i in range(num_temp_files):
    temp_files[i].close()
    temp_file_name = temp_file_name_prefix + "." + str(i+1)
    os.remove(temp_file_name)

# End external sort:  The output file is words_file_srt

# Create the word freqency file

# Open the word freqency file
word_freqs_file = open(word_freqs_file_name, 'wb')

prev_line = ''

with open(sorted_words_file_name, 'rb') as words_file:
    for line in words_file:
        if line == prev_line:
            freq += 1
            continue
        if prev_line != '':
            word_freqs_file.writelines("%20s,%04d\n" % (prev_line.strip(), freq))
        prev_line = line
        freq = 1
    if prev_line != '':
        word_freqs_file.writelines("%20s,%04d\n" % (prev_line.strip(), freq))

words_file.close()
word_freqs_file.close()

# PART 2
# Now we need to find the 25 most frequently occuring words.
# We don't need anything from the previous values in memory
del data[:]

# Let's use the first 25 entries for the top 25 words
data = data + [[]]*(25 - len(data))
data.append('') # data[25] is word,freq from file
data.append(0)  # data[26] is freq

# Loop over secondary memory file

word_freqs = open('word_freqs', 'rb')

while True:
    data[25] = word_freqs.readline().strip()
    if data[25] == '': # EOF
        break
    data[26] = int(data[25].split(',')[1]) # Read it as integer
    data[25] = data[25].split(',')[0].strip() # word
    # Check if this word has more counts than the ones in memory
    for i in range(25): # elimination of symbol i is exercise
        if data[i] == [] or data[i][1] < data[26]:
            data.insert(i, [data[25], data[26]]) 
            del data[26] #  delete the last element
            break
            
for tf in data[0:25]: # elimination of symbol tf is exercise
    if len(tf) == 2:
        print tf[0], ' - ', tf[1]
# We're done
word_freqs.close()

# Get rid of various working files
os.remove(words_file_name)
os.remove(sorted_words_file_name)
os.remove(word_freqs_file_name)

# end my-tf-01.py
