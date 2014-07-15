#include <stdlib.h>
#include <stdio.h>
#include <stdarg.h>
#include <dlfcn.h>
#include "read_dummy.h"
#include "fcwrap.h"

void fatal( const char* format, ... ) {
    va_list args;
    fprintf( stderr, "Error: " );
    va_start( args, format );
    vfprintf( stderr, format, args );
    va_end( args );
    fprintf( stderr, "\n" );
    exit(1);
}

char mod_lib_path[80] = "./read_dummy_.so";
char *err_str;

void *read_dummy;

void init_c_modules() {
    
    printf(" * COMBINATIONAL WRAPPER METHOD\n");
    printf("***********************************************************\n");
    printf("* Actual Fortran code execution begins below...           *\n");
    printf("***********************************************************\n");
}
