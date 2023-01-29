# Filter

The program is currently set up to be compiled on Linux with the clang-12 compiler (see Makefile). I'm currently in the process of trying to make it accessible for Windows users as well.

This program takes an input .bmp image, applies a filter to it, then generates an output .bmp version of the image with the filter applied.

Steps to run the program:

(1) Ensure clang-12 is installed on your Linux system by running
```shell
$ sudo apt install clang-12 --install-suggests
```

(2) Navigate to the directory containing the filter program and run
```shell
~/filter$ make filter
```

(3a) Run the following command: **./filter -[FILTER] images/[INFILE].bmp [OUTFILE].bmp**

(3b) Example: **./filter -g images/yard.bmp out.bmp**

(3c) The following filters are available: grayscale (-g), sepia (-s), reflect (-r) and blur (-b).
