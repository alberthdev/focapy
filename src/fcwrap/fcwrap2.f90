module fcwrap
    use, intrinsic :: iso_c_binding
    use kinds
    use read_dummy
    implicit none
    
    public :: ret_mean_from_array_fw
    public :: print_array_fw
    public :: read_array_fw
    
    contains
        ! float ret_mean_from_array_fw(float **array, int *ndata)
        real(r_single) function ret_mean_from_array_fw(cptr_to_array, ndata) bind(c)
            integer(i_kind),intent(in)               :: ndata
            type(C_PTR), intent(in)                  :: cptr_to_array
            
            real(r_single),allocatable,dimension (:),target,save :: array
            
            call C_F_POINTER (cptr_to_array, array, [ndata])
            
            ret_mean_from_array_fw = ret_mean_from_array(array, ndata)
        end function ret_mean_from_array_fw
        
        ! void print_array_fw(float **array, int *ndata)
        subroutine print_array_fw(cptr_to_array, ndata) bind(c)
            integer(i_kind),intent(in)              :: ndata
            type(C_PTR), intent(in)                 :: cptr_to_array
            
            !real(r_single),dimension(:)             :: array
            real(r_single),allocatable,dimension (:),target,save :: array
            
            call C_F_POINTER (cptr_to_array, array, [ndata])
            
            call print_array(array, ndata)
        end subroutine print_array_fw
        
        ! void read_array_fw(int *lun, char *filename, float **array, int *ndata)
        subroutine read_array_fw(lun,filename,array,ndata) bind(c)
            integer(i_kind), intent(in)                           :: lun
            character, dimension(120),intent(in)                  :: filename
            type (c_ptr), intent(out)                             :: array
            integer(i_kind), intent(out)                          :: ndata
            
            real(c_float), allocatable, dimension (:), target, save :: array_r
            
            call read_array(lun, filename, array_r, ndata)
            
            array = c_loc(array_r)
        end subroutine read_array_fw
        
        !subroutine read_array_fw(lun,filename,array,ndata)
        !    integer(i_kind), intent(in)                           :: lun
        !    character, dimension(120),intent(in)                  :: filename
        !    real(r_single),dimension(:),intent(inout),allocatable :: array
        !    integer(i_kind), intent(out)                          :: ndata
        !
        !    open(lun,file=filename,form='unformatted')
        !    read(lun) ndata
        !    print *,'Reading array of length=',ndata
        !    allocate(array(ndata))
        !
        !    read(lun) array
        !    close(lun)
        !end subroutine read_array_fw
end module fcwrap
