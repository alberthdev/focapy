#include "read_diag.h"

  diag_header_fix_list  *headfix;
  diag_header_chan_list *headchan; // ALLOCATABLE (:)
  diag_data_name_list   *headname;

  diag_data_fix_list *datafix;
  diag_data_chan_list *datachan; // ALLOCATABLE (:)
  diag_data_extra_list *dataextra; // ALLOCATABLE (:,:)

  long double ret_var;
  long double ret_stddev;
// optional namelist inputs - can be overriden in a radmon_diag_bin2txt.nl
  bool debug = false;
  int npred_read = 7;
  bool sst_ret = false;
  int iversion = -9999;
  //namelist /nlconfig/ debug, npred_read, sst_ret, iversion

  character*256 infn, outfn

  int inlun = 51;
  int outlun= 52;
  int nllun = 53;

  int strlen, iflag;
  int iuse, ich, nch, ipr, iob;

  logical,dimension(:),allocatable     :: luse
  bool lqcpass;

  float tob1, tob2, clat, clon

  float missing = -9999.999
  int imissing = -9999
  int nvar = 4 // number of positions in array needed for inline variance calc
// variables for output, all to be allocated as nchan.  Variances will be calculated using inline algorithm
// accredited to Welford, according
  real(r_quad),dimension(:),allocatable   :: nobstotal, nobsassim, tbtotal, tbassim, omf_nbc , omf_bc , sigo, jo
  real(r_quad),dimension(:,:),allocatable ::                                         vomf_nbc, vomf_bc
// total bias and fixed bias terms.  When Yanqui's variational angle correction is brought in, this may need to be updated.
  real(r_quad),dimension(:),allocatable   :: totbias , fixbias
  real(r_quad),dimension(:,:),allocatable :: vtotbias, vfixbias
// variational bias correction variables, which will be allocated as nchan and npred_read
  real(r_quad),dimension(:,:),allocatable   :: biasterms
  real(r_quad),dimension(:,:,:),allocatable :: vbiasterms
// Definitions for above variables - 
//   nobstotal        - number of observations considered - total
//   nobsassim        - number of observations that are assimilated
//   tbtotal          - mean brightness temperature of all observations
//   tbassim          - mean brightness temperature of assimilated observations
//   omf_nbc/vomf_nbc - mean/variance of O-F without bias correction applied  
//   omf_bc/vomf_bc   - mean/variance of O-F with bias correction applied
//   sigo             - mean observation error of assimilated observations
//   jo               - mean cost (Jo) of assimilated observations
//   totbias/vtotbias - mean/variance of bias correction applied to assimilated observations
//   fixbias/vfixbias - mean/variance of fixed scan angle position bias correction (sac.x-derived)
//   biasterms
//        /vbiasterms - means/variances of the variational terms as defined by npred_read.  

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

// -----------NAMELIST READING:
//  Reads the variables defined in nlconfig above from nlfn ^^^

  inquire(file=nlfn, exist=lnamelist)

  if (lnamelist) then
    open(nllun,file=nlfn)
    read(nllun,nml=nlconfig)
    close(nllun)
  endif
// -----------------------

  if (debug)
    printf("Debugging on - Verbose Printing\n");

  // get infn from command line
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

  read_radiag_header( inlun, npred_read, sst_ret, headfix, headchan, headname, iflag, debug );

  nch = headfix->nchan

  printf("--------HEADER INFORMATION--------\n");
  printf("headfix%nchan=%i\n",headfix%nchan);
  printf("headfix%isis=%i\n",headfix%isis);
  printf("headfix%id=%i\n",headfix%id);
  printf("headfix%obstype=%i\n",headfix%obstype);

  printf("headchan(1)%freq=%i\n",headchan(1)%freq);
  printf("headchan(1)%wave=%i\n",headchan(1)%wave);
  printf("headchan(1)%iuse=%i\n",headchan(1)%iuse);

  if (iversion < 0) {
    printf("BE AWARE THAT iversion IS BEING OVERRIDEN!\n");
    printf(" iversion diag, override=%i\n",headfix%iversion,iversion);
    printf(" (this was made necessary w/ emis bc...hopefully only temporary)\n");;
    headfix->iversion = iversion;
  }

  iob = 1;

  while (iflag >= 0) { // iflag == 0 means the end of the file
    read_radiag_data  ( inlun, headfix, false, datafix, datachan, \
                             dataextra, iflag );

    if (iflag < 0) continue;
    tob1=datachan[0]->tbobs;
    tob2=datachan[1]->tbobs;
    clat=datafix->lat;
    clon=datafix->lon;

    if (iob <= 2) {
      printf("------OBSERVATION %i------\n", iob);
      printf("datachan(1)%tbobs=%.4f\n",datachan[0]->tbobs);
      printf("datachan(2)%tbobs=%.4f\n",datachan[1]->tbobs);
      printf("datafix%lat=%.5f\n",datafix->lat);
      printf("datafix%lon=%.5f\n",datafix->lon);
    }
    iob = iob + 1;
  }

  printf("------OBSERVATION %i------\n", iob);
  printf("datachan(1)%tbobs=%.4f\n",tob1);
  printf("datachan(2)%tbobs=%.4f\n",tob2);
  printf("datafix%lat=%.5f\n",clat);
  printf("datafix%lon=%.5f\n",clon);

}


