#!/usr/bin/env python
# FoCaPy - Fortran to C and Python Wrapper
# Copyright 2014 Albert Huang.
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this program; if not, write to the Free
# Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307 USA
# 

from focapy.focapy import focapy

#in_files = [ "read_diag.f90" ]
in_files = [ "read_dummy.f90" ]

mod_name = "read_dummy"

header_output_file = "read_dummy.h"
python_output_file = "read_dummy.i"
python_name = "read_dummy"

focapy(in_files, mod_name, header_output_file, python_output_file, python_name)
