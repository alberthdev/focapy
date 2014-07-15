module read_dummy
  use, intrinsic :: iso_c_binding
  use kinds, only:  i_kind,r_single,r_quad
  implicit none

! Declare public and private
  private

  public :: header_list
  public :: data_list
  public :: mean_type
  public :: stddev_type

  public :: init_dummy
  public :: set_ndata

  public :: get_header
  public :: get_data

  public :: inc_mean
  public :: ret_mean
  public :: ret_mean_from_array

  public :: print_array
  public :: write_array
  public :: read_array

  integer(i_kind)     :: data_ct = 1 ! internal counter, will increase by one every time get_data is called

  integer(i_kind)     :: ndata   = -999 

  logical             :: linit   = .false.

  type header_list                       !  This is the structure type, containing:
    character(len=20) :: header_title    ! header title/description
    integer(i_kind)   :: ndata           ! number of data
    integer(i_kind)   :: nchan           ! number of channels - not used yet
    real(r_single)    :: dummy           ! just a dummy number
  end type header_list

  type data_list                         !  This is the data structure, containing:
    real(r_single)    :: obs             ! a fake observation (increases by 1 every time it is called)
    real(r_single)    :: error           ! a fake error (just -1 * obs)
  end type data_list

  type mean_type                       !  This is a structure to calculate a running mean
    real(r_quad)    :: total           ! mean = total / n
    real(r_quad)    :: n               !  
  end type mean_type

  type stddev_type                            !  This is a structure for a running standard deviation (Welford)
    real(r_quad)      :: n, delta, mean, M2   ! 
  end type stddev_type

contains
  subroutine init_dummy bind(c)
    print *,'Initializing read_dummy module...default ndata = 5'
    ndata = 5
    linit = .true.
  end subroutine init_dummy

  subroutine set_ndata(nd) bind(c)
    integer, intent(in) :: nd

    call test_init
    print *,'Setting ndata = ',nd
    ndata = nd
  end subroutine set_ndata

  subroutine test_init bind(c)
    if (.not. linit) then
      print *,'ERROR: module not initialized - must call init_dummy'
      call abort
    endif
  end subroutine test_init

  subroutine inc_mean(ob, mean) bind(c)
    real(r_single),intent(in)     :: ob
    type(mean_type),intent(inout) :: mean

    mean%total = mean%total + ob
    mean%n     = mean%n + 1
  end subroutine inc_mean 

  real(r_single) function ret_mean(mean) bind(c)
    type(mean_type),intent(in)  :: mean

    ret_mean = mean%total / mean%n
  end function ret_mean

  real(r_single) function ret_mean_from_array(array, ndata) !bind(c)
    integer(i_kind),intent(in)              :: ndata
    real(r_single),dimension(:),intent(in)  :: array

    real(r_quad)    :: total, n
    integer(i_kind) :: i
  
    total = 0
    n = 0 

    do i=1,ndata
      total = total + array(i)
      n = n + 1
    enddo

    ret_mean_from_array = total / n
  end function ret_mean_from_array

  subroutine print_array(array, ndata) !bind(c)
    integer(i_kind),intent(in)              :: ndata
    real(r_single),dimension(:),intent(in)  :: array

    integer(i_kind) :: i

    do i=1,ndata
      print *,'i,array(i) = ',i,array(i)
    enddo
  end subroutine print_array

  subroutine write_array(lun,filename,array,ndata) bind(c)
    integer(i_kind), intent(in)                           :: lun
    character, dimension(120),intent(in)                              :: filename
    real(r_single),dimension(ndata),intent(in) :: array
    integer(i_kind),intent(in)                           :: ndata 
    
    open(lun,file=filename,form='unformatted')
    print *,'Writing array of length=',ndata
    write(lun) ndata
    write(lun) array
    close(lun)
  end subroutine write_array

  subroutine read_array(lun,filename,array,ndata) !bind(c)
    integer(i_kind), intent(in)                           :: lun
    character, dimension(120),intent(in)                              :: filename
    real(r_single),dimension(:),intent(inout),allocatable :: array
    integer(i_kind), intent(out)                          :: ndata

    open(lun,file=filename,form='unformatted')
    read(lun) ndata
    print *,'Reading array of length=',ndata
    allocate(array(ndata))

    read(lun) array
    close(lun)
  end subroutine read_array

  subroutine get_header(inlun,head) bind(c)
    integer(i_kind),intent(in)    :: inlun
    type(header_list),intent(out) :: head

    call test_init

    write(*,*)'Getting Header...'

    head%header_title = 'Hi Albert!'
    head%ndata        = ndata
    head%nchan        = 1
    head%dummy        = 1.2345
  end subroutine get_header

  subroutine get_data(inlun,dat) bind(c)
    integer(i_kind),intent(in)    :: inlun
    type(data_list),intent(out) :: dat

    write(*,*)'Getting Data...'

    dat%obs   = data_ct
    dat%error = -1.0 * data_ct
    data_ct = data_ct + 1
  end subroutine get_data

end module read_dummy
  

    
