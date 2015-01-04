module fcwrap
    use, intrinsic :: iso_c_binding
    use kinds
    use read_dummy
    implicit none
    
    public :: ret_mean_from_array
    public :: print_array
    public :: read_array
    public :: write_array
    
    contains
        ! float ret_mean_from_array(float **array, int *ndata)
        real(r_single) function ret_mean_from_array(array_cptr_focapy, ndata) bind(c)
            integer(i_kind),intent(in)               :: ndata
            type(C_PTR), intent(in)                  :: array_cptr_focapy
            
            real(r_single),allocatable,dimension (:),target,save :: array
            
            call C_F_POINTER (array_cptr_focapy, array, [ndata])
            
            ret_mean_from_array = ret_mean_from_array_focapy_orig(array, ndata)
        end function ret_mean_from_array
        
        ! void print_array(float **array, int *ndata)
        subroutine print_array(array_cptr_focapy, ndata) bind(c)
            integer(i_kind),intent(in)              :: ndata
            type(C_PTR), intent(in)                 :: array_cptr_focapy
            
            !real(r_single),dimension(:)             :: array
            real(r_single),allocatable,dimension (:),target,save :: array
            
            call C_F_POINTER (array_cptr_focapy, array, [ndata])
            
            call print_array_focapy_orig(array, ndata)
        end subroutine print_array
        
        ! void read_array(int *lun, char *filename, float **array, int *ndata)
        subroutine read_array(lun,filename,array,ndata) bind(c)
            integer(i_kind), intent(in)                           :: lun
            character(len=1,kind=c_char),intent(in)               :: filename
            type (c_ptr), intent(out)                             :: array
            integer(i_kind), intent(out)                          :: ndata
            
            real(c_float), allocatable, dimension (:), target, save :: array_r
            
            character(1000000),pointer                        :: filename_focapy_tmp
            character(len=:),allocatable                      :: filename_focapy
            integer                                           :: filename_focapy_len
            
            call C_F_POINTER(C_LOC(filename), filename_focapy_tmp)
            filename_focapy_len = INDEX(filename_focapy_tmp,C_NULL_CHAR) - 1
            
            allocate(character(len=filename_focapy_len) :: filename_focapy)
            filename_focapy = filename_focapy_tmp(1:filename_focapy_len)
            
            call read_array_focapy_orig(lun, filename_focapy, array_r, ndata)
            
            array = c_loc(array_r)
        end subroutine read_array
        
        subroutine write_array(lun,filename,array,ndata) bind(c)
            integer(i_kind), intent(in)                :: lun
            character(len=1,kind=c_char),intent(in)    :: filename
            real(r_single),dimension(ndata),intent(in) :: array
            integer(i_kind),intent(in)                 :: ndata 
            
            character(1000000),pointer                 :: filename_focapy_tmp
            character(len=:),allocatable               :: filename_focapy
            integer                                    :: filename_focapy_len
            
            call C_F_POINTER(C_LOC(filename),filename_focapy_tmp)
            filename_focapy_len = INDEX(filename_focapy_tmp, C_NULL_CHAR) - 1
            
            allocate(character(len=filename_focapy_len) :: filename_focapy)
            filename_focapy = filename_focapy_tmp(1:filename_focapy_len)
            
            call write_array_focapy_orig(lun, filename_focapy, array, ndata)
            
        end subroutine write_array
end module fcwrap
