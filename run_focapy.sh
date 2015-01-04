#!/bin/bash

becho() {
    echo -e "\033[1m""$@""\033[0m"
}

becho "** Removing old generated files..."
rm -r focapy_out/test

becho "** Recreating output directory..."
mkdir focapy_out/test

becho "** Generating Python wrapper..."
python ./render.py

becho "** Filling in the blanks..."

REMOVE_KEYS="extern int \*linit;
extern int \*ndata;
extern int \*data_ct;"

OLDIFS="$IFS"
IFS=$'\n'

for KEY in $REMOVE_KEYS; do
    becho " * Patching away line '$KEY' from C/SWIG include files..."
    cat focapy_out/test/read_dummy.h | sed '/'"$KEY"'/d' > focapy_out/test/read_dummy-tmp123.h
    cat focapy_out/test/read_dummy.i | sed '/'"$KEY"'/d' > focapy_out/test/read_dummy-tmp123.i
    mv focapy_out/test/read_dummy-tmp123.h focapy_out/test/read_dummy.h
    mv focapy_out/test/read_dummy-tmp123.i focapy_out/test/read_dummy.i
done

IFS="$OLDIFS"

declare -a FIX_LINES_ORIGINAL=("void inc_mean(float \*ob, mean_type \*mean);" \
"void print_array(float \*\*array, int \*ndata);" \
"void write_array(int \*lun, char \*filename, float \*array, int \*ndata);" \
"void read_array(int \*lun, char \*filename, float \*\*array, int \*ndata);" \
"float ret_mean_from_array(float \*\*array, int \*ndata);")

declare -a FIX_LINES=("void inc_mean(float *INPUT, mean_type *mean);" \
"void print_array(float **array, int *INPUT);" \
"void write_array(int *INPUT, char *filename, float *array, int *INPUT);" \
"void read_array(int *INPUT, char *filename, float **array, int *INPUT);" \
"float ret_mean_from_array(float **array, int *INPUT);")

alength=${#FIX_LINES_ORIGINAL[@]}

# use for loop read all values and indexes
for (( i=1; i<${alength}+1; i++ ));
do
    becho " * Fixing line '${FIX_LINES_ORIGINAL[$i-1]}' to use INPUT (SWIG include file)..."
    #echo 's/'"${FIX_LINES_ORIGINAL[$i-1]}"'/'"${FIX_LINES[$i-1]}"'/'
    cat focapy_out/test/read_dummy.i | sed 's/'"${FIX_LINES_ORIGINAL[$i-1]}"'/'"${FIX_LINES[$i-1]}"'/' > focapy_out/test/read_dummy-tmp123.i
    mv focapy_out/test/read_dummy-tmp123.i focapy_out/test/read_dummy.i
done

becho " * Copying Makefile..."
cp focapy_out/read_dummy/Makefile focapy_out/test
becho " * Copying C test code..."
cp -r focapy_out/read_dummy/src focapy_out/test
becho " * Copying Python test code..."
cp -r focapy_out/read_dummy/test focapy_out/test
becho " * Copying required kinds.F90 source file..."
cp kinds.F90 focapy_out/test
becho " * Copying Fortran test code test_dummy.f90..."
cp focapy_out/read_dummy/test_dummy.f90 focapy_out/test

becho '** Done! Go to focapy_out/test and run `make help` for build targets.'
