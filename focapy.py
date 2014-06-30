import f90doc
in_files = [ "read_dummy.f90" ]
default_types  = {
                   'byte'             : 'unsigned char',
                   'integer'          : 'int',
                   'integer*2'        : 'short int',
                   'real'             : 'float',
                   
                   'double precision' : 'double',
                   'logical'          : 'int',
                   'character'        : 'char',
                 }

override_types = {
                   'integer(i_kind)'  : 'int',
                   'real(r_single)'   : 'float',
                 }

regex_chars = r'character\(len=(\d+)\)'
regex_chars_2 = r'character\*(\d+)'

header_fh = open("test.h", "w")
header_fh.write("#include <stdint.h>\n\n")

programs, modules, functs, subts = f90doc.read_files(in_files)
for mod, name in modules:
   print "Module %s (file '%s'):" % (mod.name, name)
   if len(mod.elements) > 0:
      print "  Elements:"
      for element in mod.elements:
         print "    Element '%s': type '%s'" % (element.name, element.type)
         type = element.type.lower()
         if type in default_types:
            header_fh.write("%s *%s;\n" % (default_types[type], element.name))
         elif type in override_types:
            header_fh.write("%s *%s;\n" % (override_types[type], element.name))
         else:
            print "WARNING: Could not find equivalent C definition for type '%s'!" % type
            print "Make sure you define it!"

   if len(mod.types) > 0:
      print "  Types:"
      header_fh.write('#pragma pack(2)\n')
      for type in mod.types:
         print "    Type '%s':" % type.name
         header_fh.write("typedef struct %s_ {\n" % type.name)
         if len(type.elements) > 0:
            for type_ele in type.elements:
               print "      Element '%s': type '%s'" % (type_ele.name, type_ele.type)
               type_ele_t = type_ele.type.lower()
               if type_ele_t in default_type_types:
                  header_fh.write("    %s %s;\n" % (default_types[type_ele_t], type_ele.name))
               elif type_ele_t in override_type_types:
                  header_fh.write("    %s %s;\n" % (override_types[type_ele_t], type_ele.name))
               # Hacky
               elif type_ele_t == 'character(len=20)':
                  header_fh.write("    char %s[20];\n" % (type_ele.name))
               else:
                  print "WARNING: Could not find equivalent C definition for type '%s'!" % type
                  print "Make sure you define it!"
            header_fh.write("} %s, *p_%s;\n" % (type.name, type.name))
      header_fh.write('#pragma pack()\n')
   
   if len(mod.subts) > 0:
      print "  Subroutines:"
      for subroutine in mod.subts:
         argument_dict = {}
         print "    Subroutine '%s':" % subroutine.name
         header_fh.write("void %s(" % subroutine.name)
         if len(subroutine.arguments) > 0:
            print "      Arguments:"
            args_list = []
            args_map = {}
            for sub_arg in subroutine.arguments:
               print "        Argument element '%s': type '%s'" % (sub_arg.name, sub_arg.type)
               type = sub_arg.type
               if type in default_types:
                  args_list.append("%s *%s" % (default_types[type], sub_arg.name))
                  args_map[type] = "%s *%s" % (default_types[type], sub_arg.name)
               elif type in override_types:
                  args_list.append("%s *%s" % (override_types[type], sub_arg.name))
                  args_map[type] = "%s *%s" % (override_types[type], sub_arg.name)
               # Hacky
               elif type == "type(header_list)":
                  args_list.append("header_list *%s" % (sub_arg.name))
                  args_map[type] = "header_list *%s" % (sub_arg.name)
               elif type == "type(data_list)":
                  args_list.append("data_list *%s" % (sub_arg.name))
                  args_map[type] = "data_list *%s" % (sub_arg.name)
               else:
                  print "WARNING: Could not find equivalent C definition for type '%s'!" % type
                  print "Make sure you define it!"
               if len(sub_arg.attributes) > 0:
                  print "          Attributes: %s" % ( ", ".join([("'%s'" % x) for x in sub_arg.attributes]) )
                  for attr in sub_arg.attributes:
                     if not sub_arg.name in argument_dict:
                        argument_dict[sub_arg.name] = []
                     if not attr in argument_dict[sub_arg.name]:
                        argument_dict[sub_arg.name].append(attr)
         header_fh.write("%s);\n" % ", ".join(args_list))
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
            

header_fh.close()