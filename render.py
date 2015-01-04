import focapy.markupsafe as markupsafe
from focapy.jinja2 import Environment, FileSystemLoader
from focapy import cdef, focapy
from focapy.typedefs import FORTRAN_LOOKUP_TABLE
import re
import sys

try:
    from collections import OrderedDict
except:
    try:
        from ordereddict import OrderedDict
    except:
        print "ERROR: OrderedDict not found! It is required to run this script."
        sys.exit(1)

def c_ize(element_name, element_type):
    (c_type, c_var_name, c_pointers, (fort_type, fort_name)) = cdef.make_type(element_type, element_name)
    return "%s %s" % (c_type, c_var_name)

def wprint(w_str):
    print w_str
    return ""

#######################################################################
# Argument Hinting
#######################################################################
# temp, will need to load from config later

# ARGUMENT HINTING
# Gives Focapy a hint on how to interpret subroutine arguments!
# 
# This is generally used for clarifying inout subroutine intents.
# 
# There are generally two situations for wrapping assumed-shape arrays
# in Fortran -> C:
#   -> ASSUME INPUT - this assumes that the array is designated as an
#      input. More precisely, it is NOT an empty variable (or pointer),
#      and is an actual allocated array, ready to be read in and/or
#      modified in place (and returned to original caller). Note that
#      the array can still be modified and returned, even though the
#      intent logic is "in(put)".
#      
#      This requires that the variable's size be given. If the original
#      subroutine requires a size, you can cue Focapy to use an existing
#      size definition variable instead. If there is no existing
#      variable, a new variable for defining the size will be placed
#      alongside the assumed-shape array argument.
#      
#      For this case, we need to make the array variable a C_PTR, either
#      with intent in or inout (generally aligned with the original
#      subroutine's intent), and then create another non-argument
#      variable that will hold our assumed-shape array. Then we can
#      convert our array C_PTR to the assumed-shape array via
#      C_F_POINTER (and a given size), and then go ahead to pass the
#      assumed-shape array to the desired function.
#      
#   -> ASSUME OUTPUT - this assumes that the array is designated as an
#      output. More precisely, it is an EMPTY variable (or pointer).
#      Even if an allocated array is passed in, it is completely
#      inaccessible in the subroutine.
#      
#      For this case, we need to make the array variable a C_PTR, with
#      intent out, and then create another non-argument variable (using
#      a C type) that will hold our assumed-shape array. Then we pass
#      the empty assumed-shape array to the desired function. Finally,
#      we return the array variable by returning the C pointer (c_loc)
#      of our assumed-shape array.
# 
# Format:
#   [ ARRAY_VARIABLE ] = {
#                           "type"  : ARRAY_INTENT,
#                           "cue"   : ARRAY_SIZE_CUE_VARIABLE,
#                        }
#     ARRAY_VARIABLE: variable that has no known size, and is generally
#       designated for output only (e.g. empty array to be filled by a
#       subroutine).
#     ARRAY_INTENT: variable that defines the array's "true" intent.
#       Arguments are either "in" or "out". The behavior for each is
#     ARRAY_SIZE_CUE_VARIABLE: variable that hints at the size of the
#       unknown array variable. If set, behavior will be aligned to
#       in/inout (accepting the array input) - the result will align to
#       the original intent (in/inout). If set to None, a new size
#       variable will be declared alongside the assumed-shape array
#       input variable. This has no effect if the original subroutine
#       has declared the intent as out, or if ARRAY_INTENT is set to
#       out.
# 
# Intent Table:
#    =========================================================
#   | Original |  Hinting Properties  | Final  | Final Intent |
#   |  Intent  | Hinting? | Hint Type | Intent |    Logic     |
#   |------------------------------------------|--------------|
#   | in       | No       | N/A       | in     | in           |
#   | in       | Yes      | in        | in     | in           |
#   | in       | Yes      | out       | ERROR  | ERROR        |
#   | inout    | No       | N/A       | inout  | in           | **
#   | inout    | Yes      | in        | inout  | in           | **
#   | inout    | Yes      | out       | out    | out          | **
#   | out      | No       | N/A       | out    | out          |
#   | out      | Yes      | in        | ERROR  | ERROR        |
#   | out      | Yes      | out       | out    | out          |
#    =========================================================
#   ** Marks potential use cases. Other uses are either
#      redundant or unsupported (and doesn't make any sense).
# 
args_hinting_config = {}
args_hinting_config["read_dummy"] = {}
args_hinting_config["read_dummy"] = {}
args_hinting_config["read_dummy"]["read_array"] = {}
args_hinting_config["read_dummy"]["read_array"]["array"] = { 
                                                            "cue" : "ndata",
                                                            "type": "out",
                                                           }
