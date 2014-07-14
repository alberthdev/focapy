from read_dummy import *
import read_dummy

init_c_modules()

head = header_list()
dat  = data_list()

cur_mean = mean_type();

cur_array = new_floata(1000)
array_from_file = new_floata(1000)

# Only exception here!
#fn = new_chara(120)

i = lun = ndata_from_file = 0
ndata_from_file = new_intp()

ifn = new_intp()
intp_assign(ifn, 0)

cst = 15;

init_dummy_() 
set_ndata_(cst) 
get_header_(ifn, head)   # First, we 'read' the header 

print("%25s %20s"   % ("head->header_title=", head.header_title))
print("%25s %10i"   % ("head->ndata=", head.ndata))
print("%25s %10i"   % ("head->nchan=", head.nchan))
print("%25s %10.3f" % ("head->dummy=", head.dummy))

cur_array = new_floata(head.ndata);

for i in xrange(1, head.ndata + 1): # then we loop over the ndata from the header
    get_data_(ifn, dat)     #   and read each data point in a loop
    print("%25s %10.3f" % ("dat%obs=", dat.obs))
    print("%25s %10.3f" % ("dat%error=", dat.error))
    inc_mean_(dat.obs, cur_mean)
    floata_setitem(cur_array, i-1, dat.obs)

print_array_(cur_array, head.ndata);

print(" Mean from mean_type:           %.6f" % ret_mean_(cur_mean))   # return mean from sequential calculation
print(" Mean from ret_mean_from_array: %.6f" % ret_mean_from_array_(cur_array,head.ndata))   #return mean from instantaneous array calc

lun = 123;
fn = "test.output.binary"

write_array_(lun,fn,cur_array,head.ndata)               # write array to 'self-describing' binary file (first element ndata, second element array(ndata) )
read_array_(lun,fn,array_from_file,ndata_from_file)   # read array from 'self-describing' binary file
#print intp_value(ndata_from_file)
print_array_(array_from_file,ndata_from_file);
