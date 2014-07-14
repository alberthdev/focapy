#include <stdlib.h>
#include <stdio.h>
#include <stdarg.h>
#include <dlfcn.h>
#include "%MODNAME%.h"
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

char mod_lib_path[80] = "./%MODNAME%_.so";
char *err_str;

void *%MODNAME%;

void init_c_modules() {
