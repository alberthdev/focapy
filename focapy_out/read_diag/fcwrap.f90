module fcwrap
    use, intrinsic :: iso_c_binding
    use kinds
    use read_diag
    implicit none
    public :: read_radiag_header
    public :: read_radiag_data

    contains
        subroutine read_radiag_header(ftin, npred_radiag, retrieval, header_fix, header_chan_cptr_focapy, data_name, iflag, lverbose) bind(c)
            integer(i_kind), intent(in) :: ftin
            integer(i_kind), intent(in) :: npred_radiag
            logical, intent(in) :: retrieval
            type(diag_header_fix_list), intent(out) :: header_fix
            type(C_PTR), intent(out) :: header_chan_cptr_focapy
            type(diag_data_name_list), intent(out) :: data_name
            integer(i_kind), intent(out) :: iflag
            logical, optional, intent(in) :: lverbose

            type(diag_header_chan_list), allocatable, dimension (:), target, save :: header_chan ! [write_fcwrap_wrap_ashapearr_var_prototypes] WARNING: Could not find equivalent C type for 'type(diag_header_chan_list)'! (Context: subroutine 'read_radiag_header', argument 'header_chan')

            call read_radiag_header_focapy_orig(ftin, npred_radiag, retrieval, header_fix, header_chan, data_name, iflag, lverbose)

            header_chan_cptr_focapy = c_loc(header_chan)
        end subroutine read_radiag_header

        subroutine read_radiag_data(ftin, header_fix, retrieval, data_fix, data_chan_cptr_focapy, data_extra, iflag) bind(c)
            integer(i_kind), intent(in) :: ftin
            type(diag_header_fix_list), intent(in) :: header_fix
            logical, intent(in) :: retrieval
            type(diag_data_fix_list), intent(out) :: data_fix
            type(C_PTR), intent(out) :: data_chan_cptr_focapy
            type(diag_data_extra_list), allocatable, dimension(:,:) :: data_extra
            integer(i_kind), intent(out) :: iflag

            type(diag_data_chan_list), allocatable, dimension (:), target, save :: data_chan ! [write_fcwrap_wrap_ashapearr_var_prototypes] WARNING: Could not find equivalent C type for 'type(diag_data_chan_list)'! (Context: subroutine 'read_radiag_data', argument 'data_chan')

            call read_radiag_data_focapy_orig(ftin, header_fix, retrieval, data_fix, data_chan, data_extra, iflag)

            data_chan_cptr_focapy = c_loc(data_chan)
        end subroutine read_radiag_data

end module fcwrap