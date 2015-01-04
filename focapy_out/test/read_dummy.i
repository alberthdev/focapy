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

%inline %{
  int **mk_intpp(int *f) {
    int **intpp = (int **) malloc(sizeof(int *));
    *intpp = f;
    return intpp;
  }
%}
/* Top-level element variable declarations */
extern int *data_ct;
extern int *ndata;
extern int *linit;

/* Derived type structures */
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



/* Subroutine prototypes */
void init_dummy(void);
void set_ndata(int *nd);
void test_init(void);
void inc_mean(float *ob, mean_type *mean);
void get_header(int *inlun, header_list *head);
void get_data(int *inlun, data_list *dat);
void print_array(float **array, int *ndata);
void write_array(int *lun, char *filename, float *array, int *ndata);
void read_array(int *lun, char *filename, float **array, int *ndata);

/* Function prototypes */
float ret_mean(mean_type *mean);
float ret_mean_from_array(float **array, int *ndata);
