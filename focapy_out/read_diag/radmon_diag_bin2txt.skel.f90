program radmon_diag_bin2txt

  use read_diag,only:read_radiag_header, diag_header_fix_list, diag_header_chan_list, diag_data_name_list
  use read_diag,only:read_radiag_data, diag_data_fix_list, diag_data_extra_list, diag_data_chan_list
  use kinds,only: r_quad, r_single

  implicit none 

  type(diag_header_fix_list )          ::  headfix
  type(diag_header_chan_list),allocatable  ::  headchan(:)
  type(diag_data_name_list)            ::  headname

  type(diag_data_fix_list)             ::  datafix
  type(diag_data_chan_list)  ,allocatable  ::  datachan(:)
  type(diag_data_extra_list) ,allocatable  ::  dataextra(:,:)

  real(r_quad)                         ::  ret_var
  real(r_quad)                         ::  ret_stddev
! optional namelist inputs - can be overriden in a radmon_diag_bin2txt.nl
  logical                              ::  debug = .false.
  integer                              ::  npred_read = 7
  logical                              ::  sst_ret = .false.
  integer                              ::  iversion = -9999
  namelist /nlconfig/ debug, npred_read, sst_ret, iversion

  character*256 infn, outfn

  integer,parameter                    ::  inlun = 51
  integer,parameter                    ::  outlun= 52
  integer,parameter                    ::  nllun = 53

  integer strlen, iflag
  integer iuse, ich, nch, ipr, iob

  logical,dimension(:),allocatable     :: luse
  logical lqcpass

  real tob1, tob2, clat, clon

  real(r_single),parameter             ::  missing = -9999.999
  integer,parameter                    ::  imissing = -9999
  integer,parameter                    ::  nvar = 4 ! number of positions in array needed for inline variance calc
! variables for output, all to be allocated as nchan.  Variances will be calculated using inline algorithm
! accredited to Welford, according
  real(r_quad),dimension(:),allocatable   :: nobstotal, nobsassim, tbtotal, tbassim, omf_nbc , omf_bc , sigo, jo
  real(r_quad),dimension(:,:),allocatable ::                                         vomf_nbc, vomf_bc
! total bias and fixed bias terms.  When Yanqui's variational angle correction is brought in, this may need to be updated.
  real(r_quad),dimension(:),allocatable   :: totbias , fixbias
  real(r_quad),dimension(:,:),allocatable :: vtotbias, vfixbias
! variational bias correction variables, which will be allocated as nchan and npred_read
  real(r_quad),dimension(:,:),allocatable   :: biasterms
  real(r_quad),dimension(:,:,:),allocatable :: vbiasterms
! Definitions for above variables - 
!   nobstotal        - number of observations considered - total
!   nobsassim        - number of observations that are assimilated
!   tbtotal          - mean brightness temperature of all observations
!   tbassim          - mean brightness temperature of assimilated observations
!   omf_nbc/vomf_nbc - mean/variance of O-F without bias correction applied  
!   omf_bc/vomf_bc   - mean/variance of O-F with bias correction applied
!   sigo             - mean observation error of assimilated observations
!   jo               - mean cost (Jo) of assimilated observations
!   totbias/vtotbias - mean/variance of bias correction applied to assimilated observations
!   fixbias/vfixbias - mean/variance of fixed scan angle position bias correction (sac.x-derived)
!   biasterms
!        /vbiasterms - means/variances of the variational terms as defined by npred_read.  

! single variables used later for printing purposes
  integer        :: inobstotal, inobsassim
  real(r_single) :: rvomf_nbc, rvomf_bc, rvtotbias, rvfixbias
  real(r_single),dimension(:),allocatable   :: rvbiasterms
  character(len=13),dimension(:),allocatable :: chfrwn 

  integer,parameter              :: max_npred = 9

  character(len=10),dimension(max_npred) :: biasnames  
  data biasnames   / 'bc_const  ', &
                     'bc_satang ', &
                     'bc_tlap   ', &
                     'bc_tlap2  ', &
                     'bc_clw    ', &
                     'bc_coslat ', &
                     'bc_sinlat ', &
                     'bc_emis   ', &
                     'bc_sst    ' /

  real(r_quad) :: cvar, rch

  logical lnamelist, linfile
  character*80                         ::  nlfn = './radmon_diag_bin2txt.nl'

!-----------NAMELIST READING:
! Reads the variables defined in nlconfig above from nlfn ^^^

  inquire(file=nlfn, exist=lnamelist)

  if (lnamelist) then
    open(nllun,file=nlfn)
    read(nllun,nml=nlconfig)
    close(nllun)
  endif
!-----------------------

  if (debug) write(*,*)'Debugging on - Verbose Printing'

  ! get infn from command line
  call getarg(1, infn)

  strlen = len(trim(infn))

  write(*,*)'Input diag file:     ',trim(infn)
  inquire(file=trim(infn), exist=linfile)
  if (.not. linfile) then
    write(*,*)trim(infn) // ' does not exist - exiting'
    call abort
  endif
  
 
  outfn = infn(1:strlen-3) // 'txt'
  write(*,*)'Output text summary: ',trim(outfn)

  iflag = 0

  open(inlun,file=infn,form='unformatted',convert='big_endian')

  call read_radiag_header( inlun, npred_read, sst_ret, headfix, headchan, headname, iflag, debug )

  nch = headfix%nchan

  print *,'--------HEADER INFORMATION--------'
  print *,'headfix%nchan=',headfix%nchan
  print *,'headfix%isis=',headfix%isis
  print *,'headfix%id=',headfix%id
  print *,'headfix%obstype=',headfix%obstype

  print *,'headchan(1)%freq=',headchan(1)%freq
  print *,'headchan(1)%wave=',headchan(1)%wave
  print *,'headchan(1)%iuse=',headchan(1)%iuse


  if (iversion .gt. 0) then
    write(*,*)'BE AWARE THAT iversion IS BEING OVERRIDEN!'
    write(*,*)' iversion diag, override=',headfix%iversion,iversion
    write(*,*)' (this was made necessary w/ emis bc...hopefully only temporary)'
    headfix%iversion = iversion
  endif

  iob = 1

  do while (iflag .ge. 0) ! iflag == 0 means the end of the file
    call read_radiag_data  ( inlun, headfix, .false., datafix, datachan, &
                             dataextra, iflag )

    if (iflag .lt. 0) cycle
    tob1=datachan(1)%tbobs
    tob2=datachan(2)%tbobs
    clat=datafix%lat
    clon=datafix%lon

    if (iob .le. 2) then
      print *,'------OBSERVATION ',iob,'------'
      print *,'datachan(1)%tbobs=',datachan(1)%tbobs
      print *,'datachan(2)%tbobs=',datachan(2)%tbobs
      print *,'datafix%lat=',datafix%lat
      print *,'datafix%lon=',datafix%lon
    endif 
    iob = iob + 1
  enddo

  print *,'------OBSERVATION ',iob,'------'
  print *,'datachan(1)%tbobs=',tob1
  print *,'datachan(2)%tbobs=',tob2
  print *,'datafix%lat=',clat
  print *,'datafix%lon=',clon


end program radmon_diag_bin2txt


