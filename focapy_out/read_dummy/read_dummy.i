/* File: example.i */
%module read_dummy
%include "cpointer.i"
%include "carrays.i"
%include "cstring.i"

/* cpointer.i stuff */
%pointer_functions(int, intp);
%pointer_functions(float, floatp);
%pointer_functions(double, doublep);

/* carrays.i stuff */
%array_functions(int, inta);
%array_functions(float, floata);
%array_functions(double, doublea);

%{
#define SWIG_FILE_WITH_INIT
#include "read_dummy.h"
%}

%inline %{
  float **mk_floatpp(float *f) {
    float **floatpp = (float **) malloc(sizeof(float *));
    *floatpp = f;
    return floatpp;
  }
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

typedef struct mean_type_ {
    long double total;
    long double n;
} mean_type, *p_mean_type;

typedef struct stddev_type_ {
    long double n;
    long double delta;
    long double mean;
    long double M2;
} stddev_type, *p_stddev_type;

void init_dummy(void);
void set_ndata(int *INPUT);
void test_init(void);
void inc_mean(float *INPUT, mean_type *INPUT);
void get_header(int *INPUT, header_list *INPUT);
void get_data(int *INPUT, data_list *INPUT);
float ret_mean(mean_type *INPUT);

float ret_mean_from_array(float **array, int *INPUT);
void print_array(float **array, int *INPUT);
void read_array(int *INPUT, char *filename, float **array, int *INPUT);
void write_array(int *INPUT, char *filename, float *INPUT, int *INPUT);
