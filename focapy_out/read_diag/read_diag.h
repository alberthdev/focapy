#include <stdint.h>

/* Top-level element variable declarations */
extern int *ireal_radiag;
extern int *ireal_old_radiag;
extern int *ipchan_radiag;
extern int *iversion_radiag;
extern int *iversion_radiag_1;
extern int *iversion_radiag_2;
extern int *iversion_radiag_3;
extern int *iversion_radiag_4;
extern float *rmiss_radiag;

/* Derived type structures */
#pragma pack(2)

typedef struct diag_header_fix_list_ {
    char isis[20];
    char id[10];
    char obstype[10];
    int jiter;
    int nchan;
    int npred;
    int idate;
    int ireal;
    int ipchan;
    int iextra;
    int jextra;
    int idiag;
    int angord;
    int iversion;
    int inewpc;
    int isens;
} diag_header_fix_list, *p_diag_header_fix_list;

typedef struct diag_data_name_list_ {
    char fix[10];
    char chn[10];
} diag_data_name_list, *p_diag_data_name_list;

typedef struct diag_header_chan_list_ {
    float freq;
    float polar;
    float wave;
    float varch;
    float tlapmean;
    int iuse;
    int nuchan;
    int iochan;
} diag_header_chan_list, *p_diag_header_chan_list;

typedef struct diag_data_fix_list_ {
    float lat;
    float lon;
    float zsges;
    float obstime;
    float senscn_pos;
    float satzen_ang;
    float satazm_ang;
    float solzen_ang;
    float solazm_ang;
    float sungln_ang;
    float water_frac;
    float land_frac;
    float ice_frac;
    float snow_frac;
    float water_temp;
    float land_temp;
    float ice_temp;
    float snow_temp;
    float soil_temp;
    float soil_mois;
    float land_type;
    float veg_frac;
    float snow_depth;
    float sfc_wndspd;
    float qcdiag1;
    float qcdiag2;
    float tref;
    float dtw;
    float dtc;
    float tz_tr;
} diag_data_fix_list, *p_diag_data_fix_list;

typedef struct diag_data_chan_list_ {
    float tbobs;
    float omgbc;
    float omgnbc;
    float errinv;
    float qcmark;
    float emiss;
    float tlap;
    float tb_tz;
    float bicons;
    float biang;
    float biclw;
    float bilap2;
    float bilap;
    float bicos;
    float bisin;
    float biemis;
    float bifix;
    float bisst;
} diag_data_chan_list, *p_diag_data_chan_list;

typedef struct diag_data_extra_list_ {
    float extra;
} diag_data_extra_list, *p_diag_data_extra_list;

#pragma pack()

/* Subroutine prototypes */
void read_radiag_header(int *ftin, int *npred_radiag, int *retrieval, diag_header_fix_list *header_fix, diag_header_chan_list **header_chan, diag_data_name_list *data_name, int *iflag, int *lverbose);
void read_radiag_data(int *ftin, diag_header_fix_list *header_fix, int *retrieval, diag_data_fix_list *data_fix, diag_data_chan_list **data_chan, diag_data_extra_list *data_extra, int *iflag);

/* Function prototypes */
