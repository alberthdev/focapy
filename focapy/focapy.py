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
# FoCaPy Main
# 
import f90doc
import sys
from header import *
from python import *
from cmod import *

in_files = [ "read_dummy.f90" ]

mod_name = "read_dummy"

c_output_file = "read_dummy.c"
header_output_file = "read_dummy.h"
python_output_file = "read_dummy.i"
python_name = "read_dummy"

def focapy(in_files, mod_name, c_output_file, header_output_file, python_output_file, python_name):
    header_fh = open(header_output_file, "w")
    python_fh = open(python_output_file, "w")
    cmod_fh = open(c_output_file, "w")

    header_write_header(header_fh)
    python_write_header(python_fh, python_name)
    python_write_c_include(python_fh, header_output_file)
    cmod_write_header(cmod_fh, mod_name)

    programs, modules, functs, subts = f90doc.read_files(in_files)
    for mod, name in modules:
        print "Module %s (file '%s'):" % (mod.name, name)
        if len(mod.elements) > 0:
            print "  Elements:"
            for element in mod.elements:
                print "    Element '%s': type '%s'" % (element.name, element.type)
                f_type = element.type.lower()
                
                header_write_type(header_fh, "%s *%s;\n", f_type, element.name, pointer = "*", stub_format = "// STUB: %s %s\n")
                #python_write_type(python_fh, "%s *%s;\n", f_type, element.name, pointer = "*", stub_format = "// STUB: %s %s\n")
            header_write_seperator(header_fh)
            #python_write_seperator(python_fh)
        if len(mod.types) > 0:
            print "  Types:"
            header_write_pre_derived_type(header_fh)
            for type in mod.types:
                print "    Type '%s':" % type.name
                header_write_start_derived_type(header_fh, type.name)
                python_write_start_derived_type(python_fh, type.name)
                if len(type.elements) > 0:
                    for type_ele in type.elements:
                        print "      Element '%s': type '%s'" % (type_ele.name, type_ele.type)
                        f_type_ele_t = type_ele.type.lower()
                        
                        header_write_type(header_fh, "    %s %s;\n", f_type_ele_t, type_ele.name, pointer = "", stub_format = "    // STUB: %s %s\n")
                        python_write_type(python_fh, "    %s %s;\n", f_type_ele_t, type_ele.name, pointer = "", stub_format = "    // STUB: %s %s\n")
                    header_write_end_derived_type(header_fh, type.name)
                    python_write_end_derived_type(python_fh, type.name)
            header_write_post_derived_type(header_fh)
        
        if len(mod.subts) > 0:
            print "  Subroutines:"
            header_write_start_subroutine(header_fh, "init_c_modules", True)
            header_write_end_subroutine(header_fh)
            python_write_start_subroutine(python_fh, "init_c_modules", True)
            python_write_end_subroutine(python_fh, None, True)
            for subroutine in mod.subts:
                argument_dict = {}
                print "    Subroutine '%s':" % subroutine.name
                header_write_start_subroutine(header_fh, subroutine.name)
                python_write_start_subroutine(python_fh, subroutine.name)
                cmod_write_subroutine_func(cmod_fh, mod_name, subroutine.name)
                args_list = None
                python_args_list = None
                if len(subroutine.arguments) > 0:
                    print "      Arguments:"
                    args_list = []
                    python_args_list = []
                    args_map = {}
                    for sub_arg in subroutine.arguments:
                        print "        Argument element '%s': type '%s'" % (sub_arg.name, sub_arg.type)
                        f_type = sub_arg.type
                        
                        header_write_type(args_list, "%s *%s", f_type, sub_arg.name, pointer = "*", stub_format = "/* STUB: %s %s,*/ ")
                        python_write_type(python_args_list, "%s *INPUT", f_type, sub_arg.name, pointer = "*", stub_format = "/* STUB: %s %s,*/ ", name_replace="INPUT")
                        if len(sub_arg.attributes) > 0:
                            print "          Attributes: %s" % ( ", ".join([("'%s'" % x) for x in sub_arg.attributes]) )
                            for attr in sub_arg.attributes:
                                if not sub_arg.name in argument_dict:
                                    argument_dict[sub_arg.name] = []
                                if not attr in argument_dict[sub_arg.name]:
                                    argument_dict[sub_arg.name].append(attr)
                    #print args_list
                    if len(subroutine.arguments) > 0:
                        final_arg_dict = {"input":[], "output":[]}
                        for arg in argument_dict:
                            for attr in argument_dict[arg]:
                                if attr == "intent(in)":
                                    final_arg_dict["input"].append(arg)
                                if attr == "intent(out)":
                                    final_arg_dict["output"].append(arg)
                    ###############################################
                header_write_end_subroutine(header_fh, args_list)
                python_write_end_subroutine(python_fh, python_args_list)
        if len(mod.functs) > 0:
            print "  Functions:"
            for function in mod.functs:
                argument_dict = {}
                print "    Function '%s':" % function.name
                if function.ret_val:
                    print "      Returns: '%s'" % function.ret_val.type
                else:
                    print "      Returns: None"
                header_write_start_function(header_fh, function.name, function.ret_val.type)
                python_write_start_function(python_fh, function.name, function.ret_val.type)
                cmod_write_subroutine_func(cmod_fh, mod_name, function.name)
                args_list = None
                python_args_list = None
                if len(function.arguments) > 0:
                    print "      Arguments:"
                    args_list = []
                    python_args_list = []
                    args_map = {}
                    for sub_arg in function.arguments:
                        print "        Argument element '%s': type '%s'" % (sub_arg.name, sub_arg.type)
                        f_type = sub_arg.type
                        
                        header_write_type(args_list, "%s *%s", f_type, sub_arg.name, pointer = "*", stub_format = "/* STUB: %s %s,*/ ")
                        python_write_type(python_args_list, "%s *INPUT", f_type, sub_arg.name, pointer = "*", stub_format = "/* STUB: %s %s,*/ ", name_replace="INPUT")
                        if len(sub_arg.attributes) > 0:
                            print "          Attributes: %s" % ( ", ".join([("'%s'" % x) for x in sub_arg.attributes]) )
                            for attr in sub_arg.attributes:
                                if not sub_arg.name in argument_dict:
                                    argument_dict[sub_arg.name] = []
                                if not attr in argument_dict[sub_arg.name]:
                                    argument_dict[sub_arg.name].append(attr)
                    #print args_list
                    if len(function.arguments) > 0:
                        final_arg_dict = {"input":[], "output":[]}
                        for arg in argument_dict:
                            for attr in argument_dict[arg]:
                                if attr == "intent(in)":
                                    final_arg_dict["input"].append(arg)
                                if attr == "intent(out)":
                                    final_arg_dict["output"].append(arg)
                    ###############################################
                header_write_end_function(header_fh, args_list)
                python_write_end_function(python_fh, python_args_list)
    python_write_footer(python_fh)
    cmod_write_footer(cmod_fh, mod_name)
    cmod_fh.close()
    python_fh.close()
    header_fh.close()

if __name__ == "__main__":
    focapy(in_files, mod_name, c_output_file, header_output_file, python_output_file, python_name)
