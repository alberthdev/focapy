import sys

import sys, os, inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0], ".")))
if cmd_subfolder not in sys.path:
    print "Adding cmd_subfolder=%s to path..." % cmd_subfolder
    sys.path.insert(0, cmd_subfolder)

import focapy
import cdef
import typedefs
import f90doc
import fcall
import markupsafe
import jinja2
