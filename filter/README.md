# Filter

The program is currently set up to be compiled on Linux with the clang-12 compiler (see Makefile). I'm currently in the process of trying to make it accessible for Windows users as well.

This program takes an input .bmp image, applies a filter to it, then generates an output .bmp version of the image with the filter applied.

Steps to run the program:

1) Navigate to the program's directory in the terminal.

2) Ensure clang-12 is installed on your Linux system, then run: **make filter**

3a) Run the following command: **./filter -[FILTER] images/[IMAGE].bmp [OUTPUT_FILENAME].bmp**

3b) Example: **./filter -g images/yard.bmp out.bmp

3c) The following filters are available: grayscale (-g), sepia (-s), reflect (-r) and blur (-b)
