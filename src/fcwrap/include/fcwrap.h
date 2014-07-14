/*
 * FCWrap - Fortran to C Wrapper
 * Header file for fcwrap library
 */

char fcwrap_lib_path[80] = "./fcwrap.so";
void *fcwrap;
void *(*fortify_c_array_int_)(int *cptr_to_array, int *n_elements, void *array);
void *(*fortify_c_array_float_)(float *cptr_to_array, int *n_elements, void *array);
void *(*fortify_c_array_double_)(double *cptr_to_array, int *n_elements, void *array);
