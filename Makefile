# Constants
BOLD  = "\033[1m"
NBOLD = "\033[0m"
ECHO  = /bin/echo -e

%.o: %.mod

.PHONY: clean pre-python pre-c pre-fortran pre-python c fortran python all-done

all: python c fortran all-done

all-done:
	@$(ECHO) $(BOLD)"Done!"$(NBOLD)

#######################################################################
c: pre-c fcwrap.so read_dummy

pre-c:
	@$(ECHO) $(BOLD)"================================================="$(NBOLD)
	@$(ECHO) $(BOLD)"= Building C wrapper...                         ="$(NBOLD)
	@$(ECHO) $(BOLD)"================================================="$(NBOLD)

read_dummy_run.o: read_dummy.h src/read_dummy_run.c
	@$(ECHO) $(BOLD)" ** Compiling C program..."$(NBOLD)
	icc -g -Isrc/fcwrap/include -I. -c src/read_dummy_run.c

read_dummy: read_dummy.mod read_dummy_run.o
	@$(ECHO) $(BOLD)" ** Compiling C program -> final executable..."$(NBOLD)
	#icc -o test test.o read_dummy.o -lifcore -limf
	ifort -g -o read_dummy read_dummy_run.o read_dummy_f2c.o -nofor-main
#######################################################################
fcwrap.o: src/fcwrap/fcwrap.f90
	@$(ECHO) $(BOLD)" ** Compiling Fortran/C wrapper..."$(NBOLD)
	ifort -g -free -fPIC -Isrc/fcwrap/include -c src/fcwrap/fcwrap.f90

fcwrap.so: fcwrap.o
	@$(ECHO) $(BOLD)" ** Compiling Fortran/C wrapper library..."$(NBOLD)
	ifort -g -free -fPIC -shared -o fcwrap.so fcwrap.o -lifcore
#######################################################################
fortran: pre-fortran test_dummy.x

pre-fortran:
	@$(ECHO) $(BOLD)"================================================="$(NBOLD)
	@$(ECHO) $(BOLD)"= Building pure Fortran test...                 ="$(NBOLD)
	@$(ECHO) $(BOLD)"================================================="$(NBOLD)

test_dummy.x: read_dummy.mod test_dummy.o
	ifort -o test_dummy.x test_dummy.o kinds.o read_dummy.o

test_dummy.o:
	ifort -g -free -fPIC -c test_dummy.f90
#######################################################################
read_dummy.o: read_dummy.mod
kinds.o: kinds.mod

read_dummy_.so: read_dummy.mod
	@$(ECHO) $(BOLD)" ** Compiling main Fortran program to shared library..."$(NBOLD)
	ifort -g -free -fPIC -shared -o read_dummy_.so read_dummy.o -lifcore

read_dummy.mod: kinds.mod read_dummy.f90
	@$(ECHO) $(BOLD)" ** Compiling main Fortran program..."$(NBOLD)
	ifort -g -free -fPIC -c read_dummy.f90

kinds.mod: kinds.F90
	@$(ECHO) $(BOLD)" ** Compiling kinds Fortran program..."$(NBOLD)
	ifort -g -free -fPIC -c kinds.F90 -D_REAL8_

python: pre-python read_dummy_.so fcwrap.so _read_dummy.so
#######################################################################
pre-python: 
	@$(ECHO) $(BOLD)"================================================="$(NBOLD)
	@$(ECHO) $(BOLD)"= Building Python module...                     ="$(NBOLD)
	@$(ECHO) $(BOLD)"================================================="$(NBOLD)

read_dummy_f2c.c: read_dummy.h

read_dummy.h: read_dummy.f90
	@$(ECHO) $(BOLD)" ** Running FoCaPy..."$(NBOLD)
	python focapy.py

_read_dummy.so: read_dummy.h read_dummy_f2c.o read_dummy_wrap.o
	@$(ECHO) $(BOLD)" ** Compiling Python shared library..."$(NBOLD)
	#icc -shared -lifcore -o _read_dummy.so read_dummy.o read_dummy_wrap.o
	ifort -shared -lifcore -o _read_dummy.so read_dummy_f2c.o read_dummy_wrap.o

read_dummy_f2c.o: read_dummy_f2c.c
	icc -g -fPIC -Isrc/fcwrap/include -c read_dummy_f2c.c

read_dummy_wrap.c: read_dummy.i
	@$(ECHO) $(BOLD)" ** Running SWIG..."$(NBOLD)
	swig -python -lpointer.i read_dummy.i

read_dummy_wrap.o: read_dummy_wrap.c
	@$(ECHO) $(BOLD)" ** Compiling SWIG wrapper..."$(NBOLD)
	icc -g -fPIC -c read_dummy_wrap.c `python-config --cflags`
#######################################################################
python-opt:
	@$(ECHO) $(BOLD)"================================================="$(NBOLD)
	@$(ECHO) $(BOLD)"= Building optimized Python module...           ="$(NBOLD)
	@$(ECHO) $(BOLD)"================================================="$(NBOLD)
	@$(ECHO) $(BOLD)" ** Running FoCaPy..."$(NBOLD)
	python focapy.py
	@$(ECHO) $(BOLD)" ** Running SWIG..."$(NBOLD)
	swig -python read_dummy.i
	@$(ECHO) $(BOLD)" ** Compiling Fortran program..."$(NBOLD)
	ifort -O3 -free -fPIC -c kinds.F90 -D_REAL8_
	ifort -O3 -free -fPIC -c read_dummy.f90
	@$(ECHO) $(BOLD)" ** Compiling SWIG wrapper..."$(NBOLD)
	icc -O3 -fPIC -c read_dummy_wrap.c `python-config --cflags`
	@$(ECHO) $(BOLD)" ** Compiling Python shared library..."$(NBOLD)
	icc -O3 -shared -lifcore -o _read_dummy.so read_dummy.o read_dummy_wrap.o
	
#######################################################################
clean:
	@$(ECHO) $(BOLD)" ** Cleaning source directory..."$(NBOLD)
	rm -f *.mod *.x *.pyc *.o *.so read_dummy.py read_dummy_wrap.c read_dummy_f2c.c read_dummy.h read_dummy read_dummy.i test.output.binary

clean-c:
	@$(ECHO) $(BOLD)" ** Removing objects from source directory..."$(NBOLD)
	rm -f *.mod *.o *.so
