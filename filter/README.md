# Filter

The program is currently set up to be compiled on Linux with the clang-12 compiler (see Makefile). I'm currently in the process of trying to make it accessible for Windows users as well.

This program takes an input .bmp image, applies a filter to it, then generates an output .bmp version of the image with the filter applied.

**Build**

Ensure clang-12 is installed on your Linux system by running
```shell
$ sudo apt install clang-12 --install-suggests
```
Navigate to the directory containing the filter program and run
```shell
$ make filter
```
**Usage**
```shell
$ ./filter -FILTER INFILE.bmp OUTFILE.bmp
```
```shell
$ ./filter -g images/yard.bmp yard_g.bmp
```
The following filters are available: grayscale (-g), sepia (-s), reflect (-r) and blur (-b).
