import f90doc
import sys
from header import *

in_files = [ "read_dummy.f90" ]

header_fh = open("test.h", "w")

header_write_header(header_fh)

programs, modules, functs, subts = f90doc.read_files(in_files)
for mod, name in modules:
    print "Module %s (file '%s'):" % (mod.name, name)
    if len(mod.elements) > 0:
        print "  Elements:"
        for element in mod.elements:
            print "    Element '%s': type '%s'" % (element.name, element.type)
            f_type = element.type.lower()
            
            header_write_type(header_fh, "%s *%s;\n", f_type, element.name, pointer = "*", stub_format = "// STUB: %s %s\n")
        header_write_seperator(header_fh)
    if len(mod.types) > 0:
        print "  Types:"
        header_write_pre_derived_type(header_fh)
        for type in mod.types:
            print "    Type '%s':" % type.name
            header_write_start_derived_type(header_fh, type.name)
            if len(type.elements) > 0:
                for type_ele in type.elements:
                    print "      Element '%s': type '%s'" % (type_ele.name, type_ele.type)
                    f_type_ele_t = type_ele.type.lower()
                    
                    header_write_type(header_fh, "    %s %s;\n", f_type_ele_t, type_ele.name, pointer = "", stub_format = "    // STUB: %s %s\n")
                header_write_end_derived_type(header_fh, type.name)
        header_write_post_derived_type(header_fh)
    
    if len(mod.subts) > 0:
        print "  Subroutines:"
        for subroutine in mod.subts:
            argument_dict = {}
            print "    Subroutine '%s':" % subroutine.name
            header_write_start_subroutine(header_fh, subroutine.name)
            args_list = None
            if len(subroutine.arguments) > 0:
                print "      Arguments:"
                args_list = []
                args_map = {}
                for sub_arg in subroutine.arguments:
                    print "        Argument element '%s': type '%s'" % (sub_arg.name, sub_arg.type)
                    f_type = sub_arg.type
                    
                    header_write_type(args_list, "%s *%s", f_type, sub_arg.name, pointer = "*", stub_format = "/* STUB: %s %s,*/ ")
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

header_fh.close()
