########################################################################
# Focapy Build System
# Makefile to build focapy generated files
# ----------------------------------------------------------------------
# Generated with Focapy v0.5b-CODENAME
#   at 2014-07-17 09:10:58.819122000 -0400
# Fortran modules: read_diag
########################################################################

# Constants

# Print constants
BOLD  = "\033[1m"
NBOLD = "\033[0m"
ECHO  = /bin/echo -e

# Default flags for building
CFLAGS      = -fPIC
FCFLAGS     = -free -fPIC

# Optional flags, set either by user or by target
CFLAGS_OPT  =
FCFLAGS_OPT =

# Compilers
CC          = icc
FC          = ifort

%.o: %.mod

.PHONY: clean clean-g clean-c clean-obj clean-fortran clean-misc
.PHONY: pre-make pre-fortran-core pre-python pre-c pre-fortran pre-opt pre-clean pre-debug
.PHONY: c fortran python fortran-core
.PHONY: opt debug
.PHONY: all-done
.PHONY: info help

all: pre-make c fortran python all-done

pre-make:
	@$(ECHO) $(BOLD)"Focapy Build System"$(NBOLD)

all-done:
	@$(ECHO) $(BOLD)" ** Done!"$(NBOLD)
#######################################################################
info:
	@$(ECHO) $(BOLD)"`head -n 8 Makefile`"$(NBOLD)

help: pre-make
	@$(ECHO) $(BOLD)"Help:"$(NBOLD)
	@$(ECHO) $(BOLD)"  General targets:"$(NBOLD)
	@$(ECHO) "    make (or make all):"
	@$(ECHO) "      Build all general targets."
	@$(ECHO) "    make python:"
	@$(ECHO) "      Build Python module."
	@$(ECHO) "    make fortran-core:"
	@$(ECHO) "      Build Fortran module core."
	@$(ECHO) "    make c:"
	@$(ECHO) "      Build C source. (NOT part of Focapy generated files!)"
	@$(ECHO) "    make fortran:"
	@$(ECHO) "      Build Fortran source. (NOT part of Focapy generated files!)"
	@$(ECHO) $(BOLD)"  Optimized targets:"$(NBOLD)
	@$(ECHO) "    make opt:"
	@$(ECHO) "      Build everything, optimized to the max with -O3."
	@$(ECHO) $(BOLD)"  Debug targets:"$(NBOLD)
	@$(ECHO) "    make debug:"
	@$(ECHO) "      Build everything, with debugging enabled via -g."
	@$(ECHO) $(BOLD)"  Cleanup:"$(NBOLD)
	@$(ECHO) "    make clean:"
	@$(ECHO) "      Clean up everything. This include all targets below."
	@$(ECHO) "    make clean-gen:"
	@$(ECHO) "      Clean up SWIG generated files and objects."
	@$(ECHO) "    make clean-c:"
	@$(ECHO) "      Clean up C source objects."
	@$(ECHO) "    make clean-obj:"
	@$(ECHO) "      Clean up ALL objects."
	@$(ECHO) "    make clean-fortran:"
	@$(ECHO) "      Clean up Fortran source objects."
	@$(ECHO) "    make clean-misc:"
	@$(ECHO) "      Clean up miscellaneous files and objects."
	@$(ECHO) $(BOLD)"  Build system:"$(NBOLD)
	@$(ECHO) "    make info:"
	@$(ECHO) "      Display information about this build system."
	@$(ECHO) "    make help:"
	@$(ECHO) "      Show this help."
#######################################################################
opt: FCFLAGS_OPT = -O3
opt: CFLAGS_OPT  = -O3
opt: pre-opt python c fortran all-done

pre-opt:
	@$(ECHO) $(BOLD)" !! Building with optimization enabled..."$(NBOLD)
#######################################################################
debug: FCFLAGS_OPT = -g
debug: CFLAGS_OPT  = -g
debug: pre-debug python c fortran all-done

