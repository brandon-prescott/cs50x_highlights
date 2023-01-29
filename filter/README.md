# Filter

The program is currently set up to be compiled on Linux with the clang-12 compiler (see Makefile). I'm currently in the process of trying to make it accessible for Windows users as well.

This program takes an input .bmp image, applies a filter to it, then generates an output .bmp version of the image with the filter applied.

Steps to run the program:

Ensure clang-12 is installed on your Linux system by running
```shell
$ sudo apt install clang-12 --install-suggests
```

Navigate to the directory containing the filter program and run
```shell
~/filter$ make filter
```
**Usage**
```shell
~/filter$ ./filter -g INFILE.bmp OUTFILE.bmp
```

```shell
~/filter$ ./filter -s INFILE.bmp OUTFILE.bmp
```

```shell
~/filter$ ./filter -r INFILE.bmp OUTFILE.bmp
```

```shell
~/filter$ ./filter -b INFILE.bmp OUTFILE.bmp
```



The following filters are available: grayscale (-g), sepia (-s), reflect (-r) and blur (-b).