args_hinting_config["read_dummy"]["print_array"] = {}
args_hinting_config["read_dummy"]["print_array"]["array"] = { 
                                                            "cue" : "ndata",
                                                            "type": "in",
                                                           }
args_hinting_config["read_dummy"]["ret_mean_from_array"] = {}
args_hinting_config["read_dummy"]["ret_mean_from_array"]["array"] = { 
                                                            "cue" : "ndata",
                                                            "type": "in",
                                                           }

###########################################################
# PREPROCESS
###########################################################
char_regex = re.compile(r'character\*(\d+)')
char_regex_replace = r'character(len=\1)'

SRC_FILE          = "read_dummy.f90"
NEW_SRC_FILE      = "focapy_out/test/read_dummy.f90"
NEW_HEADER_FILE   = "focapy_out/test/read_dummy.h"
NEW_SWIG_FILE     = "focapy_out/test/read_dummy.i"
NEW_FCWRAP_FILE   = "focapy_out/test/fcwrap.f90"

fh = open(SRC_FILE, "r")
fh_subs = open(NEW_SRC_FILE, "w")
fh_dat = fh.read()
fh.close()

if char_regex.search(fh_dat):
    fh_dat = char_regex.sub(char_regex_replace, fh_dat)

fh_subs.write(fh_dat)

fh_subs.close()

###########################################################
# PROCESS
###########################################################
module_dict = focapy.populate([NEW_SRC_FILE])
print "================================================================"

env = Environment(loader=FileSystemLoader('templates'))
env.globals['c_ize'] = c_ize
env.globals['wprint'] = wprint

header_template = env.get_template('module_header.h')

args_hinting = {}

