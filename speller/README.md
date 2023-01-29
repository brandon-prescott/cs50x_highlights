# Speller

The program is currently set up to be compiled on Linux with the clang-12 compiler (see Makefile). I'm currently in the process of trying to make it accessible for Windows users as well.

This program takes two input .txt files, one is a dictionary (defined list of words), and the other can be any file containing text such as  a book. The program first loads the dictionary into memory in a hash table structure using a custom hashing function, then checks each word in the second text file against the hash table to see if it exists. If not, then the word is classed as mispelled. The program then counts the number of mispellings, and prints the run time of the program.

**Build**

Ensure clang-12 is installed on your Linux system by running
```shell
$ sudo apt install clang-12 --install-suggests
```
Navigate to the directory containing the filter program and run
```shell
$ make speller
```
**Usage**
```shell
$ ./speller DICTIONARY INFILE.txt
```
```shell
$ ./speller dictionaries/large lalaland.txt
```
The dictionary argument can be omitted and the program will default to using the large dictionary. 

