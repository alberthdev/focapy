module fcwrap
    use, intrinsic :: iso_c_binding
    use kinds
    use read_dummy
    implicit none
    public :: print_array
    public :: write_array
    public :: read_array
    public :: ret_mean_from_array

    contains
        subroutine print_array(array_cptr_focapy, ndata) bind(c)
            type(C_PTR), intent(in) :: array_cptr_focapy
            integer(i_kind), intent(in) :: ndata

            real(r_single), allocatable, dimension (:), target, save :: array

            call C_F_POINTER (array_cptr_focapy, array, [ndata])

            call print_array_focapy_orig(array, ndata)
        end subroutine print_array

        subroutine write_array(lun, filename, array, ndata) bind(c)
            integer(i_kind), intent(in) :: lun
            character(len=1,kind=c_char), intent(in) :: filename
            real(r_single), dimension(ndata), intent(in) :: array
            integer(i_kind), intent(in) :: ndata

            character(len=:),allocatable   :: filename_focapy
            character(len=1000000),pointer :: filename_focapy_tmp
            integer                        :: filename_focapy_len

            call C_F_POINTER(C_LOC(filename), filename_focapy_tmp)
            filename_focapy_len = INDEX(filename_focapy_tmp, C_NULL_CHAR) - 1
            allocate(character(len=filename_focapy_len) :: filename_focapy)
            filename_focapy = filename_focapy_tmp(1:filename_focapy_len)

            call write_array_focapy_orig(lun, filename_focapy, array, ndata)
        end subroutine write_array

        subroutine read_array(lun, filename, array_cptr_focapy, ndata) bind(c)
            integer(i_kind), intent(in) :: lun
            character(len=1,kind=c_char), intent(in) :: filename
            type(C_PTR), intent(inout) :: array_cptr_focapy
            integer(i_kind), intent(out) :: ndata

            real(c_float), allocatable, dimension (:), target, save :: array

            character(len=:),allocatable   :: filename_focapy
            character(len=1000000),pointer :: filename_focapy_tmp
            integer                        :: filename_focapy_len

            call C_F_POINTER(C_LOC(filename), filename_focapy_tmp)
            filename_focapy_len = INDEX(filename_focapy_tmp, C_NULL_CHAR) - 1
            allocate(character(len=filename_focapy_len) :: filename_focapy)
            filename_focapy = filename_focapy_tmp(1:filename_focapy_len)

            call read_array_focapy_orig(lun, filename_focapy, array, ndata)

            array_cptr_focapy = c_loc(array)
        end subroutine read_array


        real(r_single) function ret_mean_from_array(array_cptr_focapy, ndata) bind(c)
            type(C_PTR), intent(in) :: array_cptr_focapy
            integer(i_kind), intent(in) :: ndata

            real(r_single), allocatable, dimension (:), target, save :: array

            call C_F_POINTER (array_cptr_focapy, array, [ndata])

            ret_mean_from_array = ret_mean_from_array_focapy_orig(array, ndata)
        end function ret_mean_from_array
end module fcwrap