#############################################
# ARGUMENT HINTING PROCESSING                
#############################################
for subroutine in module_dict["read_dummy"]["subroutines"]:
    print " * ARGS HINTING: Processing subroutine:", subroutine
    subroutine_dict = module_dict["read_dummy"]["subroutines"][subroutine]
    
    if len(subroutine_dict["arguments"].keys()) > 0:
        for subroutine_arg in subroutine_dict["arguments"]:
            subroutine_arg_dict = subroutine_dict["arguments"][subroutine_arg]
            if ("dimension(:)" in subroutine_arg_dict['attributes']):
                # VALIDATION
                if not (("intent(in)" in subroutine_arg_dict['attributes']) or ("intent(inout)" in subroutine_arg_dict['attributes']) or ("intent(out)" in subroutine_arg_dict['attributes'])):
                    print "ERROR: Unknown or no intent specified!"
                    sys.exit(1)
                
                hint_complete = False
                
                if "read_dummy" in args_hinting_config:
                    if not "read_dummy" in args_hinting:
                        args_hinting["read_dummy"] = {}
                    if not subroutine in args_hinting["read_dummy"]:
                        args_hinting["read_dummy"][subroutine] = {}
                    if (subroutine in args_hinting_config["read_dummy"]) and (subroutine_arg in args_hinting_config["read_dummy"][subroutine]):
                        if not subroutine_arg in args_hinting["read_dummy"]:
                            args_hinting["read_dummy"][subroutine][subroutine_arg] = {}
                        arg_hinting_dict = args_hinting_config["read_dummy"][subroutine][subroutine_arg]
                        if not (("cue" in arg_hinting_dict) and ("type" in arg_hinting_dict)):
                            print "ERROR: Args hinting configuration must have 'cue' and 'type' field!"
                            sys.exit(1)
                        
                        if ("intent(in)" in subroutine_arg_dict['attributes']):
                            if arg_hinting_dict["type"] == "out":
                                print "ERROR: Original intent 'in' can't be changed to an 'out'!"
                                sys.exit(1)
                            args_hinting["read_dummy"][subroutine][subroutine_arg]["type"] = "in"
                        elif ("intent(inout)" in subroutine_arg_dict['attributes']):
                            if (arg_hinting_dict["type"] == "in") or (arg_hinting_dict["type"] == "inout"):
                                args_hinting["read_dummy"][subroutine][subroutine_arg]["type"] = "in"
                            elif arg_hinting_dict["type"] == "out":
                                args_hinting["read_dummy"][subroutine][subroutine_arg]["type"] = "out"
                        elif ("intent(out)" in subroutine_arg_dict['attributes']):
                            if arg_hinting_dict["type"] == "in":
                                print "ERROR: Original intent 'out' can't be changed to an 'in'!"
                                sys.exit(1)
                            args_hinting["read_dummy"][subroutine][subroutine_arg]["type"] = "out"
                        
                        if args_hinting_config["read_dummy"][subroutine][subroutine_arg]["cue"]:
                            args_hinting["read_dummy"][subroutine][subroutine_arg]["cue"] = args_hinting_config["read_dummy"][subroutine][subroutine_arg]["cue"]
                        else:
                            args_hinting["read_dummy"][subroutine][subroutine_arg]["cue"] = None
                        
                        hint_complete = True
                    else:
                        hint_complete = False
                else:
                    hint_complete = False
                
                if not hint_complete:
                    if not "read_dummy" in args_hinting:
                        args_hinting["read_dummy"] = {}
                    if not subroutine in args_hinting["read_dummy"]:
                        args_hinting["read_dummy"][subroutine] = {}
                    if not subroutine_arg in args_hinting["read_dummy"]:
                        args_hinting["read_dummy"][subroutine][subroutine_arg] = {}
                    
                    if ("intent(in)" in subroutine_arg_dict['attributes']) or ("intent(inout)" in subroutine_arg_dict['attributes']):
                        args_hinting["read_dummy"][subroutine][subroutine_arg]["type"] = "in"
                    else:
                        args_hinting["read_dummy"][subroutine][subroutine_arg]["type"] = "out"
                    
                    args_hinting["read_dummy"][subroutine][subroutine_arg]["cue"] = None
                    

