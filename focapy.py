import f90doc
import re
import sys

in_files = [ "read_dummy.f90" ]
default_types  = {
                    'byte'              : 'unsigned char',
                    'integer'           : 'int',
                    'real'              : 'float',

                    'double precision'  : 'double',
                    'logical'           : 'int',
                    'character'         : 'char',
                 }

type_table = {
                'integer'   :
                                {
                                    1           : 'unsigned char',
                                    2           : 'short int',
                                    3           : 'int',
                                    4           : 'long long int',
                                    'i_kind'    : 'int',
                                    'i_byte'    : 'unsigned char',
                                    'i_short'   : 'short int',
                                    'i_long'    : 'int',
                                    'i_llong'   : 'long long int',
                                },
                'real'      :
                                {
                                    4           : 'float',
                                    8           : 'double',
                                    16          : 'long double',
                                    'r_kind'    : 'double',
                                    'r_single'  : 'float',
                                    'r_double'  : 'double',
                                    'r_quad'    : 'long double',
                                },
             }

# Format:
# regex  - the regex to match the Fortran type.
# map    - a mapping of each regex match to a named variable, respectively
#          by array. Format: map_var = %TYPE_VAR%. Uses %TYPE_VARS%:
#              %INT%    - Match integer type.
#              %STRING% - Match string type.
# format - final C header component to be written. Uses %VAR_CONTEXT_VARS%
#          and %%map_var%%.
#          %VAR_CONTEXT_VARS%:
#              %NAME%   - Variable name.

custom_types = {
                'character' :
                            {
                                'regex':
                                        [ ## TODO: variable value support
                                            r'character\(len=(\d+)\)',
                                            r'character\*(\d+)',
                                        ],
                                'map'   :
                                        [
                                            'length=%INT%',
                                        ],
                                'format':   'char %NAME%[%%length%%]',
                            },
                'type'      :
                            {
                                'regex':
                                        [
                                            r'type\(\w+\)',
                                        ],
                                'map'   :
                                        [
                                            'type_name=%STRING%',
                                        ],
                                'format':   '%%type_name%% %NAME%',
                            },
               }
                                        
override_types = {
                   #'integer(i_kind)'  : 'int',
                   #'real(r_single)'   : 'float',
                 }

