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

try:
    from collections import OrderedDict
except:
    try:
        from ordereddict import OrderedDict
    except:
        print "ERROR: OrderedDict not found! It is required to run this script."
        sys.exit(1)

def focapy(in_files, mod_name, header_output_file, python_output_file, python_name):
    #header_fh = open(header_output_file, "w")
    #python_fh = open(python_output_file, "w")
    #cmod_fh = open(c_output_file, "w")
    populate(in_files)
    pass

def rprint(odict):
    pass

def populate(in_files):
    module_dict = OrderedDict()
    
    programs, modules, functs, subts = f90doc.read_files(in_files)
    for mod, name in modules:
        print "Module %s (file '%s'):" % (mod.name, name)
        module_dict[mod.name] = OrderedDict()
        module_dict[mod.name]['elements'] = OrderedDict()
        module_dict[mod.name]['types'] = OrderedDict()
        module_dict[mod.name]['subroutines'] = OrderedDict()
        module_dict[mod.name]['functions'] = OrderedDict()
        
        if len(mod.elements) > 0:
            print "  Elements:"
            for element in mod.elements:
                print "    Element '%s': type '%s'" % (element.name, element.type)
                f_type = element.type.lower()
                module_dict[mod.name]['elements'][element.name] = { 'type': element.type, 'attributes': [] }
                if len(element.attributes) > 0:
                    print "      Attributes: %s" % ( ", ".join([("'%s'" % x) for x in element.attributes]) )
                    for attr in element.attributes:
                        if not 'attributes' in module_dict[mod.name]['elements'][element.name]:
                            module_dict[mod.name]['elements'][element.name]['attributes'] = []
                        if not attr in module_dict[mod.name]['elements'][element.name]['attributes']:
                            module_dict[mod.name]['elements'][element.name]['attributes'].append(attr)
        
        # Derived types
        if len(mod.types) > 0:
            print "  Types:"
            for type in mod.types:
                print "    Type '%s':" % type.name
                module_dict[mod.name]['types'][type.name] = OrderedDict()
                module_dict[mod.name]['types'][type.name]['elements'] = OrderedDict()
                if len(type.elements) > 0:
                    for type_ele in type.elements:
                        print "      Element '%s': type '%s'" % (type_ele.name, type_ele.type)
                        module_dict[mod.name]['types'][type.name]['elements'][type_ele.name] = { 'type': type_ele.type, 'attributes': [] }
                        f_type_ele_t = type_ele.type.lower()
                        
                        if len(type_ele.attributes) > 0:
                            print "        Attributes: %s" % ( ", ".join([("'%s'" % x) for x in type_ele.attributes]) )
                            for attr in type_ele.attributes:
                                if not 'attributes' in module_dict[mod.name]['types'][type.name]['elements'][type_ele.name]:
                                    module_dict[mod.name]['types'][type.name]['elements'][type_ele.name]['attributes'] = []
                                if not attr in module_dict[mod.name]['types'][type.name]['elements'][type_ele.name]['attributes']:
                                    module_dict[mod.name]['types'][type.name]['elements'][type_ele.name]['attributes'].append(attr)
        
        if len(mod.subts) > 0:
            print "  Subroutines:"
            
            subroutine_dict = OrderedDict()
            for subroutine in mod.subts:
                argument_dict = OrderedDict()
                subroutine_dict['arguments'] = OrderedDict()
                module_dict[mod.name]['subroutines'][subroutine.name] = OrderedDict()
                print "    Subroutine '%s':" % subroutine.name
                
                if len(subroutine.arguments) > 0:
                    print "      Arguments:"
                    for sub_arg in subroutine.arguments:
                        print "        Argument element '%s': type '%s'" % (sub_arg.name, sub_arg.type)
                        f_type = sub_arg.type
                        
                        subroutine_dict['arguments'][sub_arg.name] = { 'type' : sub_arg.type, 'attributes': [], 'io': '' }
                        
                        if len(sub_arg.attributes) > 0:
                            print "          Attributes: %s" % ( ", ".join([("'%s'" % x) for x in sub_arg.attributes]) )
                            for attr in sub_arg.attributes:
                                if not sub_arg.name in subroutine_dict['arguments']:
                                    subroutine_dict['arguments'][sub_arg.name] = {}
                                if not 'attributes' in subroutine_dict['arguments'][sub_arg.name]:
                                    subroutine_dict['arguments'][sub_arg.name]['attributes'] = []
                                if not attr in subroutine_dict['arguments'][sub_arg.name]['attributes']:
                                    subroutine_dict['arguments'][sub_arg.name]['attributes'].append(attr)
                                
                                if attr == "intent(in)":
                                    subroutine_dict['arguments'][sub_arg.name]['io'] = "input";
                                elif attr == "intent(out)":
                                    subroutine_dict['arguments'][sub_arg.name]['io'] = "output";
                                elif attr == "intent(inout)":
                                    subroutine_dict['arguments'][sub_arg.name]['io'] = "input|output";
                                else:
                                    # EEEEEEEEK
                                    pass
                    
                    #print subroutine_dict['arguments']
                else:
                    print "      [No arguments]"
                    ###############################################
                module_dict[mod.name]['subroutines'][subroutine.name].update(subroutine_dict)
        if len(mod.functs) > 0:
            print "  Functions:"
            
            function_dict = OrderedDict()
            for function in mod.functs:
                function_dict['arguments'] = OrderedDict()
                module_dict[mod.name]['functions'][function.name] = OrderedDict()
                module_dict[mod.name]['functions'][function.name]['returns'] = None
                argument_dict = OrderedDict()
                print "    Function '%s':" % function.name
                if function.ret_val:
                    print "      Returns: '%s'" % function.ret_val.type
                    module_dict[mod.name]['functions'][function.name]['returns'] = function.ret_val.type
                else:
                    print "      Returns: None"
                
                if len(function.arguments) > 0:
                    print "      Arguments:"
                    for fun_arg in function.arguments:
                        print "        Argument element '%s': type '%s'" % (fun_arg.name, fun_arg.type)
                        f_type = fun_arg.type
                        
                        function_dict['arguments'][fun_arg.name] = { 'type' : fun_arg.type, 'attributes': [], 'io': '' }
                        
                        if len(fun_arg.attributes) > 0:
                            print "          Attributes: %s" % ( ", ".join([("'%s'" % x) for x in fun_arg.attributes]) )
                            for attr in fun_arg.attributes:
                                if not fun_arg.name in function_dict['arguments']:
                                    function_dict['arguments'][fun_arg.name] = {}
                                if not 'attributes' in function_dict['arguments'][fun_arg.name]:
                                    function_dict['arguments'][fun_arg.name]['attributes'] = []
                                if not attr in function_dict['arguments'][fun_arg.name]['attributes']:
                                    function_dict['arguments'][fun_arg.name]['attributes'].append(attr)
                                
                                if attr == "intent(in)":
                                    function_dict['arguments'][fun_arg.name]['io'] = "input";
                                elif attr == "intent(out)":
                                    function_dict['arguments'][fun_arg.name]['io'] = "output";
                                elif attr == "intent(inout)":
                                    function_dict['arguments'][fun_arg.name]['io'] = "input|output";
                                else:
                                    # EEEEEEEEK
                                    pass
                            ###############################################
                            #print subroutine_dict['arguments']
                        else:
                            print "      [No arguments]"
                            ###############################################
                        module_dict[mod.name]['functions'][function.name].update(function_dict)
        #import json
        #print(json.dumps(module_dict, indent=4))
        
        return module_dict

if __name__ == "__main__":
    focapy(in_files, mod_name, c_output_file, header_output_file, python_output_file, python_name)
