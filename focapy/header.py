import re
from typedefs import *

def header_write_default_type(fh, c_format, f_type, name):
    if type(fh) == list:
        fh.append(c_format % (f_type, name))
    else:
        fh.write(c_format % (f_type, name))

def header_write_extended_type(fh, c_format, f_type, name, stub_format = "// STUB: %s %s\n"):
    f_type_base = f_type.split("*")[0].split("(")[0]
    subst_made = False
    for generic_re in GENERIC_REGEX:
        regex = re.compile(f_type_base + generic_re)
        match = regex.search(f_type)
        if match:
            found_match = match.groups()[0]
            if found_match.isdigit():
                found_match = int(found_match)
            if found_match in TYPE_TABLE[f_type_base]:
                if type(fh) == list:
                    fh.append(c_format % (TYPE_TABLE[f_type_base][found_match], name))
                else:
                    fh.write(c_format % (TYPE_TABLE[f_type_base][found_match], name))
                subst_made = True
                break
    if not subst_made:
        print "WARNING: Could not find equivalent C definition for type '%s'!" % f_type
        print "Make sure you define it!"
        if type(fh) == list:
            fh.append(stub_format % (f_type, name))
        else:
            fh.write(stub_format % (f_type, name))

def header_write_custom_type(fh, c_format, f_type, name, pointer = ""):
    f_type_base = f_type.split("*")[0].split("(")[0]
    # Validation
    if "regex" not in CUSTOM_TYPES[f_type_base]:
        print "ERROR: Custom types dict is invalid! (Regex definition not found!)"
        sys.exit(1)
    if "map" not in CUSTOM_TYPES[f_type_base]:
        print "ERROR: Custom types dict is invalid! (Map definition not found!)"
        sys.exit(1)
    if "format" not in CUSTOM_TYPES[f_type_base]:
        print "ERROR: Custom types dict is invalid! (Map definition not found!)"
        sys.exit(1)
    for reg in CUSTOM_TYPES[f_type_base]["regex"]:
        regex = re.compile(reg)
        match = regex.search(f_type)
        if match:
            # Map check
            if len(match.groups()) == 0:
                print "ERROR: No match groups defined for regex!"
                sys.exit(1)
            if len(CUSTOM_TYPES[f_type_base]["map"]) != len(match.groups()):
                print "ERROR: Number of regex matches does not match number of maps! (Map has %i, match has %i)" % (len(CUSTOM_TYPES[f_type_base]["map"]), len(match.groups()))
                sys.exit(1)
            map_dict = {}
            map_res = match.groups()
            for i in xrange(0, len(map_res)):
                # Validate
                map_split = CUSTOM_TYPES[f_type_base]["map"][i].split("=")
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
    final_format = CUSTOM_TYPES[f_type_base]["format"]
    # Variable replacement
    for var in map_dict.keys():
        final_format = final_format.replace("%%" + var + "%%", str(map_dict[var]))
    # Static variable replacement
    final_format = final_format.replace("%NAME%", name);
    final_format = final_format.replace("%POINTER%", pointer);
    
    # Write it out!
    if type(fh) == list:
        fh.append(final_format)
    else:
        fh.write(final_format + ";\n")

def header_write_type(fh, c_format, f_type, name, pointer = "", stub_format = "// STUB: %s %s\n"):
    f_type_base = f_type.split("*")[0].split("(")[0]
    if f_type in DEFAULT_TYPES:
        header_write_default_type(fh, c_format, DEFAULT_TYPES[f_type], name)
    elif f_type in OVERRIDE_TYPES:
        header_write_default_type(fh, c_format, OVERRIDE_TYPES[f_type], name)
    elif f_type_base in TYPE_TABLE.keys():
        header_write_extended_type(fh, c_format, f_type, name, stub_format)
    elif f_type_base in CUSTOM_TYPES.keys():
        header_write_custom_type(fh, c_format, f_type, name, pointer)
    else:
        print "WARNING: Could not find equivalent C definition for type '%s'!" % type
        print "Make sure you define it!"
        if type(fh) == list:
            fh.append(stub_format % (f_type, name))
        else:
            fh.write(stub_format % (f_type, name))

def header_write_header(fh):
    fh.write("#include <stdint.h>\n\n")

def header_write_seperator(fh):
    fh.write("\n")

def header_write_pre_derived_type(fh):
    fh.write('#pragma pack(2)\n\n')

def header_write_post_derived_type(fh):
    fh.write('#pragma pack()\n\n')

def header_write_start_derived_type(fh, name):
    fh.write("typedef struct %s_ {\n" % name)

def header_write_end_derived_type(fh, name):
    fh.write("} %s, *p_%s;\n" % (name, name))
    fh.write("\n")

def header_write_start_subroutine(fh, name):
    fh.write("void %s(" % name)

def header_write_end_subroutine(fh, args_list = None):
    if type(args_list) == list:
        fh.write("%s);\n" % ", ".join(args_list))
    else:
        fh.write(");\n")
