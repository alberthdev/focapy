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
# C Definition Writing Functions
# 
# Returns for all functions:
#   (c_type, c_var_name, c_pointers, (fort_type, fort_name))
#   Variables:
#     c_type: C equivalent type, without pointers.
#       Examples: void, int, double, float, char
#     c_var_name: C variable name, usually the same as the Fortran name,
#         unless the type is a custom type! No pointers included.
#       Examples:  my_var_name, tiny_var, a_char_array[20]
#     c_pointers: C pointers - provides asteriks for pointers, if
#         necessary. Pointers are specified seperately to allow the
#         template to determine pointer position. If blank, this will be
#         None.
#     fort_type: Fortran native type, usually a copy from the original
#         input.
#       Examples: character, integer(i_kind)
#     fort_name: Fortran native variable name, usually a copy from the
#         original input.
#       Examples: my_var_name, tiny_var, a_char_array
# 
import re
import sys
from typedefs import *

def make_default_type(f_type, name, type_dict):
    if f_type in type_dict:
        if type(type_dict[f_type]) == str:
            return [type_dict[f_type], name, "", [f_type, name]]
        elif type(type_dict[f_type]) == tuple:
            if (type(type_dict[f_type][0]) == str) and (type(type_dict[f_type][1]) == str):
                return [type_dict[f_type][0], name, type_dict[f_type][1], [f_type, name]]
            else:
                print "WARNING: Matched entry in type table, but tuple definition was invalid!"
                print "Entry: %s" % str(type_dict[f_type])
                return [None, None, None, [f_type, name]]
        else:
            print "WARNING: Matched entry in type table, but definition was invalid!"
            print "Entry: %s" % str(type_dict[f_type])
            return [None, None, None, [f_type, name]]
    else:
        print "WARNING: Could not find equivalent C definition for type '%s' in type_dict!" % type
        print "Make sure you define it! (Note that this may be a bug due to the error"
        print "not being triggered at a higher level.)"
        return [None, None, None, [f_type, name]]

def make_extended_type(f_type, name):
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
                if type(TYPE_TABLE[f_type_base][found_match]) == str:
                    return [TYPE_TABLE[f_type_base][found_match], name, '', [f_type, name]]
                elif type(TYPE_TABLE[f_type_base][found_match]) == tuple:
                    if (type(TYPE_TABLE[f_type_base][found_match][0]) == str) and (type(TYPE_TABLE[f_type_base][found_match][1]) == str):
                        return [TYPE_TABLE[f_type_base][found_match][0], name, TYPE_TABLE[f_type_base][found_match][1], [f_type, name]]
                    else:
                        print "WARNING: Matched entry in extended type table, but tuple definition was invalid!"
                        print "Entry: %s" % str(TYPE_TABLE[f_type_base][found_match])
                        return [None, None, None, [f_type, name]]
                else:
                    print "WARNING: Matched entry in extended type table, but definition was invalid!"
                    print "Entry: %s" % str(TYPE_TABLE[f_type_base][found_match])
                    return [None, None, None, [f_type, name]]
                
                subst_made = True
                break
    if not subst_made:
        print "WARNING: Could not find equivalent C definition for type '%s'!" % f_type
        print "Make sure you define it!"
        return [None, None, None, [f_type, name]]

def make_custom_type(f_type, name):
    f_type_base = f_type.split("*")[0].split("(")[0]
    # Validation
    if "regex" not in CUSTOM_TYPES[f_type_base]:
        print "ERROR: Custom types dict '%s' is invalid! (Regex definition not found!)" % f_type_base
        sys.exit(1)
    if "map" not in CUSTOM_TYPES[f_type_base]:
        print "ERROR: Custom types dict '%s' is invalid! (Map definition not found!)" % f_type_base
        sys.exit(1)
    if "name" not in CUSTOM_TYPES[f_type_base]:
        print "ERROR: Custom types dict '%s' is invalid! (Name definition not found!)" % f_type_base
        sys.exit(1)
    if "type" not in CUSTOM_TYPES[f_type_base]:
        print "ERROR: Custom types dict '%s' is invalid! (Core type definition not found!)" % f_type_base
        sys.exit(1)
    if "pointer" not in CUSTOM_TYPES[f_type_base]:
        print "ERROR: Custom types dict '%s' is invalid! (Pointer definition not found!)" % f_type_base
        sys.exit(1)
        
    found_match = False
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
            found_match = True
            break
    
    if not found_match:
        print "WARNING: Could not find equivalent C definition for type '%s'!" % f_type
        print "Make sure you define it!"
        return [None, None, None, [f_type, name]]
    
    final_name = CUSTOM_TYPES[f_type_base]["name"]
    final_type = CUSTOM_TYPES[f_type_base]["type"]
    final_pointer = CUSTOM_TYPES[f_type_base]["pointer"]
    
    # Variable replacement
    for var in map_dict.keys():
        final_name = final_name.replace("%%" + var + "%%", str(map_dict[var]))
        final_type = final_type.replace("%%" + var + "%%", str(map_dict[var]))
    
    # Static variable replacement
    final_name = final_name.replace("%NAME%", name);
    #final_name = final_name.replace("%POINTER%", pointer);
    
    return [final_type, final_name, final_pointer, [f_type, name]]

def make_type(f_type, name):
    #print f_type, name
    f_type_base = f_type.split("*")[0].split("(")[0]
    if f_type in DEFAULT_TYPES:
        return make_default_type(f_type, name, DEFAULT_TYPES)
    elif f_type in OVERRIDE_TYPES:
        return make_default_type(f_type, name, OVERRIDE_TYPES)
    elif f_type_base in TYPE_TABLE.keys():
        return make_extended_type(f_type, name)
    elif f_type_base in CUSTOM_TYPES.keys():
        return make_custom_type(f_type, name)
    else:
        print "WARNING: Could not find equivalent C definition for type '%s'!" % type
        print "Make sure you define it!"
        return [None, None, None, [f_type, name]]