for function in module_dict["read_dummy"]["functions"]:
    print " * ARGS HINTING: Processing function:", function
    function_dict = module_dict["read_dummy"]["functions"][function]
    
    if len(function_dict["arguments"].keys()) > 0:
        for function_arg in function_dict["arguments"]:
            function_arg_dict = function_dict["arguments"][function_arg]
            if ("dimension(:)" in function_arg_dict['attributes']):
                # VALIDATION
                if not (("intent(in)" in function_arg_dict['attributes']) or ("intent(inout)" in function_arg_dict['attributes']) or ("intent(out)" in function_arg_dict['attributes'])):
                    print "ERROR: Unknown or no intent specified!"
                    sys.exit(1)
                
                hint_complete = False
                
                if "read_dummy" in args_hinting_config:
                    if not "read_dummy" in args_hinting:
                        args_hinting["read_dummy"] = {}
                    if not function in args_hinting["read_dummy"]:
                        args_hinting["read_dummy"][function] = {}
                    if (function in args_hinting_config["read_dummy"]) and (function_arg in args_hinting_config["read_dummy"][function]):
                        if not function_arg in args_hinting["read_dummy"]:
                            args_hinting["read_dummy"][function][function_arg] = {}
                        arg_hinting_dict = args_hinting_config["read_dummy"][function][function_arg]
                        if not (("cue" in arg_hinting_dict) and ("type" in arg_hinting_dict)):
                            print "ERROR: Args hinting configuration must have 'cue' and 'type' field!"
                            sys.exit(1)
                        
                        if ("intent(in)" in function_arg_dict['attributes']):
                            if arg_hinting_dict["type"] == "out":
                                print "ERROR: Original intent 'in' can't be changed to an 'out'!"
                                sys.exit(1)
                            args_hinting["read_dummy"][function][function_arg]["type"] = "in"
                        elif ("intent(inout)" in function_arg_dict['attributes']):
                            if (arg_hinting_dict["type"] == "in") or (arg_hinting_dict["type"] == "inout"):
                                args_hinting["read_dummy"][function][function_arg]["type"] = "in"
                            elif arg_hinting_dict["type"] == "out":
                                args_hinting["read_dummy"][function][function_arg]["type"] = "out"
                        elif ("intent(out)" in function_arg_dict['attributes']):
                            if arg_hinting_dict["type"] == "in":
                                print "ERROR: Original intent 'out' can't be changed to an 'in'!"
                                sys.exit(1)
                            args_hinting["read_dummy"][function][function_arg]["type"] = "out"
                        
                        if args_hinting_config["read_dummy"][function][function_arg]["cue"]:
                            args_hinting["read_dummy"][function][function_arg]["cue"] = args_hinting_config["read_dummy"][function][function_arg]["cue"]
                        else:
                            args_hinting["read_dummy"][function][function_arg]["cue"] = None
                        
                        hint_complete = True
                    else:
                        hint_complete = False
                else:
                    hint_complete = False
                
                if not hint_complete:
                    if not "read_dummy" in args_hinting:
                        args_hinting["read_dummy"] = {}
                    if not function in args_hinting["read_dummy"]:
                        args_hinting["read_dummy"][function] = {}
                    if not function_arg in args_hinting["read_dummy"]:
                        args_hinting["read_dummy"][function][function_arg] = {}
                    
                    if ("intent(in)" in function_arg_dict['attributes']) or ("intent(inout)" in function_arg_dict['attributes']):
                        args_hinting["read_dummy"][function][function_arg]["type"] = "in"
                    else:
                        args_hinting["read_dummy"][function][function_arg]["type"] = "out"
                    
                    args_hinting["read_dummy"][function][function_arg]["cue"] = None
                    

###########################################################
# PROCESS DICTIONARIES
###########################################################

elements_conv_dict = OrderedDict()

# TODO: handle weird attributes?
if len(module_dict["read_dummy"]["elements"].keys()) > 0:
    for element in module_dict["read_dummy"]["elements"]:
        print " * Processing top-level element:", element
        element_dict = module_dict["read_dummy"]["elements"][element]
        elements_conv_dict[element] = cdef.make_type(element_dict['type'], element)

derived_types_conv_dict = OrderedDict()

# TODO: handle weird attributes?
for d_type in module_dict["read_dummy"]["types"]:
    print " * Processing derived type:", d_type
    d_type_dict = module_dict["read_dummy"]["types"][d_type]
    
    derived_types_conv_dict[d_type] = []
    
    if len(d_type_dict["elements"].keys()) > 0:
        for d_type_ele in d_type_dict["elements"]:
            print "    * Processing derived type element:", d_type_ele
            d_type_ele_dict = d_type_dict["elements"][d_type_ele]
            derived_types_conv_dict[d_type].append(cdef.make_type(d_type_ele_dict['type'], d_type_ele))

subroutines_conv_dict = OrderedDict()
wrap_subroutines = []
for subroutine in module_dict["read_dummy"]["subroutines"]:
    print " * Processing subroutine:", subroutine
    subroutine_dict = module_dict["read_dummy"]["subroutines"][subroutine]
    
    use_wrapper = False
    if len(subroutine_dict["arguments"].keys()) > 0:
        for subroutine_arg in subroutine_dict["arguments"]:
            subroutine_arg_dict = subroutine_dict["arguments"][subroutine_arg]
            if (subroutine_arg_dict["type"].startswith("character(len=")) or ("dimension(:)" in subroutine_arg_dict['attributes']):
                wrap_subroutines.append(subroutine)
                print "    * Skipping subroutine %s - character/dimension(:) detected!" % subroutine
                use_wrapper = True
                break
    
    if use_wrapper:
        continue
    
    subroutines_conv_dict[subroutine] = []
    
    if len(subroutine_dict["arguments"].keys()) > 0:
        for subroutine_arg in subroutine_dict["arguments"]:
            print "    * Processing argument:", subroutine_arg
            subroutine_arg_dict = subroutine_dict["arguments"][subroutine_arg]
            subroutines_conv_dict[subroutine].append(cdef.make_type(subroutine_arg_dict['type'], subroutine_arg))
    #print subroutines_conv_dict

