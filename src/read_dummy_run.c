#include <stdlib.h>
#include <stdio.h>
#include <stdarg.h>
#include <dlfcn.h>
#include "read_dummy.h"

int main() {
    init_c_modules();
    
    header_list *head;
    data_list *dat;
             
    mean_type *cur_mean;
    float *cur_array, *array_from_file = NULL;
    
    head      = (header_list *) malloc(sizeof(header_list));
    dat       = (data_list *)   malloc(sizeof(data_list));
    cur_mean  = (mean_type *)   malloc(sizeof(mean_type));
    
    char fn[120] = "test.output.binary";
    
    int i, ifn, lun, ndata_from_file;
    
    init_dummy();
    
    int ndata = 15;
    
    set_ndata(&ndata);  //just for the heck of it, increase ndata to 15
    
    get_header(&ifn,head); // First, we 'read' the header 
    
    printf("%25s %20s\n", "head%header_title=",head->header_title);
    printf("%25s %10i\n", "head%ndata=",head->ndata);
    printf("%25s %10i\n", "head%nchan=",head->nchan);
    printf("%25s %10.3f\n", "head%dummy=",head->dummy);
    
    cur_array = (float *) malloc(sizeof(float) * (head->ndata));
    
    for(i=1; i <= head->ndata; i++) {          // then we loop over the ndata from the header
        get_data(&ifn,dat);   //   and read each data point in a loop
        printf("%25s %10.3f\n", "dat%obs=",dat->obs);
        printf("%25s %10.3f\n", "dat%error=",dat->error);
        inc_mean(&(dat->obs), cur_mean); // sequentially calculate mean
        cur_array[i-1] = dat->obs;
    }
    
    //void *cur_array_fortran;
    
    //fortify_c_array_float(&cur_array, &(head->ndata), &cur_array_fortran);
    print_array_fw(&cur_array,&(head->ndata));
    
    //print_array_(&cur_array,&(head->ndata));
    
    printf(" Mean from mean_type:            %10.6f\n",ret_mean(cur_mean)); // return mean from sequential calculation
    printf(" Mean from ret_mean_from_array:  %10.6f\n",ret_mean_from_array_fw(&cur_array,&(head->ndata))); //return mean from instantaneous array calc
    
    lun = 123;
    
    write_array(&lun,fn,cur_array,&(head->ndata));           // write array to 'self-describing' binary file (first element ndata, second element array(ndata) )
    
    //void *array_from_file_fortran;
    //fortify_c_array_float(&array_from_file, &(head->ndata), &array_from_file_fortran);
    
    lun = 234;
    
    read_array_fw(&lun,fn,&array_from_file,&ndata_from_file); // read array from 'self-describing' binary file
    
    print_array_fw(&array_from_file,&ndata_from_file);
}
