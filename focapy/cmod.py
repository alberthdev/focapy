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
# C Module Writing Functions
# 
import re
import fcall
from typedefs import *

def cmod_subst_prefix(src, prefix):
    return src.replace("%PREFIX%", prefix)

def cmod_write_header(fh, mod_name):
    cmod_top = open("./template/cmod_top.c", "r")
    fh.write((cmod_top.read()).replace("%MODNAME%", mod_name))
    cmod_top.close()
    
    cmod_fcwrap_init = open("./template/cmod_fcwrap_init_module.c", "r")
    fh.write(cmod_subst_prefix(cmod_fcwrap_init.read(), fcall.getPrefix("fcwrap")))
    cmod_fcwrap_init.close()
    
    fh.write("\n")
    
    cmod_fcwrap_init = open("./template/cmod_mod_init_module_so.c", "r")
    fh.write(cmod_subst_prefix(cmod_fcwrap_init.read().replace("%MODNAME%", mod_name), fcall.getPrefix(mod_name)))
    cmod_fcwrap_init.close()

def cmod_write_subroutine_func(fh, mod_name, sub_func_name):
    cmod_func_init = open("./template/cmod_mod_init_module_funcs.c", "r")
    cmod_func_init_templ = cmod_func_init.read()
    cmod_func_init_templ = cmod_func_init_templ.replace("%FUNCNAME%", sub_func_name)
    fh.write(cmod_subst_prefix(cmod_func_init_templ, fcall.getPrefix(mod_name)))
    cmod_func_init.close()
    fh.write("\n")

def cmod_write_footer(fh, mod_name):
    cmod_bottom = open("./template/cmod_bottom.c", "r")
    fh.write(cmod_bottom.read().replace("%MODNAME%", mod_name))
    cmod_bottom.close()