functions_conv_dict = OrderedDict()
wrap_functions = []
for function in module_dict["read_dummy"]["functions"]:
    print " * Processing function:", function
    function_dict = module_dict["read_dummy"]["functions"][function]
    
    use_wrapper = False
    if len(function_dict["arguments"].keys()) > 0:
        for function_arg in function_dict["arguments"]:
            function_arg_dict = function_dict["arguments"][function_arg]
            if (function_arg_dict["type"].startswith("character(len=")) or ("dimension(:)" in function_arg_dict['attributes']):
                wrap_functions.append(function)
                print "    * Skipping function %s - character/dimension(:) detected!" % function
                use_wrapper = True
                break
    
    if use_wrapper:
        continue
    
    functions_conv_dict[function] = { "returns" : cdef.make_type(function_dict["returns"], "RETURN_VAR"), "arguments": [] }
    
    if len(function_dict["arguments"].keys()) > 0:
        for function_arg in function_dict["arguments"]:
            print "    * Processing argument:", function_arg
            function_arg_dict = function_dict["arguments"][function_arg]
            functions_conv_dict[function]["arguments"].append(cdef.make_type(function_arg_dict['type'], function_arg))
    #print functions_conv_dict

###########################################################
# BIND(C)
###########################################################
fh_subs = open(NEW_SRC_FILE, "r")
fh_dat = fh_subs.read()
fh_subs.close()

for subroutine in module_dict["read_dummy"]["subroutines"]:
    if subroutine in wrap_subroutines:
        continue
    print " * Processing subroutine for BIND(C):", subroutine
    
    subroutine_regex = re.compile(r'subroutine\s*' + subroutine + r'\s*(\(.*\))?$')
    subroutine_regex_replace = r'subroutine ' + subroutine + r'\g<1> bind(c)'
    
    subroutine_regex_replace_noargs = r'subroutine ' + subroutine + r' bind(c)'
    
    lines = []
    
    for line in fh_dat.split('\n'):
        matches = subroutine_regex.search(line.strip())
        
        if not line.strip().startswith("end subroutine"):
            if matches:
                #print "MATCH RESULT:", matches.group(1)
                if matches.group(1):
                    #print "ARGS ENABLED, doing replace: %s" % subroutine_regex_replace
                    line = subroutine_regex.sub(subroutine_regex_replace, line)
                else:
                    #print "ARGS DISABLED"
                    line = subroutine_regex.sub(subroutine_regex_replace_noargs, line)
        lines.append(line)
    
    fh_dat = "\n".join(lines)

for function in module_dict["read_dummy"]["functions"]:
    if function in wrap_functions:
        continue
    print " * Processing function for BIND(C):", function
    function_regex = re.compile(r'(.*) function\s*' + function + r'\s*(\(.*\))?$')
    function_regex_replace = r'\g<1> function ' + function + r'\g<2> bind(c)'
    
    function_regex_replace_noargs = r'\g<1> function ' + function + r' bind(c)'
    
    lines = []
    
    for line in fh_dat.split('\n'):
        matches = function_regex.search(line.strip())
        
        if not line.strip().startswith("end function"):
            if matches:
                #print "MATCH RESULT:", matches.group(2), "on line", line
                if matches.group(1):
                    if matches.group(2):
                        #print "ARGS ENABLED, doing replace: %s" % function_regex_replace
                        line = function_regex.sub(function_regex_replace, line)
                    else:
                        #print "ARGS DISABLED"
                        line = function_regex.sub(function_regex_replace_noargs, line)
                else:
                    print "WARNING: Unable to process line "+line+" due to missing type part."
        lines.append(line)
    
    fh_dat = "\n".join(lines)
    

