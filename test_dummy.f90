program test_dummy

  use kinds, only : r_single
  use read_dummy, only: header_list, data_list, get_header, get_data, mean_type, &
                        stddev_type, inc_mean, ret_mean, ret_mean_from_array, init_dummy, &
                        set_ndata, print_array, read_array, write_array

  type(header_list) :: head
  type(data_list)   :: dat

  type(mean_type)     :: cur_mean
  real(r_single),dimension(:),allocatable  :: cur_array, array_from_file

  character*120 :: fn

  integer i, ifn, lun, ndata_from_file

  call init_dummy ! initialize the module

  call set_ndata(15)  !just for the heck of it, increase ndata to 15

  call get_header(ifn,head) ! First, we 'read' the header 

  write(*,fmt='(A25,1X,A20)')'head%header_title=',head%header_title
  write(*,fmt='(A25,1X,I10)')'head%ndata=',head%ndata
  write(*,fmt='(A25,1X,I10)')'head%nchan=',head%nchan
  write(*,fmt='(A25,1X,F10.3)')'head%dummy=',head%dummy

  allocate(cur_array(head%ndata))

  do i=1,head%ndata          ! then we loop over the ndata from the header
    call get_data(ifn,dat)   !   and read each data point in a loop
    write(*,fmt='(A25,1X,F10.3)')'dat%obs=',dat%obs
    write(*,fmt='(A25,1X,F10.3)')'dat%error=',dat%error
    call inc_mean(dat%obs, cur_mean) ! sequentially calculate mean
    cur_array(i) = dat%obs
  enddo

  call print_array(cur_array,head%ndata)

  print *,'Mean from mean_type:           ',ret_mean(cur_mean) ! return mean from sequential calculation
  print *,'Mean from ret_mean_from_array: ',ret_mean_from_array(cur_array,head%ndata) !return mean from instantaneous array calc

  lun = 123
  fn  = 'test.output.binary'

  call write_array(lun,fn,cur_array,head%ndata)            ! write array to 'self-describing' binary file (first element ndata, second element array(ndata) )
  call read_array(lun,fn,array_from_file,ndata_from_array) ! read array from 'self-describing' binary file

  call print_array(array_from_file,ndata_from_array)

end program test_dummy
