#include <stdint.h>

int *data_ct;
int *ndata;
int *linit;

#pragma pack(2)

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

#pragma pack()

void init_dummy(void);
void set_ndata(int *nd);
void test_init(void);
void inc_mean(float *ob, mean_type *mean);
void get_header(int *inlun, header_list *head);
void get_data(int *inlun, data_list *dat);
float ret_mean(mean_type *mean);

float ret_mean_from_array(float **array, int *ndata);
void print_array(float **array, int *ndata);
void read_array(int *lun, char *filename, float **array, int *ndata);
void write_array(int *lun, char *filename, float *array, int *ndata);