fh_subs = open(NEW_SRC_FILE, "w")
fh_subs.write(fh_dat)
fh_subs.close()

###########################################################
# SPECIAL SUBROUTINES AND FUNCTIONS
###########################################################
double_pointer_types = []

for subroutine in wrap_subroutines:
    print " * Processing special subroutine:", subroutine
    subroutine_dict = module_dict["read_dummy"]["subroutines"][subroutine]
    
    subroutines_conv_dict[subroutine] = []
    
    if len(subroutine_dict["arguments"].keys()) > 0:
        for subroutine_arg in subroutine_dict["arguments"]:
            print "    * Processing argument:", subroutine_arg
            subroutine_arg_dict = subroutine_dict["arguments"][subroutine_arg]
            subroutine_proc_res = cdef.make_type(subroutine_arg_dict['type'], subroutine_arg)
            
            if (subroutine_arg_dict["type"].lower().startswith("character(")) and (subroutine_arg_dict["type"].lower() not in [ "character(1)", "character(len=1)" ]):
                print "      * character(len=##) detected!"
                # Ensure that it is NOT a character array! (Convert bla[123] to simply bla!)
                subroutine_proc_res[1] = subroutine_arg
                
            if ("dimension(:)" in subroutine_arg_dict['attributes']):
                print "    * Dimension(:) detected for type %s (c type: %s)!" % (subroutine_proc_res[3][0], subroutine_proc_res[0])
                subroutine_proc_res[2] = "*"
                if subroutine_proc_res[0] not in double_pointer_types:
                    double_pointer_types.append(subroutine_proc_res[0])
            
            subroutines_conv_dict[subroutine].append(subroutine_proc_res)
    #print subroutines_conv_dict

for function in wrap_functions:
    print " * Processing special function:", function
    function_dict = module_dict["read_dummy"]["functions"][function]
    
    functions_conv_dict[function] = { "returns" : cdef.make_type(function_dict["returns"], "RETURN_VAR"), "arguments": [] }
    
    if len(function_dict["arguments"].keys()) > 0:
        for function_arg in function_dict["arguments"]:
            print "    * Processing argument:", function_arg
            function_arg_dict = function_dict["arguments"][function_arg]
            function_proc_res = cdef.make_type(function_arg_dict['type'], function_arg)
            
            if (function_arg_dict["type"].startswith("character(len=")):
                print "    * character(len=##) detected!"
                function_proc_res[1] = function_arg
                
            if ("dimension(:)" in function_arg_dict['attributes']):
                print "    * Dimension(:) detected for type %s (c type: %s)!" % (subroutine_proc_res[3][0], subroutine_proc_res[0])
                function_proc_res[2] = "*"
                if subroutine_proc_res[0] not in double_pointer_types:
                    double_pointer_types.append(subroutine_proc_res[0])
            
            functions_conv_dict[function]["arguments"].append(function_proc_res)
    #print functions_conv_dict

#######################################################################
# Generate Header
#######################################################################
print " * Generating header..."
output_from_header_template = header_template.render(module_name = "read_dummy", \
                                    elements = elements_conv_dict, \
                                    derived_types = derived_types_conv_dict, \
                                    subroutines = subroutines_conv_dict, \
                                    functions = functions_conv_dict, \
                                    args_hinting = args_hinting)
fh_header = open(NEW_HEADER_FILE, "w")
fh_header.write(output_from_header_template)
fh_header.close()

#print "========================================================"
#print output_from_header_template
#print "========================================================"
swig_template = env.get_template('module_swig.i')

print " * Generating SWIG..."
if len(double_pointer_types) > 0:
    output_from_swig_template = swig_template.render(module_name = "read_dummy", \
                                        assumed_shape_vars = double_pointer_types, \
                                        elements = elements_conv_dict, \
                                        derived_types = derived_types_conv_dict, \
                                        subroutines = subroutines_conv_dict, \
                                        functions = functions_conv_dict, \
                                        args_hinting = args_hinting)
