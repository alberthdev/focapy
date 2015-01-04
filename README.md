focapy
======

FoCaPy - Fortran to C and Python

**NOT READY FOR ANY USE, PRODUCTION OR TESTING.** This repo was created for storing work - it is NOT ready for any use yet!

## Introduction
**FoCaPy**, short for Fortran tO C And PYthon, is a tool to allow C and Python programs to interface with native Fortran code.

## Download
**FoCaPy** is extremely unstable (especially in the Git repo), so you should get a prepared release archive from here:

https://github.com/alberthdev/focapy/releases

## Testing
If you wish to test Focapy, download a release archive, extract, and run the following:

    ./run_focapy.sh
    cd focapy_out/test
    make
    # Original Fortran test program
    ./test_dummy.x
    # C test program (using Focapy C headers)
    ./read_dummy
    # Python test program (using Focapy C headers + SWIG include)
    python test/read_dummy_run.py
