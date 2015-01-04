focapy - Combinational Wrapper Branch
======================================
FoCaPy - Fortran to C and Python - **Combinational Wrapper Branch**

**NOT READY FOR ANY USE, PRODUCTION OR TESTING.** This repo was created for storing work - it is NOT ready for any use yet!

## Introduction
**FoCaPy**, short for Fortran tO C And PYthon, is a tool to allow C and Python programs to interface with native Fortran code.

The **Combinational Wrapper** branch is a branch that compiles everything (including the original Fortran code) into one
binary, as well as adding additional Fortran wrapper code to make things work.

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

If you wish to look inside FoCaPy, take a look at the script, and follow from there!
