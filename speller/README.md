# Speller

The program is currently set up to be compiled on Linux with the clang-12 compiler (see Makefile). I'm currently in the process of trying to make it accessible for Windows users as well.

This program takes two input .txt files, one is a dictionary (defined list of words), and the other can be any file containing text such as  a book. The program first loads the dictionary into memory in a hash table structure using a custom hashing function, then checks each word in the second text file against the hash table to see if it exists. If not, then the word is classed as mispelled. The program then counts the number of mispellings, and prints the run time of the program.

Steps to run the program:

(1) Navigate to the program's directory in the terminal.

(2) Ensure clang-12 is installed on your Linux system, then run: **make speller**

(3a) Run the following command: **./speller [DICTIONARY] texts/[TEXT].txt**

(3b) Example: ./speller dictionaries/large texts/lalaland.txt**

(3c) Note: The dictionaries argument can be omitted and it will default to the large dictionary (the small one was for testing during development)