else:
    output_from_swig_template = swig_template.render(module_name = "read_dummy", \
                                        elements = elements_conv_dict, \
                                        derived_types = derived_types_conv_dict, \
                                        subroutines = subroutines_conv_dict, \
                                        functions = functions_conv_dict, \
                                        args_hinting = args_hinting)

fh_swig = open(NEW_SWIG_FILE, "w")
fh_swig.write(output_from_swig_template)
fh_swig.close()

#print "========================================================"
#print output_from_swig_template

######################################################################
# POST-PROCESS WRAPPED SUBROUTINES AND FUNCTIONS: REPLACE
######################################################################
#_focapy_orig

fh_subs = open(NEW_SRC_FILE, "r")
fh_dat = fh_subs.read()
fh_subs.close()

fh_subs = open(NEW_SRC_FILE, "w")

for subroutine in wrap_subroutines:
    subroutine_regex = re.compile(r'subroutine\s*'+subroutine+r'\s*\(')
    subroutine_regex_replace = r'subroutine '+subroutine+r'_focapy_orig('
    
    end_subroutine_regex = re.compile(r'end\s*subroutine\s*'+subroutine)
    end_subroutine_regex_replace = r'end subroutine '+subroutine+r'_focapy_orig'
    
    fh_dat = subroutine_regex.sub(subroutine_regex_replace, fh_dat)
    fh_dat = end_subroutine_regex.sub(end_subroutine_regex_replace, fh_dat)

for subroutine in wrap_subroutines:
    public_subroutine_regex = re.compile(r'public\s*\:\:\s*'+subroutine+r'[ \t]*')
    public_subroutine_regex_replace = r'public :: '+subroutine+r'_focapy_orig'
    
    fh_dat = public_subroutine_regex.sub(public_subroutine_regex_replace, fh_dat)

## FUNCTIONS
for function in wrap_functions:
    function_regex = re.compile(r'function\s*'+function+r'\s*\(')
    function_regex_replace = r'function '+function+r'_focapy_orig('
    
    end_function_regex = re.compile(r'end\s*function\s*'+function)
    end_function_regex_replace = r'end function '+function+r'_focapy_orig'
    
    fh_dat = function_regex.sub(function_regex_replace, fh_dat)
    fh_dat = end_function_regex.sub(end_function_regex_replace, fh_dat)

for function in wrap_functions:
    public_function_regex = re.compile(r'public\s*\:\:\s*'+function+r'[ \t]*')
    public_function_regex_replace = r'public :: '+function+r'_focapy_orig'
    
    fh_dat = public_function_regex.sub(public_function_regex_replace, fh_dat)

for function in wrap_functions:
    public_function_regex = re.compile(r''+function+r'[ \t]\=[ \t]*')
    public_function_regex_replace = r''+function+r'_focapy_orig = '
    
    fh_dat = public_function_regex.sub(public_function_regex_replace, fh_dat)

fh_subs.write(fh_dat)

fh_subs.close()

######################################################################
# POST-PROCESS WRAPPED SUBROUTINES AND FUNCTIONS: FCWRAP
######################################################################
print " * Generating FCWrap..."

fcwrap_template = env.get_template('module_fcwrap.f90')
output_from_fcwrap_template = fcwrap_template.render(module_name = "read_dummy", \
                                wrap_subroutines = wrap_subroutines, \
                                wrap_functions = wrap_functions, \
                                subroutines = module_dict["read_dummy"]["subroutines"], \
                                functions = module_dict["read_dummy"]["functions"],
                                fortran_lookup_table = FORTRAN_LOOKUP_TABLE,
                                args_hinting = args_hinting)
#print output_from_fcwrap_template
fh_fcwrap = open(NEW_FCWRAP_FILE, "w")
fh_fcwrap.write(output_from_fcwrap_template)
fh_fcwrap.close()