pre-debug:
	@$(ECHO) $(BOLD)" !! Building with debugging enabled..."$(NBOLD)
#######################################################################
fortran-core: pre-fortran-core read_diag.mod fcwrap.mod

pre-fortran-core:
	@$(ECHO) $(BOLD)" ** Building pure Fortran core modules..."$(NBOLD)

read_diag.o: read_diag.mod
kinds.o: kinds.mod
fcwrap.o: fcwrap.mod

read_diag.mod: kinds.mod read_diag.f90
	@$(ECHO) $(BOLD)"  * Compiling main Fortran program..."$(NBOLD)
	$(FC) $(FCFLAGS_OPT) $(FCFLAGS) -c read_diag.f90

kinds.mod: kinds.F90
	@$(ECHO) $(BOLD)"  * Compiling kinds Fortran program..."$(NBOLD)
	$(FC) $(FCFLAGS_OPT) $(FCFLAGS) -c kinds.F90 -D_REAL8_

fcwrap.mod: fcwrap.f90
	@$(ECHO) $(BOLD)"  * Compiling Fortran/C wrapper..."$(NBOLD)
	$(FC) $(FCFLAGS_OPT) $(FCFLAGS) -c fcwrap.f90
#######################################################################
python: pre-python _read_diag.so

pre-python: 
	@$(ECHO) $(BOLD)" ** Building Python module..."$(NBOLD)

_read_diag.so: read_diag.mod fcwrap.mod read_diag_wrap.o
	@$(ECHO) $(BOLD)"  * Compiling Python shared library..."$(NBOLD)
	$(FC) -shared -lifcore -o _read_diag.so read_diag_wrap.o read_diag.o fcwrap.o

read_diag_wrap.c: read_diag.i
	@$(ECHO) $(BOLD)"  * Generating Python wrapper via SWIG..."$(NBOLD)
	swig -python read_diag.i

read_diag_wrap.o: read_diag.h read_diag_wrap.c
	@$(ECHO) $(BOLD)"  * Compiling SWIG wrapper..."$(NBOLD)
	$(CC) $(CFLAGS_OPT) $(CFLAGS) -c read_diag_wrap.c `python-config --cflags`
#######################################################################
c: read_diag.mod fcwrap.mod pre-c read_diag

pre-c:
	@$(ECHO) $(BOLD)" ** Building C wrapper..."$(NBOLD)

read_diag_run.o: read_diag.h src/read_diag_run.c
	@$(ECHO) $(BOLD)"  * Compiling C program..."$(NBOLD)
	$(CC) $(CFLAGS_OPT) $(CFLAGS) -I. -c src/read_diag_run.c

read_diag: read_diag.mod fcwrap.mod read_diag_run.o
	@$(ECHO) $(BOLD)"  * Compiling C program -> final executable..."$(NBOLD)
	$(FC) $(FCFLAGS_OPT) -o read_diag read_diag_run.o read_diag.o fcwrap.o -nofor-main
#######################################################################
fortran: pre-fortran test_dummy.x

pre-fortran:
	@$(ECHO) $(BOLD)" ** Building pure Fortran test..."$(NBOLD)

test_dummy.x: read_diag.mod test_dummy.o
	$(FC) -o test_dummy.x test_dummy.o kinds.o read_diag.o

test_dummy.o:
	$(FC) $(FCFLAGS_OPT) $(FCFLAGS) -c test_dummy.f90
#######################################################################
clean: pre-clean clean-gen clean-c clean-obj clean-fortran clean-misc

pre-clean:
	@$(ECHO) $(BOLD)"  * Cleaning source directory..."$(NBOLD)

clean-gen:
	rm -f *.pyc read_diag.py read_diag_wrap.c _read_diag.so read_diag_wrap.o

clean-c:
	rm -f read_diag read_diag_run.o

clean-obj:
	rm -f *.mod *.o *.so

clean-fortran:
	rm -f *.x

clean-misc:
	rm -f *.pyc test.output.binary