generic_regex  = [
                    r'\((\w+)\)',
                    r'\*(\w+)',
                 ]

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
            type_base = type.split("*")[0].split("(")[0]
            if type in default_types:
                header_fh.write("%s *%s;\n" % (default_types[type], element.name))
            elif type in override_types:
                header_fh.write("%s *%s;\n" % (override_types[type], element.name))
            elif type_base in type_table.keys():
                subst_made = False
                for generic_re in generic_regex:
                    regex = re.compile(type_base + generic_re)
                    match = regex.search(type)
                    if match:
                        found_match = match.groups()[0]
                        if found_match.isdigit():
                            found_match = int(found_match)
                        if found_match in type_table[type_base]:
                            header_fh.write("%s %s;\n" % (type_table[type_base][found_match], element.name))
                            subst_made = True
                            break
                if not subst_made:
                    print "WARNING: Could not find equivalent C definition for type '%s'!" % type
                    print "Make sure you define it!"
                    header_fh.write("// STUB: %s %s\n" % (type, element.name))
            elif type_base in custom_types.keys():
                # Validation
                if "regex" not in custom_types[type_base]:
                    print "ERROR: Custom types dict is invalid! (Regex definition not found!)"
                    sys.exit(1)
                if "map" not in custom_types[type_base]:
                    print "ERROR: Custom types dict is invalid! (Map definition not found!)"
                    sys.exit(1)
                if "format" not in custom_types[type_base]:
                    print "ERROR: Custom types dict is invalid! (Map definition not found!)"
                    sys.exit(1)
                for reg in custom_types[type_base]["regex"]:
                    regex = re.compile(reg)
                    match = regex.search(type)
                    if match:
                        # Map check
                        if len(custom_types[type_base]["map"]) != len(match.groups()):
                            print "ERROR: Number of regex matches does not match number of maps!"
                            sys.exit(1)
                        map_dict = []
                        map_res = match.groups()
                        for i in xrange(0, len(map_res)):
                            # Validate
                            map_split = custom_types[type_base]["map"][i].split("=")
                            if len(map_split) != 2:
                                print "ERROR: Map specification is invalid! It should be variable=%TYPE%!"
                                sys.exit(1)
                            if not ((map_split[1][0] == "%") and (map_split[1][-1] == "%")):
                                print "ERROR: Map specification is invalid! The type part is invalid - it should be variable=%TYPE%!"
                                sys.exit(1)
                            map_name = map_split[0]
                            map_type = map_split[1].upper()
                            if map_type == "%INT%":
                                map_dict[map_name] = int(map_res[i])
                            elif map_type == "%FLOAT%":
                                map_dict[map_name] = float(map_res[i])
                            elif map_type == "%STRING%":
                                map_dict[map_name] = str(map_res[i])
                            else:
                                print "ERROR: Map specification is invalid! (Invalid type found - valid: %INT%, %FLOAT%, %STRING%)"
                                sys.exit(1)
                final_format = custom_types[type_base]["format"]
                # Variable replacement
                for var in map_dict.keys():
                    final_format = final_format.replace("%%" + var + "%%", map_dict[var])
                # Static variable replacement
                final_format = final_format.replace("%NAME%", element.name);
                final_format = final_format.replace("%POINTER%", "");
                
                # Write it out!
                header_fh.write(final_format + ";\n")
            else:
                print "WARNING: Could not find equivalent C definition for type '%s'!" % type
                print "Make sure you define it!"
                header_fh.write("// STUB: %s %s\n" % (type, element.name))

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
                   type_ele_t_base = type_ele_t.split("*")[0].split("(")[0]
                   if type_ele_t in default_types:
                       header_fh.write("    %s %s;\n" % (default_types[type_ele_t], type_ele.name))
                   elif type_ele_t in override_types:
                       header_fh.write("    %s %s;\n" % (override_types[type_ele_t], type_ele.name))
                   elif type_ele_t_base in type_table.keys():
                       subst_made = False
                       for generic_re in generic_regex:
                           print "DEBUG: SEARCH: "+(type_ele_t_base + generic_re)
                           regex = re.compile(type_ele_t_base + generic_re)
                           match = regex.search(type_ele_t)
                           if match:
                               print "MATCH!"
                               found_match = match.groups()[0]
                               if found_match.isdigit():
                                   found_match = int(found_match)
                               if found_match in type_table[type_ele_t_base]:
                                   header_fh.write("    %s %s;\n" % (type_table[type_ele_t_base][found_match], type_ele.name))
                                   subst_made = True
                                   break
                       if not subst_made:
                           print "WARNING: Could not find equivalent C definition for type '%s'!" % type_ele_t
                           print "Make sure you define it!"
                           header_fh.write("    // STUB: %s %s\n" % (type_ele_t, type_ele.name))
                   # Hacky
                   elif type_ele_t == 'character(len=20)':
                       header_fh.write("    char %s[20];\n" % (type_ele.name))
                   else:
                       print "WARNING: Could not find equivalent C definition for type '%s'!" % type_ele_t
                       print "Make sure you define it!"
                       header_fh.write("    // STUB: %s %s\n" % (type_ele_t, type_ele.name))
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
                   type_base = type.split("*")[0].split("(")[0]
                   if type in default_types:
                       args_list.append("%s *%s" % (default_types[type], sub_arg.name))
                       args_map[type] = "%s *%s" % (default_types[type], sub_arg.name)
                   elif type in override_types:
                       args_list.append("%s *%s" % (override_types[type], sub_arg.name))
                       args_map[type] = "%s *%s" % (override_types[type], sub_arg.name)
                   elif type_base in type_table.keys():
                       subst_made = False
                       for generic_re in generic_regex:
                           regex = re.compile(type_base + generic_re)
                           match = regex.search(type)
                           if match:
                               found_match = match.groups()[0]
                               if found_match.isdigit():
                                   found_match = int(found_match)
                               if found_match in type_table[type_base]:
                                   args_list.append("%s *%s" % (type_table[type_base][found_match], sub_arg.name))
                                   args_map[type] = "%s *%s" % (type_table[type_base][found_match], sub_arg.name)
                                   subst_made = True
                                   break
                       if not subst_made:
                           print "WARNING: Could not find equivalent C definition for type '%s'!" % type
                           print "Make sure you define it!"
                           header_fh.write("/* STUB: %s %s,*/ " % (type, sub_arg.name))
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
                       header_fh.write("/* STUB: %s %s,*/ " % (type, sub_arg.name))
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
