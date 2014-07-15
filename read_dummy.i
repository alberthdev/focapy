/* File: example.i */
%module read_dummy

%{
#define SWIG_FILE_WITH_INIT
#include "read_dummy.h"
%}

typedef struct header_list_ {
    char header_title[20];
    int ndata;
    int nchan;
    float dummy;
} header_list, *p_header_list;
typedef struct data_list_ {
    float obs;
    float error;
} data_list, *p_data_list;

void get_header(int *INPUT, header_list *INPUT);
void get_data(int *INPUT, data_list *INPUT);
